#!/bin/bash
# Script helper para probar con IP específica

if [ -z "$1" ]; then
    echo "Uso: $0 <IP_RASPBERRY_PI>"
    echo ""
    echo "Ejemplo:"
    echo "  $0 192.168.1.100"
    echo ""
    echo "Para obtener la IP de la Raspberry Pi:"
    echo "  En la Pi: hostname -I"
    echo "  O desde el router: buscar dispositivo 'raspberrypi'"
    exit 1
fi

IP=$1
echo "🧪 Ejecutando pruebas con IP: $IP"
echo ""

cd "$(dirname "$0")/.."
source venv/bin/activate
python scripts/test_raspberry_connection.py --host "$IP" --user picamara
