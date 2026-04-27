#!/usr/bin/env bash
set -e

echo "Apagando primary real..."
docker stop mysql-primary-cajero

echo "Primary apagado. El backend deberia intentar usar secondary."
echo "Esperando 3 minutos..."
sleep 180

echo "Encendiendo primary otra vez..."
docker start mysql-primary-cajero

echo "Esperando que MySQL primary vuelva a estar listo..."
sleep 20

docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep mysql

echo "Primary encendido otra vez."
