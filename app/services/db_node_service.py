from sqlalchemy import text

def obtener_nodo_actual(db) -> str:
    return db.info.get("nodo_bd", "desconocido")

def healthcheck_db(db) -> dict:
    db.execute(text("SELECT 1"))
    return {
        "ok": True,
        "nodo_bd": obtener_nodo_actual(db)
    }
