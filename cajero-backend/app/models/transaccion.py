from sqlalchemy import BigInteger, DateTime, ForeignKey, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class Transaccion(Base):
    __tablename__ = "transacciones"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    cuenta_id: Mapped[int] = mapped_column(ForeignKey("cuentas.id"), nullable=False, index=True)
    tipo: Mapped[str] = mapped_column(String(20), nullable=False)
    monto: Mapped[float] = mapped_column(Numeric(18, 2), nullable=False, default=0)
    saldo_anterior: Mapped[float] = mapped_column(Numeric(18, 2), nullable=False, default=0)
    saldo_nuevo: Mapped[float] = mapped_column(Numeric(18, 2), nullable=False, default=0)
    descripcion: Mapped[str | None] = mapped_column(Text, nullable=True)
    atm_origen: Mapped[str] = mapped_column(String(50), nullable=False, default="ATM-LOCAL")
    fecha: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
