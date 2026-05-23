from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.auth import LoginRequest, TokenResponse
from app.services.auth_service import login

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/login", response_model=TokenResponse)
def login_route(payload: LoginRequest, request: Request, db: Session = Depends(get_db)):
    login_result = login(
        db=db,
        numero_cuenta=payload.numero_cuenta,
        pin=payload.pin,
        atm_origen=payload.atm_origen,
        ip_origen=request.client.host if request.client else None
    )
    return {
        "access_token": login_result["access_token"],
        "token_type": "bearer",
        "mensaje": "Login correcto",
        "titular_nombre": login_result["titular_nombre"],
        "tipo_cuenta": login_result["tipo_cuenta"],
    }
