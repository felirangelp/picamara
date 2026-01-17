#!/usr/bin/expect -f
# Script para iniciar servidor en Raspberry Pi (modo interactivo)

set IP [lindex $argv 0]
set USER [lindex $argv 1]
set PASS [lindex $argv 2]

if {$IP == ""} { set IP "192.168.0.105" }
if {$USER == ""} { set USER "picamara" }
if {$PASS == ""} { set PASS "picamara" }

puts "============================================================"
puts "🚀 INICIANDO SERVIDOR EN RASPBERRY PI"
puts "============================================================"
puts "IP: $IP"
puts "Usuario: $USER"
puts ""
puts "⚠️  NOTA: Este script iniciará el servidor en modo interactivo"
puts "   Para ejecutar en segundo plano, usa systemd service"
puts "============================================================"
puts ""

# Verificar que todo esté listo
spawn ssh $USER@$IP "cd ~/Pi_camara && source venv/bin/activate && python3 -c 'import fastapi; import picamera2; print(\"READY\")'"
expect {
    "password:" {
        send "$PASS\r"
        exp_continue
    }
    "READY" {
        puts "✅ Sistema listo"
    }
    eof
}

puts ""
puts "Iniciando servidor..."
puts "Accede a: http://$IP:5000"
puts ""
puts "Presiona Ctrl+C para detener el servidor"
puts ""

# Iniciar servidor (modo interactivo)
spawn ssh -t $USER@$IP "cd ~/Pi_camara && source venv/bin/activate && python src/main.py"
expect {
    "password:" {
        send "$PASS\r"
        exp_continue
    }
    "Uvicorn running" {
        puts "✅ Servidor iniciado"
    }
    eof
}

exit 0
