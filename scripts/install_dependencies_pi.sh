#!/usr/bin/expect -f
# Script para instalar dependencias en Raspberry Pi

set IP [lindex $argv 0]
set USER [lindex $argv 1]
set PASS [lindex $argv 2]

if {$IP == ""} { set IP "192.168.0.105" }
if {$USER == ""} { set USER "picamara" }
if {$PASS == ""} { set PASS "picamara" }

set timeout 300

puts "============================================================"
puts "📦 INSTALACIÓN DE DEPENDENCIAS EN RASPBERRY PI"
puts "============================================================"
puts "IP: $IP"
puts "Usuario: $USER"
puts "============================================================"
puts ""

# Verificar que el proyecto existe
puts "1. Verificando proyecto..."
spawn ssh $USER@$IP "test -d ~/Pi_camara && echo 'EXISTS' || echo 'NOT_FOUND'"
expect {
    "password:" {
        send "$PASS\r"
        exp_continue
    }
    "NOT_FOUND" {
        puts "❌ Proyecto no encontrado en ~/Pi_camara"
        puts "   Ejecuta primero: ./scripts/deploy_to_pi.sh"
        exit 1
    }
    "EXISTS" {
        puts "   ✅ Proyecto encontrado"
    }
}

# Verificar python3-venv
puts ""
puts "2. Verificando python3-venv..."
spawn ssh $USER@$IP "dpkg -l | grep python3-venv || echo 'NOT_INSTALLED'"
expect {
    "password:" {
        send "$PASS\r"
        exp_continue
    }
    "NOT_INSTALLED" {
        puts "   ⚠️  python3-venv no instalado, instalando..."
        spawn ssh $USER@$IP "sudo apt install -y python3-venv python3-full"
        expect {
            "password:" {
                send "$PASS\r"
                exp_continue
            }
            eof
        }
    }
    eof
}

# Crear entorno virtual
puts ""
puts "3. Creando entorno virtual..."
spawn ssh $USER@$IP "cd ~/Pi_camara && rm -rf venv && python3 -m venv venv"
expect {
    "password:" {
        send "$PASS\r"
        exp_continue
    }
    eof
}

# Actualizar pip
puts ""
puts "4. Actualizando pip..."
spawn ssh $USER@$IP "cd ~/Pi_camara && ./venv/bin/pip install --upgrade pip"
expect {
    "password:" {
        send "$PASS\r"
        exp_continue
    }
    "Successfully installed" {
        puts "   ✅ pip actualizado"
    }
    "Requirement already satisfied" {
        puts "   ✅ pip ya está actualizado"
    }
    eof
}

# Instalar dependencias
puts ""
puts "5. Instalando dependencias (esto puede tardar 5-10 minutos)..."
puts "   Por favor, espera..."

spawn ssh $USER@$IP "cd ~/Pi_camara && ./venv/bin/pip install -r requirements.txt"
expect {
    "password:" {
        send "$PASS\r"
        exp_continue
    }
    "Successfully installed" {
        puts "   ✅ Dependencias instaladas"
    }
    "Requirement already satisfied" {
        puts "   ✅ Dependencias ya instaladas"
    }
    timeout {
        puts "   ⚠️  Timeout, pero la instalación puede continuar"
    }
    eof
}

# Verificar instalación
puts ""
puts "6. Verificando instalación..."
spawn ssh $USER@$IP "cd ~/Pi_camara && ./venv/bin/python3 -c 'import fastapi; print(\"FastAPI OK\")' && ./venv/bin/python3 -c 'import picamera2; print(\"picamera2 OK\")' && ./venv/bin/python3 -c 'import cv2; print(\"OpenCV OK\")'"
expect {
    "password:" {
        send "$PASS\r"
        exp_continue
    }
    "OK" {
        puts "   ✅ Módulos principales verificados"
    }
    eof
}

# Crear directorios necesarios
puts ""
puts "7. Creando directorios necesarios..."
spawn ssh $USER@$IP "cd ~/Pi_camara && mkdir -p data/videos data/episodes data/models logs"
expect {
    "password:" {
        send "$PASS\r"
        exp_continue
    }
    eof
}

puts ""
puts "============================================================"
puts "✅ Instalación completada"
puts "============================================================"
puts ""
puts "📋 Próximos pasos:"
puts "   1. Ejecutar pruebas: ./scripts/test_local_pi.sh $IP $USER $PASS"
puts "   2. O iniciar servidor: ./scripts/start_server_pi.sh $IP $USER $PASS"
puts ""

exit 0
