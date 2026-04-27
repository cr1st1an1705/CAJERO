#!/usr/bin/env bash
set -e

# este script es el monitor de conmutacion por error
# no pertenece a la logica del cajero
# pertenece a la infraestructura de base de datos

cd "$(dirname "$0")/.."

ESTADO="/tmp/cajero_failover_estado"
LOG="logs/failover-monitor.log"

mkdir -p logs

echo "normal" > "$ESTADO"

echo "$(date '+%Y-%m-%d %H:%M:%S') monitor iniciado" >> "$LOG"

while true; do
  if mysql -h 127.0.0.1 -P 3307 -u cajero_user -pcajero_pass -e "SELECT 1;" >/dev/null 2>&1; then

    if grep -q "failover" "$ESTADO"; then
      echo "$(date '+%Y-%m-%d %H:%M:%S') primary regreso se inicia failback automatico" >> "$LOG"

      sleep 10

      ./scripts/sincronizar_primary_desde_secondary.sh >> "$LOG" 2>&1
      ./scripts/configurar_replica.sh >> "$LOG" 2>&1

      echo "normal" > "$ESTADO"
      echo "$(date '+%Y-%m-%d %H:%M:%S') failback terminado sistema en modo normal" >> "$LOG"
    fi

  else

    if grep -q "normal" "$ESTADO"; then
      echo "failover" > "$ESTADO"
      echo "$(date '+%Y-%m-%d %H:%M:%S') primary caido backend debe usar secondary" >> "$LOG"
    fi

  fi

  sleep 5
done
