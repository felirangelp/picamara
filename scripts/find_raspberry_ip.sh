#!/bin/bash
# Script para encontrar la IP de la Raspberry Pi en la red local

echo "🔍 Buscando Raspberry Pi en la red local..."
echo ""

# Intentar ping a raspberrypi.local
if ping -c 1 raspberrypi.local &>/dev/null; then
    IP=$(ping -c 1 raspberrypi.local | grep -oE '\([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+\)' | tr -d '()')
    echo "✅ Encontrada: raspberrypi.local -> $IP"
    echo "$IP"
    exit 0
fi

# Si no funciona, intentar escanear la red local
echo "⚠️  raspberrypi.local no responde. Intentando escanear red local..."
echo "   (Esto puede tardar unos segundos)"
echo ""

# Obtener rango de red local
GATEWAY=$(route -n get default | grep gateway | awk '{print $2}' 2>/dev/null || ipconfig getifaddr en0 2>/dev/null | cut -d. -f1-3)
if [ -z "$GATEWAY" ]; then
    GATEWAY=$(ip route | grep default | awk '{print $3}' | cut -d. -f1-3)
fi

if [ -z "$GATEWAY" ]; then
    echo "❌ No se pudo determinar el rango de red"
    echo ""
    echo "💡 Por favor, proporciona la IP manualmente:"
    echo "   python scripts/test_raspberry_connection.py --host <IP> --user picamara"
    exit 1
fi

NETWORK="${GATEWAY}.0/24"
echo "📡 Escaneando red: $NETWORK"
echo ""

# Intentar nmap si está disponible
if command -v nmap &> /dev/null; then
    echo "Usando nmap..."
    nmap -sn "$NETWORK" 2>/dev/null | grep -i raspberry | head -1
elif command -v arp &> /dev/null; then
    echo "Usando arp..."
    arp -a | grep -i raspberry | head -1
else
    echo "❌ No se encontraron herramientas de escaneo (nmap, arp)"
    echo ""
    echo "💡 Opciones:"
    echo "   1. Proporciona la IP manualmente"
    echo "   2. En la Raspberry Pi, ejecuta: hostname -I"
    exit 1
fi

echo ""
echo "💡 Si no aparece nada, proporciona la IP manualmente:"
echo "   python scripts/test_raspberry_connection.py --host <IP> --user picamara"
