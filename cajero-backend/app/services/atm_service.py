from datetime import datetime, timedelta
from decimal import Decimal
from fastapi import HTTPException, status
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.core.config import settings
from app.models.cuenta import Cuenta
from app.models.sesion import Sesion
from app.models.transaccion import Transaccion
from app.services.audit_service import registrar_auditoria

def validar_sesion(db: Session, token: str):
    sesion = db.query(Sesion).filter(Sesion.token == token, Sesion.activa == True).first()
    if not sesion:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Sesion invalida")

    ahora = datetime.now()
    if sesion.ultimo_movimiento < ahora - timedelta(minutes=settings.SESSION_IDLE_MINUTES):
        sesion.activa = False
        db.commit()
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Sesion expirada por inactividad")

    cuenta = db.query(Cuenta).filter(Cuenta.id == sesion.cuenta_id).first()
    if not cuenta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cuenta no encontrada")

    sesion.ultimo_movimiento = ahora
    db.commit()
    return cuenta

def consultar_saldo(db: Session, cuenta: Cuenta, atm_origen: str = "ATM-LOCAL"):
    registrar_auditoria(db, cuenta.id, "INFO", "FISICO", "SELECCION_CONSULTA_SALDO", f"ATM={atm_origen}")
    registrar_auditoria(db, cuenta.id, "INFO", "LOGICO", "CONSULTA_SALDO", f"Saldo actual consultado")
    db.commit()
    return Decimal(str(cuenta.saldo))

def depositar(db: Session, cuenta: Cuenta, monto: Decimal, atm_origen: str = "ATM-LOCAL"):
    if monto <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Monto invalido")

    # Aqui se hace el bloqueo de fila para evitar que dos operaciones cambien el mismo saldo al mismo tiempo.
    fila = db.execute(
        text("SELECT id, saldo FROM cuentas WHERE id = :id FOR UPDATE"),
        {"id": cuenta.id}
    ).mappings().first()

    saldo_anterior = Decimal(str(fila["saldo"]))
    saldo_nuevo = saldo_anterior + monto

    db.execute(
        text("UPDATE cuentas SET saldo = :saldo WHERE id = :id"),
        {"saldo": saldo_nuevo, "id": cuenta.id}
    )

    db.add(
        Transaccion(
            cuenta_id=cuenta.id,
            tipo="DEPOSITO",
            monto=monto,
            saldo_anterior=saldo_anterior,
            saldo_nuevo=saldo_nuevo,
            descripcion="Deposito a cuenta autenticada",
            atm_origen=atm_origen,
            fecha=datetime.now(),
        )
    )

    registrar_auditoria(db, cuenta.id, "INFO", "FISICO", "SOLICITUD_DEPOSITO", f"Monto={monto}")
    registrar_auditoria(db, cuenta.id, "INFO", "LOGICO", "DEPOSITO_OK", f"Saldo nuevo={saldo_nuevo}")
    db.commit()
    return saldo_anterior, saldo_nuevo

def retirar(db: Session, cuenta: Cuenta, monto: Decimal, atm_origen: str = "ATM-LOCAL"):
    if monto <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Monto invalido")

    # Aqui se hace el bloqueo de fila para que un solo retiro pueda tocar el saldo de la cuenta a la vez.
    fila = db.execute(
        text("SELECT id, saldo FROM cuentas WHERE id = :id FOR UPDATE"),
        {"id": cuenta.id}
    ).mappings().first()

    saldo_anterior = Decimal(str(fila["saldo"]))

    if saldo_anterior < monto:
        registrar_auditoria(db, cuenta.id, "WARNING", "LOGICO", "RETIRO_RECHAZADO", "Saldo insuficiente")
        db.commit()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Saldo insuficiente")

    saldo_nuevo = saldo_anterior - monto

    db.execute(
        text("UPDATE cuentas SET saldo = :saldo WHERE id = :id"),
        {"saldo": saldo_nuevo, "id": cuenta.id}
    )

    db.add(
        Transaccion(
            cuenta_id=cuenta.id,
            tipo="RETIRO",
            monto=monto,
            saldo_anterior=saldo_anterior,
            saldo_nuevo=saldo_nuevo,
            descripcion="Retiro desde cuenta autenticada",
            atm_origen=atm_origen,
            fecha=datetime.now(),
        )
    )

    registrar_auditoria(db, cuenta.id, "INFO", "FISICO", "SOLICITUD_RETIRO", f"Monto={monto}")
    registrar_auditoria(db, cuenta.id, "INFO", "LOGICO", "RETIRO_OK", f"Saldo nuevo={saldo_nuevo}")
    db.commit()
    return saldo_anterior, saldo_nuevo

def historial(db: Session, cuenta: Cuenta):
    filas = (
        db.query(Transaccion)
        .filter(Transaccion.cuenta_id == cuenta.id)
        .order_by(Transaccion.fecha.desc())
        .limit(50)
        .all()
    )
    registrar_auditoria(db, cuenta.id, "INFO", "LOGICO", "CONSULTA_HISTORIAL", "Consulta de historial")
    db.commit()
    return filas

def logout(db: Session, token: str, cuenta: Cuenta):
    sesion = db.query(Sesion).filter(Sesion.token == token, Sesion.activa == True).first()
    if sesion:
        sesion.activa = False
        registrar_auditoria(db, cuenta.id, "INFO", "FISICO", "SALIDA_CAJERO", "Sesion cerrada")
        registrar_auditoria(db, cuenta.id, "INFO", "LOGICO", "LOGOUT_OK", "Sesion finalizada")
        db.commit()
