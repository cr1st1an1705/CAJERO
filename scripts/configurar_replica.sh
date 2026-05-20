#!/usr/bin/env bash
set -e

echo "configurando replica real primary hacia secondary"

cd "$(dirname "$0")/.."

echo "1. verificando contenedores"
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep mysql

echo "2. creando usuario de replicacion en primary desde sql"
docker exec -i mysql-primary-cajero mysql -uroot -proot < database/sql/02_replication_user.sql

echo "3. copiando datos actuales de primary hacia secondary"
docker exec mysql-primary-cajero mysqldump -uroot -proot --single-transaction --set-gtid-purged=OFF --databases cajero_atm > /tmp/cajero_atm_dump.sql

echo "3.1 desactivando modo solo lectura en secondary para restaurar datos"
docker exec mysql-secondary-cajero mysql -uroot -proot -e "SET GLOBAL super_read_only=OFF; SET GLOBAL read_only=OFF;"

docker exec -i mysql-secondary-cajero mysql -uroot -proot < /tmp/cajero_atm_dump.sql

echo "4. activando replica en secondary desde sql"
docker exec -i mysql-secondary-cajero mysql -uroot -proot < database/sql/03_configurar_replica.sql | grep -E "Replica_IO_Running|Replica_SQL_Running|Last_IO_Error|Last_SQL_Error" || true

echo "replica configurada"
