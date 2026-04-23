MANUAL DE USUARIO

1. Entrar a la documentacion tecnica
- Abrir en navegador: http://localhost:8000/docs

2. Login
- Endpoint: POST /api/auth/login
- Enviar numero_cuenta, pin y atm_origen

3. Usar token
- Copiar access_token
- En docs usar Authorize
- Pegar: Bearer TOKEN

4. Operaciones
- GET /api/atm/saldo
- POST /api/atm/depositar
- POST /api/atm/retirar
- GET /api/atm/historial
- POST /api/atm/logout

5. Reglas
- 4 PIN invalidos bloquean por 1 minuto
- 3 minutos sin actividad cierran la sesion
- No hay transferencias a terceros
- Deposito solo a cuenta autenticada
