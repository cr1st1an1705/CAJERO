#!/usr/bin/env bash
set -e

echo "Configurando replica real primary -> secondary..."

cd "$(dirname "$0")/.."

echo "1. Verificando contenedores..."
sudo docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep mysql

echo "2. Creando usuario de replicacion en primary..."
sudo docker exec mysql-primary-cajero mysql -uroot -proot -e "
CREATE USER IF NOT EXISTS 'replica_user'@'%' IDENTIFIED BY 'replica_pass';
GRANT REPLICATION SLAVE, REPLICATION CLIENT ON *.* TO 'replica_user'@'%';
FLUSH PRIVILEGES;
"

echo "3. Copiando datos actuales de primary hacia secondary..."
sudo docker exec mysql-primary-cajero mysqldump -uroot -proot --single-transaction --set-gtid-purged=OFF --databases cajero_atm > /tmp/cajero_atm_dump.sql
sudo docker exec -i mysql-secondary-cajero mysql -uroot -proot < /tmp/cajero_atm_dump.sql

echo "4. Activando replicacion en secondary..."
sudo docker exec mysql-secondary-cajero mysql -uroot -proot -e "
STOP REPLICA;
RESET REPLICA ALL;
CHANGE REPLICATION SOURCE TO
  SOURCE_HOST='mysql-primary',
  SOURCE_PORT=3306,
  SOURCE_USER='replica_user',
  SOURCE_PASSWORD='replica_pass',
  SOURCE_AUTO_POSITION=1,
  GET_SOURCE_PUBLIC_KEY=1;
START REPLICA;
"

echo "5. Estado de replica:"
sudo docker exec mysql-secondary-cajero mysql -uroot -proot -e "SHOW REPLICA STATUS\G" | grep -E "Replica_IO_Running|Replica_SQL_Running|Last_IO_Error|Last_SQL_Error"

echo "Replica configurada."
