from sqlalchemy import BigInteger, Boolean, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class Sesion(Base):
    __tablename__ = "sesiones"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    cuenta_id: Mapped[int] = mapped_column(ForeignKey("cuentas.id"), nullable=False, index=True)
    token: Mapped[str] = mapped_column(String(500), nullable=False, unique=True)
    ultimo_movimiento: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    activa: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
