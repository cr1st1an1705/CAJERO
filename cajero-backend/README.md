# Backend-Cajero

Proyecto base de backend para un cajero ATM sin frontend.

## Stack
- Python
- FastAPI
- MySQL
- Docker

## Que hace
- Login con numero de cuenta y PIN
- Bloqueo por intentos fallidos
- Sesion con token
- Cierre por inactividad
- Consulta de saldo
- Deposito a cuenta autenticada
- Retiro con control de concurrencia
- Historial
- Logs en archivo y en BD
- Cambio de nodo primary a secondary si primary falla

## Estructura
- app/
- database/
- docker/
- docs/
- logs/
- scripts/

## Importante
La parte de replicacion real entre primary y secondary queda separada para el equipo BD.

## Despliegue en Railway

### Archivos clave
- `Procfile`
- `.env.example`
- `requirements.txt`

### Comando de inicio
El backend usa este comando en Railway:

`uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Variables de entorno minimas
- `JWT_SECRET`: secreto largo y aleatorio.
- `BACKEND_CORS_ORIGINS`: URL publica del frontend Railway.
- `DATABASE_URL` o `DB_PRIMARY_URL`: URL de MySQL de Railway.

### Variables opcionales
- `ENABLE_DB_FAILOVER=false`: recomendado cuando usas una sola instancia MySQL en Railway.
- `DB_SECONDARY_URL`: usar solo si despliegas estrategia de failover real.

### Notas
- Si Railway entrega la URL en formato `mysql://`, el backend la convierte automaticamente a `mysql+pymysql://`.
- Si frontend y backend estan en dominios distintos, configura `BACKEND_CORS_ORIGINS` con el dominio publico del frontend.
