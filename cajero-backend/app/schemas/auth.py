from pydantic import BaseModel, Field

class LoginRequest(BaseModel):
    numero_cuenta: str = Field(..., min_length=5, max_length=20)
    pin: str = Field(..., min_length=4, max_length=4)
    atm_origen: str = Field(default="ATM-LOCAL", max_length=50)

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    mensaje: str
    titular_nombre: str
    tipo_cuenta: str
