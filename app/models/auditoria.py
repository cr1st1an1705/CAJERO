from sqlalchemy import BigInteger, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class Auditoria(Base):
    __tablename__ = "auditorias"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    cuenta_id: Mapped[int | None] = mapped_column(ForeignKey("cuentas.id"), nullable=True, index=True)
    nivel: Mapped[str] = mapped_column(String(20), nullable=False, default="INFO")
    categoria: Mapped[str] = mapped_column(String(20), nullable=False)
    accion: Mapped[str] = mapped_column(String(100), nullable=False)
    detalle: Mapped[str | None] = mapped_column(Text, nullable=True)
    nodo_bd: Mapped[str | None] = mapped_column(String(30), nullable=True)
    ip_origen: Mapped[str | None] = mapped_column(String(50), nullable=True)
    fecha: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
