#!/usr/bin/expect -f
# Prueba detallada de cámara con expect

set IP [lindex $argv 0]
set USER [lindex $argv 1]
set PASS [lindex $argv 2]

if {$IP == ""} { set IP "picamara.local" }
if {$USER == ""} { set USER "picamara" }
if {$PASS == ""} { set PASS "picamara" }

set timeout 15

puts "============================================================"
puts "📷 PRUEBA DETALLADA DE CÁMARA"
puts "============================================================"
puts ""

# Verificar cámara con diferentes métodos
puts "1. Verificando cámara con vcgencmd..."
spawn ssh $USER@$IP "vcgencmd get_camera"
expect {
    "password:" {
        send "$PASS\r"
        exp_continue
    }
    "supported" {
        puts "   ✅ Cámara soportada"
    }
    timeout {
        puts "   ⚠️  No se pudo verificar"
    }
}

puts ""
puts "2. Verificando dispositivo de cámara..."
spawn ssh $USER@$IP "ls -la /dev/video* 2>/dev/null || echo 'NO_VIDEO_DEVICES'"
expect {
    "password:" {
        send "$PASS\r"
        exp_continue
    }
    "/dev/video" {
        puts "   ✅ Dispositivos de video encontrados"
    }
    "NO_VIDEO_DEVICES" {
        puts "   ⚠️  No se encontraron dispositivos /dev/video*"
    }
    timeout {
        puts "   ⚠️  Timeout"
    }
}

puts ""
puts "3. Verificando módulos de cámara cargados..."
spawn ssh $USER@$IP "lsmod | grep -i camera || lsmod | grep -i imx || echo 'NO_CAMERA_MODULES'"
expect {
    "password:" {
        send "$PASS\r"
        exp_continue
    }
    -re "imx|bcm|camera" {
        puts "   ✅ Módulos de cámara detectados"
    }
    "NO_CAMERA_MODULES" {
        puts "   ⚠️  No se encontraron módulos específicos"
    }
    timeout {
        puts "   ⚠️  Timeout"
    }
}

puts ""
puts "4. Probando captura con picamera2..."
spawn ssh $USER@$IP "python3 << 'PYTHON_EOF'
try:
    from picamera2 import Picamera2
    import time
    camera = Picamera2()
    camera.start()
    time.sleep(1)
    frame = camera.capture_array()
    if frame is not None:
        print(f'OK: Frame shape={frame.shape}')
    else:
        print('ERROR: No frame captured')
    camera.stop()
except Exception as e:
    print(f'ERROR: {e}')
PYTHON_EOF
"
expect {
    "password:" {
        send "$PASS\r"
        exp_continue
    }
    "OK:" {
        puts "   ✅ Captura de frame exitosa"
        puts "   $expect_out(buffer)"
    }
    "ERROR:" {
        puts "   ❌ Error en captura"
        puts "   $expect_out(buffer)"
    }
    timeout {
        puts "   ⚠️  Timeout en captura"
    }
}

puts ""
puts "============================================================"
puts "✅ Pruebas completadas"
puts "============================================================"

exit 0
