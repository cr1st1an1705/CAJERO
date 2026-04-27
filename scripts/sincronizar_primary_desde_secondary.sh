#!/usr/bin/env bash
set -e

echo "Sincronizando primary desde secondary..."

cd "$(dirname "$0")/.."

echo "1. Verificando que ambos contenedores esten activos..."
sudo docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep mysql

echo "2. Creando copia actual desde secondary..."
sudo docker exec mysql-secondary-cajero mysqldump -uroot -proot --single-transaction --set-gtid-purged=OFF --databases cajero_atm > /tmp/cajero_atm_failback.sql

echo "3. Restaurando copia en primary..."
sudo docker exec -i mysql-primary-cajero mysql -uroot -proot < /tmp/cajero_atm_failback.sql

echo "4. Verificando datos en primary..."
mysql -h 127.0.0.1 -P 3307 -u cajero_user -pcajero_pass -e "USE cajero_atm; SELECT COUNT(*) AS cuentas FROM cuentas; SELECT COUNT(*) AS transacciones FROM transacciones; SELECT COUNT(*) AS auditorias FROM auditorias; SELECT numero_cuenta, saldo FROM cuentas;"

echo "5. Verificando datos en secondary..."
mysql -h 127.0.0.1 -P 3308 -u cajero_user -pcajero_pass -e "USE cajero_atm; SELECT COUNT(*) AS cuentas FROM cuentas; SELECT COUNT(*) AS transacciones FROM transacciones; SELECT COUNT(*) AS auditorias FROM auditorias; SELECT numero_cuenta, saldo FROM cuentas;"

echo "Sincronizacion secondary -> primary finalizada."
