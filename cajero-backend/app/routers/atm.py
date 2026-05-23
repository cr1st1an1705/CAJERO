from fastapi import APIRouter, Depends
from app.api.deps import get_current_account
from app.schemas.atm import (
    HistorialItem,
    LogoutResponse,
    MontoRequest,
    OperacionResponse,
    SaldoResponse,
)
from app.services.atm_service import consultar_saldo, depositar, retirar, historial, logout

router = APIRouter(prefix="/api/atm", tags=["atm"])

@router.get("/saldo", response_model=SaldoResponse)
def saldo_route(ctx = Depends(get_current_account)):
    cuenta = ctx["cuenta"]
    db = ctx["db"]
    saldo = consultar_saldo(db, cuenta)
    return {
        "numero_cuenta": cuenta.numero_cuenta,
        "saldo": saldo,
        "nodo_bd": db.info.get("nodo_bd", "desconocido")
    }

@router.post("/depositar", response_model=OperacionResponse)
def depositar_route(payload: MontoRequest, ctx = Depends(get_current_account)):
    cuenta = ctx["cuenta"]
    db = ctx["db"]
    saldo_anterior, saldo_nuevo = depositar(db, cuenta, payload.monto)
    return {
        "mensaje": "Deposito aplicado",
        "saldo_anterior": saldo_anterior,
        "saldo_nuevo": saldo_nuevo,
        "nodo_bd": db.info.get("nodo_bd", "desconocido")
    }

@router.post("/retirar", response_model=OperacionResponse)
def retirar_route(payload: MontoRequest, ctx = Depends(get_current_account)):
    cuenta = ctx["cuenta"]
    db = ctx["db"]
    saldo_anterior, saldo_nuevo = retirar(db, cuenta, payload.monto)
    return {
        "mensaje": "Retiro aplicado",
        "saldo_anterior": saldo_anterior,
        "saldo_nuevo": saldo_nuevo,
        "nodo_bd": db.info.get("nodo_bd", "desconocido")
    }

@router.get("/historial", response_model=list[HistorialItem])
def historial_route(ctx = Depends(get_current_account)):
    cuenta = ctx["cuenta"]
    db = ctx["db"]
    filas = historial(db, cuenta)
    return [
        {
            "tipo": x.tipo,
            "monto": x.monto,
            "saldo_anterior": x.saldo_anterior,
            "saldo_nuevo": x.saldo_nuevo,
            "descripcion": x.descripcion,
            "fecha": x.fecha.strftime("%Y-%m-%d %H:%M:%S"),
        }
        for x in filas
    ]

@router.post("/logout", response_model=LogoutResponse)
def logout_route(ctx = Depends(get_current_account)):
    cuenta = ctx["cuenta"]
    db = ctx["db"]
    token = ctx["token"]
    logout(db, token, cuenta)
    return {"mensaje": "Sesion cerrada"}
