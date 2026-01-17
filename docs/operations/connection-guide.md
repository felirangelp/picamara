# Guía de Conexión Remota a Raspberry Pi

## Acceso Remoto al Sistema de Seguridad

Esta guía explica cómo conectarte remotamente a tu Raspberry Pi para monitorear y controlar el sistema de seguridad.

---

## 1. Conexión SSH

### 1.1 Encontrar la IP de tu Raspberry Pi

**Desde la Raspberry Pi** (si tienes acceso físico):
```bash
hostname -I
```

**Desde tu computadora** (en la misma red):
```bash
# Linux/Mac
ping raspberrypi.local

# O escanear la red
nmap -sn 192.168.1.0/24 | grep -B 2 "Raspberry"
```

**Desde el router**:
- Accede a la interfaz de administración de tu router
- Busca en la lista de dispositivos conectados
- Identifica "raspberrypi" o el nombre que configuraste

### 1.2 Conectar vía SSH

**Conexión básica**:
```bash
ssh pi@<IP_RASPBERRY_PI>
# O con el usuario que configuraste:
ssh <usuario>@<IP_RASPBERRY_PI>
```

**Primera conexión**: Acepta la clave SSH escribiendo `yes`.

### 1.3 Configurar SSH Keys (Acceso Sin Contraseña)

**En tu computadora local**:

```bash
# Generar clave SSH (si no tienes una)
ssh-keygen -t ed25519 -C "tu_email@example.com"

# Copiar clave a Raspberry Pi
ssh-copy-id pi@<IP_RASPBERRY_PI>
```

Ahora podrás conectarte sin escribir contraseña.

### 1.4 Configurar Alias SSH (Opcional)

Edita `~/.ssh/config` en tu computadora:

```
Host pi
    HostName <IP_RASPBERRY_PI>
    User pi
    IdentityFile ~/.ssh/id_ed25519
```

Ahora puedes conectarte simplemente con:
```bash
ssh pi
```

---

## 2. Acceso Web

### 2.1 Acceso Local

Una vez que el sistema esté corriendo, abre tu navegador y visita:

```
http://<IP_RASPBERRY_PI>:5000
```

Deberías ver:
- Dashboard principal con stream de video
- Panel de estado
- Lista de episodios
- Controles de configuración

### 2.2 Acceso desde Móvil

En la misma red WiFi, abre el navegador en tu móvil y visita la misma URL.

**Nota**: La interfaz es responsive y funciona bien en móviles.

### 2.3 Verificar que el Servicio Esté Corriendo

```bash
# Desde SSH en la Raspberry Pi
sudo systemctl status pi-camera

# O verificar que el puerto esté abierto
sudo netstat -tlnp | grep 5000
```

### 2.4 Troubleshooting Acceso Web

**No se puede conectar**:
```bash
# Verificar que el servicio esté corriendo
sudo systemctl status pi-camera

# Verificar logs
sudo journalctl -u pi-camera -n 50

# Verificar firewall
sudo ufw status
# Si está activo, permitir puerto 5000:
sudo ufw allow 5000/tcp
```

**Stream no carga**:
- Verifica que la cámara esté funcionando: `libcamera-hello -t 0`
- Revisa logs del servicio
- Intenta recargar la página (Ctrl+F5)

---

## 3. Acceso desde Internet (Opcional - Avanzado)

### 3.1 Port Forwarding

**⚠️ ADVERTENCIA**: Exponer el sistema a internet requiere medidas de seguridad adicionales (autenticación, HTTPS, etc.) que no están implementadas en Fase 1.

Si aún así quieres hacerlo:

1. **Configurar Port Forwarding en tu router**:
   - Accede a la configuración del router
   - Busca "Port Forwarding" o "Virtual Server"
   - Redirige puerto externo (ej: 8080) → IP Raspberry Pi:5000

2. **Obtener IP Pública**:
   - Tu IP pública puede cambiar (IP dinámica)
   - Considera usar un servicio como DuckDNS o No-IP

3. **Acceso**:
   ```
   http://<TU_IP_PUBLICA>:8080
   ```

**Recomendación**: Usa un túnel SSH en su lugar (más seguro).

### 3.2 Túnel SSH (Recomendado)

**Desde tu computadora local**:

```bash
ssh -L 5000:localhost:5000 pi@<IP_RASPBERRY_PI>
```

Ahora puedes acceder a:
```
http://localhost:5000
```

Y el tráfico se redirige de forma segura a través de SSH.

---

## 4. VNC (Acceso de Escritorio Remoto - Opcional)

### 4.1 Instalar VNC Server

```bash
sudo apt update
sudo apt install -y realvnc-vnc-server
```

### 4.2 Habilitar VNC

```bash
sudo raspi-config
```

Navega a:
- **Interface Options** → **VNC** → **Enable**

### 4.3 Conectar desde Cliente VNC

**En tu computadora**, instala un cliente VNC:
- **Windows**: RealVNC Viewer, TightVNC
- **Mac**: RealVNC Viewer (disponible en App Store)
- **Linux**: `sudo apt install remmina` o RealVNC Viewer

**Conectar**:
- Abre el cliente VNC
- Ingresa: `<IP_RASPBERRY_PI>:5900`
- Usuario y contraseña de tu Raspberry Pi

---

## 5. Monitoreo Remoto

### 5.1 Ver Estado del Sistema

**Vía SSH**:
```bash
# Estado del servicio
sudo systemctl status pi-camera

# Ver logs en tiempo real
sudo journalctl -u pi-camera -f

# Ver últimos eventos
sudo journalctl -u pi-camera -n 100
```

**Vía API**:
```bash
curl http://<IP_RASPBERRY_PI>:5000/api/status
```

### 5.2 Ver Episodios Guardados

**Vía SSH**:
```bash
ls -lh ~/Pi_camara/data/episodes/
ls -lh ~/Pi_camara/data/videos/
```

**Vía API**:
```bash
curl http://<IP_RASPBERRY_PI>:5000/api/episodes?limit=10
```

### 5.3 Ver Base de Datos

```bash
cd ~/Pi_camara
sqlite3 data/database.db

# Consultas útiles:
.tables
SELECT * FROM episodes ORDER BY start_time DESC LIMIT 10;
SELECT * FROM events ORDER BY timestamp DESC LIMIT 20;
.quit
```

---

## 6. Transferencia de Archivos

### 6.1 SCP (Secure Copy)

**Copiar archivo desde Raspberry Pi a tu computadora**:
```bash
scp pi@<IP_RASPBERRY_PI>:~/Pi_camara/data/episodes/episode_001/video.mp4 ./
```

**Copiar archivo desde tu computadora a Raspberry Pi**:
```bash
scp archivo.txt pi@<IP_RASPBERRY_PI>:~/
```

**Copiar carpeta completa**:
```bash
scp -r pi@<IP_RASPBERRY_PI>:~/Pi_camara/data/episodes ./
```

### 6.2 SFTP

```bash
sftp pi@<IP_RASPBERRY_PI>
# Comandos:
cd Pi_camara/data/episodes
get episode_001
put archivo_local.txt
quit
```

### 6.3 rsync (Sincronización)

```bash
# Sincronizar episodios desde Pi a tu computadora
rsync -avz pi@<IP_RASPBERRY_PI>:~/Pi_camara/data/episodes/ ./episodes_backup/
```

---

## 7. Comandos Útiles Remotos

### 7.1 Reiniciar el Servicio

```bash
ssh pi@<IP_RASPBERRY_PI> "sudo systemctl restart pi-camera"
```

### 7.2 Ver Logs

```bash
ssh pi@<IP_RASPBERRY_PI> "sudo journalctl -u pi-camera -n 50"
```

### 7.3 Verificar Cámara

```bash
ssh pi@<IP_RASPBERRY_PI> "libcamera-hello -t 0"
```

### 7.4 Actualizar Código

```bash
ssh pi@<IP_RASPBERRY_PI> "cd ~/Pi_camara && git pull && source venv/bin/activate && pip install -r requirements.txt && sudo systemctl restart pi-camera"
```

---

## 8. Troubleshooting

### 8.1 No Puedo Conectar por SSH

**Verificar**:
- ¿Está la Raspberry Pi encendida?
- ¿Está en la misma red?
- ¿SSH está habilitado? (`sudo systemctl status ssh`)
- ¿El firewall bloquea el puerto 22?

**Solución**:
```bash
# En la Raspberry Pi (acceso físico necesario)
sudo systemctl enable ssh
sudo systemctl start ssh
sudo ufw allow 22/tcp
```

### 8.2 No Puedo Acceder a la Interfaz Web

**Verificar**:
- ¿El servicio está corriendo? (`sudo systemctl status pi-camera`)
- ¿El puerto 5000 está abierto? (`sudo netstat -tlnp | grep 5000`)
- ¿El firewall permite el puerto? (`sudo ufw status`)

**Solución**:
```bash
# Ver logs para errores
sudo journalctl -u pi-camera -n 100

# Reiniciar servicio
sudo systemctl restart pi-camera

# Permitir puerto en firewall
sudo ufw allow 5000/tcp
```

### 8.3 Conexión Lenta

**Posibles causas**:
- Red WiFi débil
- Raspberry Pi sobrecargada
- Múltiples conexiones simultáneas

**Soluciones**:
- Usar conexión Ethernet si es posible
- Reducir resolución de video
- Verificar carga del sistema: `htop`

---

## 9. Seguridad

### 9.1 Cambiar Contraseña por Defecto

```bash
passwd
```

### 9.2 Deshabilitar Login Root

```bash
sudo passwd -l root
```

### 9.3 Configurar Fail2Ban (Protección contra ataques)

```bash
sudo apt install -y fail2ban
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

### 9.4 Actualizar Sistema Regularmente

```bash
sudo apt update && sudo apt upgrade -y
```

---

## 10. Referencias

- **raspberry-pi-setup.md**: Configuración inicial completa (misma carpeta)
- **OPERATION.md**: Operación diaria del sistema
- **README.md**: Información general del proyecto

---

**Última Actualización**: 2025-01-15
