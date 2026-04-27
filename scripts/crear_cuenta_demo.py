import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.core.security import hash_pin
from app.models import Cuenta
from app.db.base import Base

engine = create_engine(settings.PRIMARY_DB_URL, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

Base.metadata.create_all(bind=engine)

db = SessionLocal()
try:
    numero = input("Numero de cuenta: ").strip()
    nombre = input("Titular: ").strip()
    pin = input("PIN de 4 digitos: ").strip()

    existe = db.query(Cuenta).filter(Cuenta.numero_cuenta == numero).first()
    if existe:
        print("La cuenta ya existe")
    else:
        cuenta = Cuenta(
            numero_cuenta=numero,
            titular_nombre=nombre,
            pin_hash=hash_pin(pin),
            saldo=0,
            intentos_fallidos=0,
            activa=True
        )
        db.add(cuenta)
        db.commit()
        print("Cuenta creada")
finally:
    db.close()
