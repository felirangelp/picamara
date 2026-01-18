#!/usr/bin/expect -f
# Script robusto para iniciar servidor en Raspberry Pi

set IP [lindex $argv 0]
set USER [lindex $argv 1]
set PASS [lindex $argv 2]
set timeout 30

if {$IP == ""} { set IP "192.168.1.50" }
if {$USER == ""} { set USER "picamara" }
if {$PASS == ""} { set PASS "picamara" }

puts "============================================================"
puts "🚀 INICIANDO SERVIDOR (MODO ROBUSTO)"
puts "============================================================"
puts ""

# Detener procesos anteriores
puts "1. Deteniendo procesos anteriores..."
spawn ssh -o StrictHostKeyChecking=no $USER@$IP "pkill -f 'python.*run.py' 2>/dev/null; pkill -f uvicorn 2>/dev/null; sleep 3; echo 'OK'"
expect {
    "password:" {
        send "$PASS\r"
        exp_continue
    }
    eof
}

# Iniciar servidor con disown para que quede corriendo
puts ""
puts "2. Iniciando servidor..."
spawn ssh -o StrictHostKeyChecking=no $USER@$IP "cd ~/Pi_camara && nohup ./venv/bin/python3 run.py > logs/server.log 2>&1 & disown; sleep 5; echo 'Servidor iniciado'"
expect {
    "password:" {
        send "$PASS\r"
        exp_continue
    }
    eof
}

puts ""
puts "Esperando 30 segundos para inicio completo..."
sleep 30

# Verificar
puts ""
puts "3. Verificando proceso..."
spawn ssh -o StrictHostKeyChecking=no $USER@$IP "ps aux | grep 'python.*run.py' | grep -v grep"
expect {
    "password:" {
        send "$PASS\r"
        exp_continue
    }
    eof
}

puts ""
puts "4. Verificando puerto..."
spawn ssh -o StrictHostKeyChecking=no $USER@$IP "ss -tuln | grep :5000"
expect {
    "password:" {
        send "$PASS\r"
        exp_continue
    }
    eof
}

puts ""
puts "5. Probando API..."
spawn ssh -o StrictHostKeyChecking=no $USER@$IP "curl -s http://localhost:5000/api/status 2>&1 | head -5"
expect {
    "password:" {
        send "$PASS\r"
        exp_continue
    }
    eof
}

puts ""
puts "6. Revisando logs recientes..."
spawn ssh -o StrictHostKeyChecking=no $USER@$IP "tail -20 ~/Pi_camara/logs/server.log 2>&1 | tail -10"
expect {
    "password:" {
        send "$PASS\r"
        exp_continue
    }
    eof
}

puts ""
puts "============================================================"
puts "✅ SERVIDOR INICIADO"
puts "============================================================"
puts ""
puts "Accede a: http://$IP:5000"
puts ""
