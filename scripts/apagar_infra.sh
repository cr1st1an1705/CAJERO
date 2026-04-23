#!/usr/bin/env bash
set -e
cd "$(dirname "$0")/.."
sudo docker compose -f docker/docker-compose.yml down
