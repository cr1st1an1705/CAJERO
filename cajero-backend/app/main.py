from fastapi import FastAPI
from app.core.config import settings
from app.core.logging_config import configurar_logging
from app.routers.auth import router as auth_router
from app.routers.atm import router as atm_router
from app.routers.health import router as health_router

configurar_logging()

app = FastAPI(
    title=settings.APP_NOMBRE,
    version="1.0.0",
    description="Backend de cajero ATM sin frontend. Proyecto base para universidad."
)

app.include_router(auth_router)
app.include_router(atm_router)
app.include_router(health_router)

@app.get("/")
def root():
    return {
        "mensaje": "Backend Cajero ATM activo",
        "docs": "/docs",
        "redoc": "/redoc"
    }
