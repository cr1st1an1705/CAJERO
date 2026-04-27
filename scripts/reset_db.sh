#!/usr/bin/env bash
set -e

echo "Reiniciando base de datos del proyecto..."

cd "$(dirname "$0")/.."

sudo docker compose -f docker/docker-compose.yml down -v
sudo docker compose -f docker/docker-compose.yml up -d

echo "Esperando MySQL..."
sleep 20

echo "Contenedores activos:"
sudo docker ps

echo "Probando primary..."
mysql -h 127.0.0.1 -P 3307 -u cajero_user -pcajero_pass -e "USE cajero_atm; SHOW TABLES;"

echo "Probando secondary..."
mysql -h 127.0.0.1 -P 3308 -u cajero_user -pcajero_pass -e "USE cajero_atm; SHOW TABLES;"

echo "Base de datos lista."
