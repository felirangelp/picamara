#!/usr/bin/expect -f
# Script expect para probar conectividad con contraseña

set IP [lindex $argv 0]
set USER [lindex $argv 1]
set PASS [lindex $argv 2]

if {$IP == ""} { set IP "picamara.local" }
if {$USER == ""} { set USER "picamara" }
if {$PASS == ""} { set PASS "picamara" }

set timeout 10

puts "============================================================"
puts "🧪 PRUEBAS DE CONECTIVIDAD - RASPBERRY PI"
puts "============================================================"
puts "IP: $IP"
puts "Usuario: $USER"
puts "============================================================"
puts ""

# Prueba 1: Conexión SSH
puts "============================================================"
puts "🔌 Probando conexión SSH..."
puts "============================================================"

spawn ssh -o StrictHostKeyChecking=no $USER@$IP "echo 'SSH_OK'"
expect {
    "password:" {
        send "$PASS\r"
        exp_continue
    }
    "SSH_OK" {
        puts "✅ Conexión SSH exitosa"
        set SSH_OK 1
    }
    timeout {
        puts "❌ Timeout en conexión SSH"
        exit 1
    }
    "Permission denied" {
        puts "❌ Error de autenticación SSH"
        exit 1
    }
}

# Prueba 2: Detección de cámara
puts ""
puts "============================================================"
puts "📷 Probando detección de cámara..."
puts "============================================================"

spawn ssh $USER@$IP "libcamera-hello --list-cameras"
expect {
    "password:" {
        send "$PASS\r"
        exp_continue
    }
    "imx219" {
        puts "✅ Cámara IMX219 detectada"
        set CAMERA_OK 1
    }
    "camera" {
        puts "✅ Cámara detectada"
        set CAMERA_OK 1
    }
    timeout {
        puts "⚠️  Timeout o cámara no detectada"
        set CAMERA_OK 0
    }
}

# Prueba 3: picamera2
puts ""
puts "============================================================"
puts "🐍 Probando picamera2..."
puts "============================================================"

spawn ssh $USER@$IP "python3 -c 'import picamera2; print(\"OK\")'"
expect {
    "password:" {
        send "$PASS\r"
        exp_continue
    }
    "OK" {
        puts "✅ picamera2 disponible"
        set PICAMERA_OK 1
    }
    "No module named" {
        puts "❌ picamera2 no instalado"
        puts "   Instalar: sudo apt install python3-picamera2"
        set PICAMERA_OK 0
    }
    timeout {
        puts "⚠️  Timeout"
        set PICAMERA_OK 0
    }
}

# Prueba 4: Proyecto
puts ""
puts "============================================================"
puts "📁 Verificando proyecto..."
puts "============================================================"

spawn ssh $USER@$IP "test -d ~/Pi_camara && echo 'EXISTS' || echo 'NOT_FOUND'"
expect {
    "password:" {
        send "$PASS\r"
        exp_continue
    }
    "EXISTS" {
        puts "✅ Proyecto encontrado en ~/Pi_camara"
    }
    "NOT_FOUND" {
        puts "⚠️  Proyecto no encontrado en ~/Pi_camara"
    }
    timeout {
        puts "⚠️  Timeout"
    }
}

puts ""
puts "============================================================"
puts "📊 RESUMEN"
puts "============================================================"
if {[info exists SSH_OK]} { puts "✅ SSH: OK" } else { puts "❌ SSH: FAIL" }
if {[info exists CAMERA_OK] && $CAMERA_OK} { puts "✅ Cámara: OK" } else { puts "❌ Cámara: FAIL" }
if {[info exists PICAMERA_OK] && $PICAMERA_OK} { puts "✅ picamera2: OK" } else { puts "❌ picamera2: FAIL" }
puts "============================================================"

exit 0
