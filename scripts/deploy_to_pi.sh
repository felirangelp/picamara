#!/usr/bin/expect -f
# Script para transferir proyecto a Raspberry Pi usando rsync

set IP [lindex $argv 0]
set USER [lindex $argv 1]
set PASS [lindex $argv 2]
set LOCAL_PATH [lindex $argv 3]

if {$IP == ""} { set IP "picamara.local" }
if {$USER == ""} { set USER "picamara" }
if {$PASS == ""} { set PASS "picamara" }
if {$LOCAL_PATH == ""} { 
    set LOCAL_PATH [exec pwd]
}

set timeout 30

puts "============================================================"
puts "📦 TRANSFERENCIA DE PROYECTO A RASPBERRY PI"
puts "============================================================"
puts "IP: $IP"
puts "Usuario: $USER"
puts "Origen: $LOCAL_PATH"
puts "Destino: ~/Pi_camara"
puts "============================================================"
puts ""

# Verificar que rsync esté disponible
if {[catch {exec which rsync} result]} {
    puts "❌ rsync no está instalado"
    puts "   Instalar: brew install rsync (Mac) o sudo apt install rsync (Linux)"
    exit 1
}

# Crear directorio en la Pi si no existe
puts "1. Creando directorio en Raspberry Pi..."
spawn ssh $USER@$IP "mkdir -p ~/Pi_camara"
expect {
    "password:" {
        send "$PASS\r"
        exp_continue
    }
    eof
}

# Transferir archivos con rsync
puts ""
puts "2. Transfiriendo archivos (esto puede tardar varios minutos)..."
puts "   Excluyendo: venv/, __pycache__/, .git/, data/videos/, data/episodes/"

spawn rsync -avz --progress \
    --exclude 'venv' \
    --exclude '__pycache__' \
    --exclude '*.pyc' \
    --exclude '.git' \
    --exclude 'data/videos' \
    --exclude 'data/episodes' \
    --exclude 'data/models' \
    --exclude '.DS_Store' \
    --exclude '*.log' \
    "$LOCAL_PATH/" $USER@$IP:~/Pi_camara/

expect {
    "password:" {
        send "$PASS\r"
        exp_continue
    }
    "total size" {
        puts "   ✅ Transferencia completada"
    }
    timeout {
        puts "   ⚠️  Timeout, pero la transferencia puede continuar en segundo plano"
    }
    eof
}

# Verificar transferencia
puts ""
puts "3. Verificando archivos transferidos..."
spawn ssh $USER@$IP "ls -la ~/Pi_camara/ | head -10"
expect {
    "password:" {
        send "$PASS\r"
        exp_continue
    }
    eof
}

puts ""
puts "============================================================"
puts "✅ Transferencia completada"
puts "============================================================"
puts ""
puts "📋 Próximos pasos:"
puts "   1. Ejecutar: ./scripts/install_dependencies_pi.sh $IP $USER $PASS"
puts "   2. O manualmente:"
puts "      ssh $USER@$IP"
puts "      cd ~/Pi_camara"
puts "      python3 -m venv venv"
puts "      source venv/bin/activate"
puts "      pip install -r requirements.txt"
puts ""

exit 0
