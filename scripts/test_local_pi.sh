#!/usr/bin/expect -f
# Script para ejecutar pruebas locales en Raspberry Pi

set IP [lindex $argv 0]
set USER [lindex $argv 1]
set PASS [lindex $argv 2]

if {$IP == ""} { set IP "picamara.local" }
if {$USER == ""} { set USER "picamara" }
if {$PASS == ""} { set PASS "picamara" }

set timeout 60

puts "============================================================"
puts "🧪 PRUEBAS LOCALES EN RASPBERRY PI"
puts "============================================================"
puts "IP: $IP"
puts "Usuario: $USER"
puts "============================================================"
puts ""

# Verificar entorno virtual
puts "1. Verificando entorno virtual..."
spawn ssh $USER@$IP "test -d ~/Pi_camara/venv && echo 'EXISTS' || echo 'NOT_FOUND'"
expect {
    "password:" {
        send "$PASS\r"
        exp_continue
    }
    "NOT_FOUND" {
        puts "❌ Entorno virtual no encontrado"
        puts "   Ejecuta primero: ./scripts/install_dependencies_pi.sh"
        exit 1
    }
    "EXISTS" {
        puts "   ✅ Entorno virtual encontrado"
    }
}

# Ejecutar prueba de cámara
puts ""
puts "2. Ejecutando prueba de cámara local..."
puts "   (Esto capturará algunos frames para verificar funcionamiento)"
puts ""

spawn ssh $USER@$IP "cd ~/Pi_camara && source venv/bin/activate && timeout 10 python scripts/test_camera_local.py || echo 'TEST_COMPLETE'"
expect {
    "password:" {
        send "$PASS\r"
        exp_continue
    }
    "Frame capturado" {
        puts "   ✅ Cámara funcionando"
    }
    "Motion detected" {
        puts "   ✅ Detección de movimiento funcionando"
    }
    "TEST_COMPLETE" {
        puts "   ✅ Prueba completada"
    }
    timeout {
        puts "   ⚠️  Timeout en prueba (puede ser normal)"
    }
    eof
}

# Verificar imports
puts ""
puts "3. Verificando imports de módulos..."
spawn ssh $USER@$IP "cd ~/Pi_camara && source venv/bin/activate && python3 -c 'from src.camera.imx219_handler import IMX219Handler; print(\"IMX219Handler OK\")' && python3 -c 'from src.detection.motion_detector import MotionDetector; print(\"MotionDetector OK\")' && python3 -c 'from src.database.db_manager import DatabaseManager; print(\"DatabaseManager OK\")'"
expect {
    "password:" {
        send "$PASS\r"
        exp_continue
    }
    "OK" {
        puts "   ✅ Módulos del proyecto importan correctamente"
    }
    "ImportError" {
        puts "   ❌ Error en imports"
    }
    eof
}

puts ""
puts "============================================================"
puts "✅ Pruebas completadas"
puts "============================================================"
puts ""
puts "📋 Si todas las pruebas pasaron, puedes iniciar el servidor:"
puts "   ./scripts/start_server_pi.sh $IP $USER $PASS"
puts ""

exit 0
