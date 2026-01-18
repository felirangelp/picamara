#!/bin/bash
# Prueba simple de SSH con contraseña usando expect

IP=${1:-picamara.local}
USER=${2:-picamara}
PASS=${3:-picamara}

echo "🧪 Probando SSH a $USER@$IP"
echo ""

# Crear script expect temporal
EXPECT_SCRIPT=$(mktemp)
cat > "$EXPECT_SCRIPT" << EOF
#!/usr/bin/expect -f
set timeout 10
spawn ssh -o StrictHostKeyChecking=no $USER@$IP "echo 'SSH_CONNECTION_OK'"
expect {
    "password:" {
        send "$PASS\r"
        exp_continue
    }
    "SSH_CONNECTION_OK" {
        puts "✅ Conexión SSH exitosa"
        exit 0
    }
    timeout {
        puts "❌ Timeout"
        exit 1
    }
    eof
}
EOF

chmod +x "$EXPECT_SCRIPT"

if command -v expect &> /dev/null; then
    expect -f "$EXPECT_SCRIPT"
    SSH_RESULT=$?
else
    echo "❌ 'expect' no está instalado"
    echo "   Instalar: brew install expect"
    SSH_RESULT=1
fi

rm -f "$EXPECT_SCRIPT"

if [ $SSH_RESULT -eq 0 ]; then
    echo ""
    echo "✅ SSH funciona. Ejecutando pruebas completas..."
    echo ""
    # Ahora podemos ejecutar el script Python con configuración de SSH
    cd "$(dirname "$0")/.."
    source venv/bin/activate
    
    # Configurar SSH para usar expect
    export SSH_ASKPASS_REQUIRE=never
    python scripts/test_raspberry_connection.py --host "$IP" --user "$USER" 2>&1 || {
        echo ""
        echo "💡 Si falla, prueba manualmente:"
        echo "   ssh $USER@$IP"
        echo "   Luego en la Pi ejecuta las pruebas locales"
    }
fi
