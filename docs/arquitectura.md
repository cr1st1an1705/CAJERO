ARQUITECTURA DEL PROYECTO

Lenguaje
- Python

Framework
- FastAPI

Base de datos
- MySQL primary
- MySQL secondary

Capas
- routers: exponen endpoints
- services: concentran la logica del cajero
- models: representan tablas
- schemas: validan entrada y salida
- core: config, seguridad, logging, DB
- docs: explicacion para backend, BD y manual
- database: schema SQL y DBML

Flujos principales
1. Login con numero de cuenta y PIN
2. Validacion de bloqueo temporal por intentos fallidos
3. Creacion de sesion con token
4. Expiracion de sesion por inactividad
5. Consulta de saldo
6. Deposito a cuenta autenticada
7. Retiro con bloqueo de fila
8. Historial de transacciones
9. Auditoria y logs
10. Cambio automatico a nodo secondary si primary falla

Concurrencia
- En retiro y deposito se usa SELECT ... FOR UPDATE.
- Esto evita que dos operaciones cambien el mismo saldo al mismo tiempo.
