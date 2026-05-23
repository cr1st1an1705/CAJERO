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
