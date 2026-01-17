#!/bin/bash
# Script para instalar el servicio systemd

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
SERVICE_FILE="$PROJECT_DIR/systemd/pi-camera.service"

echo "=== Instalando servicio systemd ==="

# Verificar que el archivo de servicio existe
if [ ! -f "$SERVICE_FILE" ]; then
    echo "Error: No se encuentra $SERVICE_FILE"
    exit 1
fi

# Copiar servicio a systemd
echo "Copiando servicio a /etc/systemd/system/..."
sudo cp "$SERVICE_FILE" /etc/systemd/system/pi-camera.service

# Ajustar rutas en el servicio (si es necesario)
PROJECT_DIR_ABS=$(realpath "$PROJECT_DIR")
sudo sed -i "s|/home/pi/Pi_camara|$PROJECT_DIR_ABS|g" /etc/systemd/system/pi-camera.service

# Recargar systemd
echo "Recargando systemd..."
sudo systemctl daemon-reload

# Habilitar servicio
echo "Habilitando servicio..."
sudo systemctl enable pi-camera.service

echo "=== Servicio instalado ==="
echo "Comandos útiles:"
echo "  Iniciar:   sudo systemctl start pi-camera"
echo "  Detener:   sudo systemctl stop pi-camera"
echo "  Estado:    sudo systemctl status pi-camera"
echo "  Logs:      sudo journalctl -u pi-camera -f"
