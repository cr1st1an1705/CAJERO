# Cajero Frontend

Frontend del cajero ATM construido con React + Vite.

## Scripts
- `npm run dev`: desarrollo local.
- `npm run build`: build de produccion.
- `npm run start`: servir build en modo produccion (Railway).
- `npm run lint`: validacion de estilo.

## Variable de entorno
Crear `.env` a partir de `.env.example`:

- `VITE_API_BASE_URL`: URL publica del backend (sin slash final).

Ejemplo:

`VITE_API_BASE_URL=https://cajero-backend.up.railway.app`

## Despliegue en Railway

### Archivos clave
- `Procfile`
- `.env.example`
- `package.json`

### Flujo esperado en Railway
1. Instalar dependencias.
2. Ejecutar `npm run build`.
3. Ejecutar `npm run start`.

El frontend queda accesible en el puerto dinamico de Railway (`$PORT`).
