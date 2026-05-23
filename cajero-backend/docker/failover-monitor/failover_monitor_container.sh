#!/usr/bin/env bash
set -e

# monitor de conmutacion por error
# corre como contenedor docker
# revisa si mysql primary esta activo
# si primary cae deja el sistema en modo failover
# si primary vuelve sincroniza secondary hacia primary
# despues reactiva la replica primary hacia secondary

PRIMARY_HOST="${PRIMARY_HOST:-mysql-primary}"
SECONDARY_HOST="${SECONDARY_HOST:-mysql-secondary}"
MYSQL_PORT="${MYSQL_PORT:-3306}"

MYSQL_ROOT_USER="${MYSQL_ROOT_USER:-root}"
MYSQL_ROOT_PASSWORD="${MYSQL_ROOT_PASSWORD:-root}"

APP_DB="${APP_DB:-cajero_atm}"
APP_USER="${APP_USER:-cajero_user}"
APP_PASSWORD="${APP_PASSWORD:-cajero_pass}"

REPL_USER="${REPL_USER:-replica_user}"
REPL_PASSWORD="${REPL_PASSWORD:-replica_pass}"

ESTADO="/tmp/cajero_failover_estado"
LOG="/logs/failover-monitor.log"

mkdir -p /logs

if [ ! -f "$ESTADO" ]; then
  echo "normal" > "$ESTADO"
fi

echo "$(date '+%Y-%m-%d %H:%M:%S') monitor docker iniciado" >> "$LOG"

while true; do
  if mysql -h "$PRIMARY_HOST" -P "$MYSQL_PORT" -u "$APP_USER" -p"$APP_PASSWORD" -e "SELECT 1;" >/dev/null 2>&1; then

    if grep -q "failover" "$ESTADO"; then
      echo "$(date '+%Y-%m-%d %H:%M:%S') primary regreso se inicia failback automatico" >> "$LOG"

      sleep 10

      echo "$(date '+%Y-%m-%d %H:%M:%S') sincronizando secondary hacia primary" >> "$LOG"

      mysqldump \
        -h "$SECONDARY_HOST" \
        -P "$MYSQL_PORT" \
        -u "$APP_USER" \
        -p"$APP_PASSWORD" \
        --single-transaction \
        --set-gtid-purged=OFF \
        "$APP_DB" > /tmp/cajero_failback.sql

      mysql \
        -h "$PRIMARY_HOST" \
        -P "$MYSQL_PORT" \
        -u "$APP_USER" \
        -p"$APP_PASSWORD" \
        "$APP_DB" < /tmp/cajero_failback.sql

      echo "$(date '+%Y-%m-%d %H:%M:%S') reactivando replica primary hacia secondary" >> "$LOG"

      mysql -h "$PRIMARY_HOST" -P "$MYSQL_PORT" -u "$MYSQL_ROOT_USER" -p"$MYSQL_ROOT_PASSWORD" -e "
CREATE USER IF NOT EXISTS '$REPL_USER'@'%' IDENTIFIED BY '$REPL_PASSWORD';
GRANT REPLICATION SLAVE, REPLICATION CLIENT ON *.* TO '$REPL_USER'@'%';
FLUSH PRIVILEGES;
"

      mysql -h "$SECONDARY_HOST" -P "$MYSQL_PORT" -u "$MYSQL_ROOT_USER" -p"$MYSQL_ROOT_PASSWORD" -e "
SET GLOBAL super_read_only=OFF;
SET GLOBAL read_only=OFF;
STOP REPLICA;
RESET REPLICA ALL;
CHANGE REPLICATION SOURCE TO
  SOURCE_HOST='$PRIMARY_HOST',
  SOURCE_PORT=$MYSQL_PORT,
  SOURCE_USER='$REPL_USER',
  SOURCE_PASSWORD='$REPL_PASSWORD',
  SOURCE_AUTO_POSITION=1,
  GET_SOURCE_PUBLIC_KEY=1;
START REPLICA;
"

      mysql -h "$SECONDARY_HOST" -P "$MYSQL_PORT" -u "$MYSQL_ROOT_USER" -p"$MYSQL_ROOT_PASSWORD" -e "SHOW REPLICA STATUS\G" | grep -E "Replica_IO_Running|Replica_SQL_Running|Last_IO_Error|Last_SQL_Error" >> "$LOG"

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
