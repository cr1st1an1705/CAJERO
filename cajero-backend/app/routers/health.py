from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.db_node_service import healthcheck_db

router = APIRouter(prefix="/api/health", tags=["health"])

@router.get("")
def health_route(db: Session = Depends(get_db)):
    return {
        "app": "ok",
        "database": healthcheck_db(db)
    }
