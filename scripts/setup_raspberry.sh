#!/bin/bash
# Script de configuración inicial de Raspberry Pi

set -e

echo "=== Configuración de Raspberry Pi para Sistema de Seguridad ==="

# Actualizar sistema
echo "Actualizando sistema..."
sudo apt update
sudo apt upgrade -y

# Instalar dependencias del sistema
echo "Instalando dependencias del sistema..."
sudo apt install -y \
    python3-pip \
    python3-venv \
    git \
    libcamera-dev \
    libopencv-dev \
    python3-opencv \
    build-essential \
    cmake \
    pkg-config

# Instalar picamera2
echo "Instalando picamera2..."
sudo apt install -y python3-picamera2

# Crear directorios
echo "Creando directorios..."
mkdir -p ~/Pi_camara/data/{videos,episodes,models}
mkdir -p ~/Pi_camara/logs

echo "=== Configuración completada ==="
echo "Siguiente paso:"
echo "1. cd ~/Pi_camara"
echo "2. python3 -m venv venv"
echo "3. source venv/bin/activate"
echo "4. pip install -r requirements.txt"
