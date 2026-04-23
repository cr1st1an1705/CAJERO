COMANDOS UBUNTU USADOS EN EL PROYECTO

sudo apt-get update
- Actualiza indices de paquetes

sudo apt-get install -y python3 python3-venv python3-pip curl ca-certificates git
- Instala Python, entorno virtual y herramientas base

sudo apt-get install -y docker.io
- Instala Docker

sudo apt-get install -y docker-compose-plugin
- Instala plugin docker compose

sudo systemctl enable --now docker
- Inicia Docker y lo deja activo al arrancar el sistema

python3 -m venv .venv
- Crea entorno virtual

source .venv/bin/activate
- Activa entorno virtual

pip install -r requirements.txt
- Instala dependencias del backend

sudo docker compose -f docker/docker-compose.yml up -d
- Levanta MySQL primary y secondary

sudo docker compose -f docker/docker-compose.yml down
- Baja contenedores

uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
- Levanta el backend

Observacion
- Si docker compose no funciona como plugin, probar:
  sudo docker-compose -f docker/docker-compose.yml up -d
