# Guia de Despliegue en Railway

Esta guia deja el proyecto listo para desplegar frontend, backend y base de datos en Railway.

## 1) Crear servicios en Railway

Crear 3 servicios dentro del mismo proyecto Railway:

1. MySQL (plugin de Railway).
2. Backend (raiz del servicio: `cajero-backend`).
3. Frontend (raiz del servicio: `cajero-frontend`).

## 2) Configurar backend

### Root Directory
`cajero-backend`

### Start Command
Railway tomara `Procfile`:

`web: uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Variables de entorno requeridas

- `JWT_SECRET`: secreto seguro.
- `BACKEND_CORS_ORIGINS`: URL publica del frontend.
- `DATABASE_URL` o `DB_PRIMARY_URL`: URL de MySQL Railway.

### Variables recomendadas

- `ENABLE_DB_FAILOVER=false` (si usas una sola BD en Railway).

### Nota de conexion

Si Railway entrega la URL como `mysql://...`, la app la adapta automaticamente a `mysql+pymysql://...`.

## 3) Configurar frontend

### Root Directory
`cajero-frontend`

### Build Command
`npm run build`

### Start Command
Railway tomara `Procfile`:

`web: npm run start`

### Variable de entorno requerida

- `VITE_API_BASE_URL`: URL publica del backend, por ejemplo:
  - `https://cajero-backend-production.up.railway.app`

## 4) Conectar backend con MySQL Railway

En el servicio backend, definir `DATABASE_URL` con la cadena de conexion del servicio MySQL de Railway.

## 5) Verificaciones post-despliegue

1. Backend health:
   - `GET https://<backend>/api/health`
2. Frontend:
   - abrir URL publica y validar login/retiro/saldo.
3. CORS:
   - confirmar que no hay bloqueos de navegador entre frontend y backend.

## 6) Recomendaciones de produccion

- Rotar `JWT_SECRET` periodicamente.
- No reutilizar credenciales de desarrollo.
- Activar monitoreo y logs en Railway.
- Mantener `ENABLE_DB_FAILOVER=false` mientras exista una sola instancia MySQL.
