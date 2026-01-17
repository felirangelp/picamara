#!/usr/bin/expect -f
# Script watchdog para mantener el servidor corriendo

set IP [lindex $argv 0]
set USER [lindex $argv 1]
set PASS [lindex $argv 2]
set timeout 20

if {$IP == ""} { set IP "192.168.1.50" }
if {$USER == ""} { set USER "picamara" }
if {$PASS == ""} { set PASS "picamara" }

puts "Verificando servidor..."
spawn ssh -o StrictHostKeyChecking=no $USER@$IP "ps aux | grep 'python.*run.py' | grep -v grep"
expect {
    "password:" {
        send "$PASS\r"
        exp_continue
    }
    "python" {
        puts "✅ Servidor corriendo"
    }
    eof {
        puts "⚠️  Servidor no está corriendo, reiniciando..."
        spawn ssh -o StrictHostKeyChecking=no $USER@$IP "cd ~/Pi_camara && nohup ./venv/bin/python3 run.py > logs/server.log 2>&1 &"
        expect {
            "password:" {
                send "$PASS\r"
                exp_continue
            }
            eof
        }
        puts "✅ Servidor reiniciado"
    }
}
