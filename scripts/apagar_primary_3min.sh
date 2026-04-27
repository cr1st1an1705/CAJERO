#!/usr/bin/env bash
set -e

echo "Apagando primary real..."
sudo docker stop mysql-primary-cajero

echo "Primary apagado. El backend deberia intentar usar secondary."
echo "Esperando 3 minutos..."
sleep 180

echo "Encendiendo primary otra vez..."
sudo docker start mysql-primary-cajero

echo "Esperando que MySQL primary vuelva a estar listo..."
sleep 20

sudo docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep mysql

echo "Primary encendido otra vez."
