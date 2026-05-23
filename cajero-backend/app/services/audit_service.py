from datetime import datetime
import logging
from app.models.auditoria import Auditoria

logger = logging.getLogger(__name__)

def registrar_auditoria(db, cuenta_id, nivel, categoria, accion, detalle=None, ip_origen=None):
    nodo_bd = db.info.get("nodo_bd", "desconocido")
    registro = Auditoria(
        cuenta_id=cuenta_id,
        nivel=nivel,
        categoria=categoria,
        accion=accion,
        detalle=detalle,
        nodo_bd=nodo_bd,
        ip_origen=ip_origen,
        fecha=datetime.now(),
    )
    db.add(registro)
    logger.info(f"{categoria} | {accion} | cuenta={cuenta_id} | nodo={nodo_bd} | {detalle}")
