#!/bin/bash
# Script de monitoreo para mantener el servidor corriendo

IP="${1:-192.168.1.50}"
USER="${2:-picamara}"
PASS="${3:-picamara}"

echo "============================================================"
echo "🔍 MONITOREANDO SERVIDOR"
echo "============================================================"

# Verificar si el servidor está corriendo
if ssh -o StrictHostKeyChecking=no "$USER@$IP" "ps aux | grep 'python.*run.py' | grep -v grep" > /dev/null 2>&1; then
    echo "✅ Servidor corriendo"
    exit 0
else
    echo "⚠️  Servidor no está corriendo, reiniciando..."
    ./scripts/start_server_robust.sh "$IP" "$USER" "$PASS"
    exit $?
fi
