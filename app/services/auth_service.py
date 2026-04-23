from datetime import datetime, timedelta
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.security import verificar_pin, crear_token
from app.models.cuenta import Cuenta
from app.models.sesion import Sesion
from app.services.audit_service import registrar_auditoria

def login(db: Session, numero_cuenta: str, pin: str, atm_origen: str, ip_origen: str | None = None) -> str:
    cuenta = db.query(Cuenta).filter(Cuenta.numero_cuenta == numero_cuenta).first()

    if not cuenta:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales invalidas")

    ahora = datetime.now()

    if cuenta.bloqueada_hasta and cuenta.bloqueada_hasta > ahora:
        raise HTTPException(
            status_code=status.HTTP_423_LOCKED,
            detail=f"Cuenta bloqueada hasta {cuenta.bloqueada_hasta}"
        )

    if not verificar_pin(pin, cuenta.pin_hash):
        cuenta.intentos_fallidos += 1
        if cuenta.intentos_fallidos >= settings.MAX_INTENTOS_PIN:
            cuenta.bloqueada_hasta = ahora + timedelta(minutes=settings.MINUTOS_BLOQUEO)
            cuenta.intentos_fallidos = 0
            registrar_auditoria(
                db, cuenta.id, "WARNING", "LOGICO",
                "CUENTA_BLOQUEADA",
                f"Se bloqueara por {settings.MINUTOS_BLOQUEO} minuto(s)"
            )
        else:
            registrar_auditoria(
                db, cuenta.id, "WARNING", "LOGICO",
                "PIN_INVALIDO",
                f"Intento fallido desde {atm_origen}"
            )
        db.commit()
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales invalidas")

    cuenta.intentos_fallidos = 0
    cuenta.bloqueada_hasta = None

    token = crear_token(cuenta.numero_cuenta)
    sesion = Sesion(
        cuenta_id=cuenta.id,
        token=token,
        ultimo_movimiento=ahora,
        activa=True
    )
    db.add(sesion)

    registrar_auditoria(
        db, cuenta.id, "INFO", "FISICO",
        "INGRESO_CUENTA_Y_PIN",
        f"ATM={atm_origen}"
    )
    registrar_auditoria(
        db, cuenta.id, "INFO", "LOGICO",
        "LOGIN_OK",
        f"Sesion abierta desde {atm_origen}",
        ip_origen=ip_origen
    )

    db.commit()
    return token
