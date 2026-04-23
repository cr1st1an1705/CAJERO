import logging
from contextlib import contextmanager
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

logger = logging.getLogger(__name__)

engine_primary = create_engine(
    settings.PRIMARY_DB_URL,
    pool_pre_ping=True,
    pool_recycle=3600,
    future=True,
)
engine_secondary = create_engine(
    settings.SECONDARY_DB_URL,
    pool_pre_ping=True,
    pool_recycle=3600,
    future=True,
)

SessionPrimary = sessionmaker(bind=engine_primary, autoflush=False, autocommit=False, future=True)
SessionSecondary = sessionmaker(bind=engine_secondary, autoflush=False, autocommit=False, future=True)

def probar_engine(engine) -> bool:
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception as e:
        logger.warning(f"Fallo conexion a DB: {e}")
        return False

def obtener_fabrica_sesion():
    if probar_engine(engine_primary):
        return SessionPrimary, "primary"
    if probar_engine(engine_secondary):
        return SessionSecondary, "secondary"
    raise RuntimeError("No hay conexion ni a primary ni a secondary")

def get_db():
    SessionFactory, nodo = obtener_fabrica_sesion()
    db = SessionFactory()
    db.info["nodo_bd"] = nodo
    try:
        yield db
    finally:
        db.close()

@contextmanager
def db_context():
    SessionFactory, nodo = obtener_fabrica_sesion()
    db = SessionFactory()
    db.info["nodo_bd"] = nodo
    try:
        yield db
    finally:
        db.close()
