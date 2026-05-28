import logging
from time import sleep
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import engine_primary
from app.core.logging_config import configurar_logging
from app.db.base import Base
import app.models  # noqa: F401 - registra modelos para metadata
from app.routers.auth import router as auth_router
from app.routers.atm import router as atm_router
from app.routers.health import router as health_router

configurar_logging()
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.APP_NOMBRE,
    version="1.0.0",
    description="Backend de cajero ATM sin frontend. Proyecto base para universidad."
)

if settings.ALLOWED_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(auth_router)
app.include_router(atm_router)
app.include_router(health_router)

@app.on_event("startup")
def auto_init_schema() -> None:
    if not settings.AUTO_INIT_SCHEMA:
        return

    # En cloud puede haber una breve espera hasta que MySQL acepte conexiones.
    for intento in range(1, 6):
        try:
            Base.metadata.create_all(bind=engine_primary)
            logger.info("AUTO_INIT_SCHEMA activo: esquema verificado/creado correctamente")
            return
        except Exception as exc:
            logger.warning("Intento %s/5 de inicializar esquema fallo: %s", intento, exc)
            sleep(2)

    raise RuntimeError("No se pudo inicializar el esquema de base de datos con AUTO_INIT_SCHEMA")

@app.get("/")
def root():
    return {
        "mensaje": "Backend Cajero ATM activo",
        "docs": "/docs",
        "redoc": "/redoc"
    }
