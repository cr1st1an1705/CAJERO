from decimal import Decimal
from pydantic import BaseModel, Field

class MontoRequest(BaseModel):
    monto: Decimal = Field(..., gt=0)

class SaldoResponse(BaseModel):
    numero_cuenta: str
    saldo: Decimal
    nodo_bd: str

class OperacionResponse(BaseModel):
    mensaje: str
    saldo_anterior: Decimal
    saldo_nuevo: Decimal
    nodo_bd: str

class HistorialItem(BaseModel):
    tipo: str
    monto: Decimal
    saldo_anterior: Decimal
    saldo_nuevo: Decimal
    descripcion: str | None
    fecha: str

class LogoutResponse(BaseModel):
    mensaje: str
