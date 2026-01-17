#!/usr/bin/expect -f
# Script para actualizar código en Raspberry Pi desde GitHub

set IP [lindex $argv 0]
set USER [lindex $argv 1]
set PASS [lindex $argv 2]

if {$IP == ""} { set IP "192.168.1.50" }
if {$USER == ""} { set USER "picamara" }
if {$PASS == ""} { set PASS "picamara" }

set timeout 30

puts "============================================================"
puts "📥 ACTUALIZANDO CÓDIGO EN RASPBERRY PI DESDE GITHUB"
puts "============================================================"
puts "IP: $IP"
puts "Usuario: $USER"
puts "============================================================"
puts ""

# Verificar que el proyecto existe
puts "1. Verificando proyecto..."
spawn ssh -o StrictHostKeyChecking=no $USER@$IP "test -d ~/Pi_camara && echo 'EXISTS' || echo 'NOT_FOUND'"
expect {
    "password:" {
        send "$PASS\r"
        exp_continue
    }
    "NOT_FOUND" {
        puts "❌ Proyecto no encontrado. Clonando desde GitHub..."
        spawn ssh -o StrictHostKeyChecking=no $USER@$IP "cd ~ && git clone https://github.com/felirangelp/picamara.git Pi_camara"
        expect {
            "password:" {
                send "$PASS\r"
                exp_continue
            }
            eof
        }
    }
    "EXISTS" {
        puts "   ✅ Proyecto encontrado"
    }
    eof
}

# Verificar si es un repositorio Git
puts ""
puts "2. Verificando repositorio Git..."
spawn ssh -o StrictHostKeyChecking=no $USER@$IP "cd ~/Pi_camara && git status > /dev/null 2>&1 && echo 'GIT_OK' || echo 'NOT_GIT'"
expect {
    "password:" {
        send "$PASS\r"
        exp_continue
    }
    "NOT_GIT" {
        puts "   ⚠️  No es un repositorio Git. Inicializando..."
        spawn ssh -o StrictHostKeyChecking=no $USER@$IP "cd ~/Pi_camara && git init && git remote add origin https://github.com/felirangelp/picamara.git && git fetch && git checkout -b main origin/main 2>&1 || git branch -M main && git pull origin main"
        expect {
            "password:" {
                send "$PASS\r"
                exp_continue
            }
            eof
        }
    }
    "GIT_OK" {
        puts "   ✅ Repositorio Git configurado"
    }
    eof
}

# Actualizar desde GitHub
puts ""
puts "3. Actualizando código desde GitHub..."
spawn ssh -o StrictHostKeyChecking=no $USER@$IP "cd ~/Pi_camara && git fetch origin && git pull origin main"
expect {
    "password:" {
        send "$PASS\r"
        exp_continue
    }
    "Already up to date" {
        puts "   ✅ Código ya está actualizado"
    }
    "Updating" {
        puts "   ✅ Código actualizado"
    }
    eof
}

# Verificar cambios
puts ""
puts "4. Verificando estado..."
spawn ssh -o StrictHostKeyChecking=no $USER@$IP "cd ~/Pi_camara && git log --oneline -1"
expect {
    "password:" {
        send "$PASS\r"
        exp_continue
    }
    eof
}

puts ""
puts "============================================================"
puts "✅ ACTUALIZACIÓN COMPLETADA"
puts "============================================================"
puts ""
puts "Si el servidor está corriendo, reinícialo:"
puts "  ssh $USER@$IP 'pkill -f run.py && cd ~/Pi_camara && nohup ./venv/bin/python3 run.py > logs/server.log 2>&1 &'"
puts "============================================================"
