#!/usr/bin/expect -f
# Verificar modelo exacto de cámara conectada

set IP [lindex $argv 0]
set USER [lindex $argv 1]
set PASS [lindex $argv 2]

if {$IP == ""} { set IP "picamara.local" }
if {$USER == ""} { set USER "picamara" }
if {$PASS == ""} { set PASS "picamara" }

set timeout 10

puts "============================================================"
puts "📷 VERIFICANDO MODELO DE CÁMARA"
puts "============================================================"
puts ""

# Método 1: vcgencmd
puts "1. Información de cámara (vcgencmd):"
spawn ssh $USER@$IP "vcgencmd get_camera"
expect {
    "password:" {
        send "$PASS\r"
        exp_continue
    }
    eof
}

puts ""
puts "2. Información de libcamera:"
spawn ssh $USER@$IP "python3 << 'PYTHON_EOF'
from picamera2 import Picamera2
camera = Picamera2()
camera_info = camera.camera_properties
print('Modelo detectado:', camera_info.get('Model', 'N/A'))
print('Sensor:', camera_info.get('SensorModel', 'N/A'))
for key, value in camera_info.items():
    if 'model' in key.lower() or 'sensor' in key.lower():
        print(f'{key}: {value}')
PYTHON_EOF
"
expect {
    "password:" {
        send "$PASS\r"
        exp_continue
    }
    eof
}

puts ""
puts "3. Listando cámaras disponibles:"
spawn ssh $USER@$IP "python3 << 'PYTHON_EOF'
from picamera2 import Picamera2
camera = Picamera2()
available_cameras = camera.camera_manager.cameras
for i, cam in enumerate(available_cameras):
    print(f'Cámara {i}: {cam.id}')
    props = cam.properties
    if 'Model' in props:
        print(f'  Modelo: {props[\"Model\"]}')
    if 'SensorModel' in props:
        print(f'  Sensor: {props[\"SensorModel\"]}')
PYTHON_EOF
"
expect {
    "password:" {
        send "$PASS\r"
        exp_continue
    }
    eof
}

puts ""
puts "============================================================"
puts "✅ Verificación completada"
puts "============================================================"
puts ""
puts "💡 NOTA: Si detecta OV5647 en lugar de IMX219, puede ser:"
puts "   1. Otra cámara conectada"
puts "   2. El sistema detectó otra interfaz"
puts "   3. La IMX219 necesita configuración adicional"
puts ""
puts "   El código debería funcionar con cualquier cámara compatible"
puts "   con picamera2."

exit 0
