#!/usr/bin/expect -f
# Script para instalar el servicio systemd en Raspberry Pi

set IP [lindex $argv 0]
set USER [lindex $argv 1]
set PASS [lindex $argv 2]
set timeout 30

if {$IP == ""} { set IP "192.168.1.50" }
if {$USER == ""} { set USER "picamara" }
if {$PASS == ""} { set PASS "picamara" }

puts "============================================================"
puts "🔧 INSTALANDO SERVICIO SYSTEMD PARA INICIO AUTOMÁTICO"
puts "============================================================"
puts "IP: $IP"
puts "Usuario: $USER"
puts "============================================================"
puts ""

# 1. Verificar que el archivo de servicio existe
puts "1. Verificando archivo de servicio..."
spawn ssh -o StrictHostKeyChecking=no $USER@$IP "test -f ~/Pi_camara/systemd/pi-camera.service && echo 'OK' || echo 'ERROR'"
expect {
    "password:" {
        send "$PASS\r"
        exp_continue
    }
    "OK" {
        puts "   ✅ Archivo de servicio encontrado"
    }
    "ERROR" {
        puts "   ❌ Archivo de servicio NO encontrado"
        exit 1
    }
    eof
}

# 2. Detener cualquier proceso anterior del servidor
puts ""
puts "2. Deteniendo procesos anteriores..."
spawn ssh -o StrictHostKeyChecking=no $USER@$IP "pkill -9 -f 'python.*run.py' 2>/dev/null; pkill -9 -f uvicorn 2>/dev/null; sleep 2; echo 'OK'"
expect {
    "password:" {
        send "$PASS\r"
        exp_continue
    }
    eof
}

# 3. Copiar servicio a systemd
puts ""
puts "3. Copiando servicio a /etc/systemd/system/..."
spawn ssh -o StrictHostKeyChecking=no $USER@$IP "sudo cp ~/Pi_camara/systemd/pi-camera.service /etc/systemd/system/pi-camera.service && echo 'OK'"
expect {
    "password:" {
        send "$PASS\r"
        exp_continue
    }
    "\[sudo\] password" {
        send "$PASS\r"
        exp_continue
    }
    "OK" {
        puts "   ✅ Servicio copiado"
    }
    eof
}

# 4. Recargar systemd
puts ""
puts "4. Recargando systemd..."
spawn ssh -o StrictHostKeyChecking=no $USER@$IP "sudo systemctl daemon-reload && echo 'OK'"
expect {
    "password:" {
        send "$PASS\r"
        exp_continue
    }
    "\[sudo\] password" {
        send "$PASS\r"
        exp_continue
    }
    "OK" {
        puts "   ✅ systemd recargado"
    }
    eof
}

# 5. Habilitar servicio (inicio automático)
puts ""
puts "5. Habilitando servicio (inicio automático)..."
spawn ssh -o StrictHostKeyChecking=no $USER@$IP "sudo systemctl enable pi-camera.service && echo 'OK'"
expect {
    "password:" {
        send "$PASS\r"
        exp_continue
    }
    "\[sudo\] password" {
        send "$PASS\r"
        exp_continue
    }
    "OK" {
        puts "   ✅ Servicio habilitado para inicio automático"
    }
    eof
}

# 6. Iniciar el servicio ahora
puts ""
puts "6. Iniciando servicio ahora..."
spawn ssh -o StrictHostKeyChecking=no $USER@$IP "sudo systemctl start pi-camera.service && echo 'OK'"
expect {
    "password:" {
        send "$PASS\r"
        exp_continue
    }
    "\[sudo\] password" {
        send "$PASS\r"
        exp_continue
    }
    "OK" {
        puts "   ✅ Servicio iniciado"
    }
    eof
}

# 7. Esperar un momento para que el servicio inicie
puts ""
puts "Esperando 10 segundos para inicio completo..."
sleep 10

# 8. Verificar estado del servicio
puts ""
puts "7. Verificando estado del servicio..."
spawn ssh -o StrictHostKeyChecking=no $USER@$IP "sudo systemctl status pi-camera.service --no-pager | head -15"
expect {
    "password:" {
        send "$PASS\r"
        exp_continue
    }
    "\[sudo\] password" {
        send "$PASS\r"
        exp_continue
    }
    eof {
        # Mostrar lo que se capturó
    }
}

# 9. Verificar que el puerto está escuchando
puts ""
puts "8. Verificando puerto 5000..."
spawn ssh -o StrictHostKeyChecking=no $USER@$IP "ss -tuln | grep :5000"
expect {
    "password:" {
        send "$PASS\r"
        exp_continue
    }
    -regexp "LISTEN.*:5000" {
        puts "   ✅ Puerto 5000 escuchando"
    }
    timeout {
        puts "   ⚠️  Puerto 5000 aún no está escuchando (puede tardar unos segundos más)"
    }
    eof {
        puts "   ⚠️  Puerto 5000 aún no está escuchando (puede tardar unos segundos más)"
    }
}

# 10. Probar API
puts ""
puts "9. Probando API..."
spawn ssh -o StrictHostKeyChecking=no $USER@$IP "curl -s http://localhost:5000/api/status 2>&1 | head -3"
expect {
    "password:" {
        send "$PASS\r"
        exp_continue
    }
    -regexp "camera_active" {
        puts "   ✅ API responde correctamente"
    }
    timeout {
        puts "   ⚠️  API aún no responde (puede tardar unos segundos más)"
    }
    eof {
        puts "   ⚠️  API aún no responde (puede tardar unos segundos más)"
    }
}

puts ""
puts "============================================================"
puts "✅ SERVICIO INSTALADO Y CONFIGURADO"
puts "============================================================"
puts ""
puts "📋 El servidor ahora:"
puts "   • Se iniciará automáticamente al reiniciar la Raspberry Pi"
puts "   • Se reiniciará automáticamente si se cae (Restart=always)"
puts "   • Los logs se guardan en: ~/Pi_camara/logs/server.log"
puts ""
puts "📋 Comandos útiles (ejecutar en la Raspberry Pi):"
puts "   • Ver estado:    sudo systemctl status pi-camera"
puts "   • Ver logs:      sudo journalctl -u pi-camera -f"
puts "   • Reiniciar:     sudo systemctl restart pi-camera"
puts "   • Detener:       sudo systemctl stop pi-camera"
puts "   • Deshabilitar:  sudo systemctl disable pi-camera"
puts ""
puts "🌐 Accede a: http://$IP:5000"
puts ""
exit 0
