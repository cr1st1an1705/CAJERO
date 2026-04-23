from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.auth import LoginRequest, TokenResponse
from app.services.auth_service import login

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/login", response_model=TokenResponse)
def login_route(payload: LoginRequest, request: Request, db: Session = Depends(get_db)):
    token = login(
        db=db,
        numero_cuenta=payload.numero_cuenta,
        pin=payload.pin,
        atm_origen=payload.atm_origen,
        ip_origen=request.client.host if request.client else None
    )
    return {
        "access_token": token,
        "token_type": "bearer",
        "mensaje": "Login correcto"
    }
