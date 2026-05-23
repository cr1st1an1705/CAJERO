from datetime import datetime, timedelta, timezone
import jwt
from passlib.context import CryptContext
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_pin(pin: str) -> str:
    return pwd_context.hash(pin)

def verificar_pin(pin_plano: str, pin_hash: str) -> bool:
    return pwd_context.verify(pin_plano, pin_hash)

def crear_token(numero_cuenta: str) -> str:
    ahora = datetime.now(timezone.utc)
    payload = {
        "sub": numero_cuenta,
        "iat": ahora,
        "exp": ahora + timedelta(minutes=settings.JWT_EXP_MINUTES),
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

def decodificar_token(token: str) -> dict:
    return jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
