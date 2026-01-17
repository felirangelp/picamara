#!/bin/bash
# Script para probar conectividad con contraseña SSH

IP=${1:-192.168.0.105}
USER=${2:-picamara}
PASS=${3:-picamara}

echo "🧪 Probando conectividad con Raspberry Pi"
echo "   IP: $IP"
echo "   Usuario: $USER"
echo ""

# Verificar si sshpass está disponible
if command -v sshpass &> /dev/null; then
    echo "✅ Usando sshpass para autenticación"
    SSHPASS="sshpass -p '$PASS'"
else
    echo "⚠️  sshpass no está instalado"
    echo "   Instalando con: brew install hudochenkov/sshpass/sshpass"
    echo "   O ejecuta las pruebas manualmente con contraseña"
    SSHPASS=""
fi

# Prueba 1: Conexión SSH
echo ""
echo "============================================================"
echo "🔌 Probando conexión SSH..."
echo "============================================================"

if [ -n "$SSHPASS" ]; then
    if eval "$SSHPASS ssh -o StrictHostKeyChecking=no -o ConnectTimeout=5 $USER@$IP 'echo SSH_OK' 2>&1" | grep -q "SSH_OK"; then
        echo "✅ Conexión SSH exitosa"
        SSH_OK=true
    else
        echo "❌ Error en conexión SSH"
        SSH_OK=false
    fi
else
    echo "⚠️  Prueba SSH manual requerida (sin sshpass)"
    echo "   Ejecuta: ssh $USER@$IP"
    SSH_OK=false
fi

if [ "$SSH_OK" = false ]; then
    echo ""
    echo "💡 Para instalar sshpass (Mac):"
    echo "   brew install hudochenkov/sshpass/sshpass"
    echo ""
    echo "💡 O configura SSH keys para acceso sin contraseña:"
    echo "   ssh-copy-id $USER@$IP"
    exit 1
fi

# Prueba 2: Detección de cámara
echo ""
echo "============================================================"
echo "📷 Probando detección de cámara..."
echo "============================================================"

CAMERA_OUTPUT=$(eval "$SSHPASS ssh $USER@$IP 'libcamera-hello --list-cameras' 2>&1")
if echo "$CAMERA_OUTPUT" | grep -qi "imx219\|camera"; then
    echo "✅ Cámara detectada:"
    echo "$CAMERA_OUTPUT" | grep -i "imx219\|camera" | head -3
else
    echo "❌ Cámara no detectada"
    echo "   Salida: $CAMERA_OUTPUT"
fi

# Prueba 3: picamera2
echo ""
echo "============================================================"
echo "🐍 Probando picamera2..."
echo "============================================================"

PICAMERA_OUTPUT=$(eval "$SSHPASS ssh $USER@$IP 'python3 -c \"import picamera2; print(\\\"OK\\\")\"' 2>&1")
if echo "$PICAMERA_OUTPUT" | grep -q "OK"; then
    echo "✅ picamera2 disponible"
else
    echo "❌ picamera2 no disponible"
    echo "   Instalar: sudo apt install python3-picamera2"
fi

# Prueba 4: Proyecto
echo ""
echo "============================================================"
echo "📁 Verificando proyecto..."
echo "============================================================"

PROJECT_CHECK=$(eval "$SSHPASS ssh $USER@$IP 'test -d ~/Pi_camara && echo EXISTS || echo NOT_FOUND' 2>&1")
if echo "$PROJECT_CHECK" | grep -q "EXISTS"; then
    echo "✅ Proyecto encontrado en ~/Pi_camara"
else
    echo "⚠️  Proyecto no encontrado en ~/Pi_camara"
fi

echo ""
echo "============================================================"
echo "✅ Pruebas completadas"
echo "============================================================"
