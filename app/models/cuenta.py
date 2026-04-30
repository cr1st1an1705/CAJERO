from sqlalchemy import BigInteger, Boolean, DateTime, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class Cuenta(Base):
    __tablename__ = "cuentas"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    numero_cuenta: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    titular_nombre: Mapped[str] = mapped_column(String(150), nullable=False)
    pin_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    saldo: Mapped[float] = mapped_column(Numeric(18, 2), nullable=False, default=0)
    intentos_fallidos: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    bloqueada_hasta: Mapped[DateTime | None] = mapped_column(DateTime, nullable=True)
    activa: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    tipo_cuenta: Mapped[str] = mapped_column(String(20), nullable=False, default='AHORRO')
