#!/bin/bash
# Script para esperar a que la Raspberry Pi esté disponible y luego instalar el servicio

IP="${1:-picamara.local}"
USER="${2:-picamara}"
PASS="${3:-picamara}"
MAX_ATTEMPTS=60  # Intentar por 5 minutos (60 intentos x 5 segundos)
ATTEMPT=0

echo "============================================================"
echo "⏳ ESPERANDO A QUE LA RASPBERRY PI ESTÉ DISPONIBLE"
echo "============================================================"
echo "IP: $IP"
echo "Usuario: $USER"
echo "Intentando cada 5 segundos (máximo $MAX_ATTEMPTS intentos)..."
echo ""

while [ $ATTEMPT -lt $MAX_ATTEMPTS ]; do
    ATTEMPT=$((ATTEMPT + 1))
    echo -n "Intento $ATTEMPT/$MAX_ATTEMPTS: "
    
    # Intentar conectar
    if timeout 3 ssh -o StrictHostKeyChecking=no -o ConnectTimeout=2 "$USER@$IP" "echo 'OK'" >/dev/null 2>&1; then
        echo "✅ Raspberry Pi está disponible!"
        echo ""
        echo "============================================================"
        echo "🚀 INSTALANDO SERVICIO SYSTEMD"
        echo "============================================================"
        echo ""
        
        # Ejecutar script de instalación
        SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
        "$SCRIPT_DIR/install_service_pi.sh" "$IP" "$USER" "$PASS"
        exit $?
    else
        echo "⏳ No disponible aún, esperando 5 segundos..."
        sleep 5
    fi
done

echo ""
echo "❌ Timeout: La Raspberry Pi no está disponible después de $MAX_ATTEMPTS intentos"
echo "   Por favor, verifica que:"
echo "   1. La Raspberry Pi esté encendida"
echo "   2. Esté conectada a la red"
echo "   3. La IP sea correcta: $IP"
echo ""
exit 1
