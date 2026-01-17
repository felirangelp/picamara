# Guía de Configuración de Raspberry Pi

## Configuración Inicial del Sistema

Esta guía te ayudará a configurar tu Raspberry Pi 4 para ejecutar el Sistema de Seguridad Inteligente.

---

## 1. Requisitos Previos

### Hardware Necesario

- **Raspberry Pi 4** (mínimo 4GB RAM recomendado)
- **Cámara IMX219 8MP** conectada vía CSI
- **Tarjeta SD** 32GB+ (clase 10 o superior)
- **Fuente de alimentación** oficial de Raspberry Pi (5V, 3A)
- **Conexión a red** (WiFi o Ethernet)
- **Cable HDMI** (opcional, para configuración inicial)
- **Teclado y mouse** (opcional, para configuración inicial)

### Software Necesario

- **Raspberry Pi Imager** (para escribir imagen en SD)
- **Raspberry Pi OS** (64-bit) - descargado automáticamente por Imager

---

## 2. Instalación del Sistema Operativo

### 2.1 Descargar e Instalar Raspberry Pi OS

1. **Descargar Raspberry Pi Imager**:
   - Visita: https://www.raspberrypi.com/software/
   - Descarga e instala Raspberry Pi Imager para tu sistema operativo

2. **Escribir imagen en tarjeta SD**:
   - Abre Raspberry Pi Imager
   - Selecciona "Raspberry Pi OS (64-bit)" como sistema operativo
   - Selecciona tu tarjeta SD
   - **IMPORTANTE**: Antes de escribir, haz clic en el ícono de engranaje (⚙️) para configurar:
     - **Habilitar SSH**: Marca la casilla
     - **Establecer usuario y contraseña**: Crea un usuario (por defecto `pi` con contraseña)
     - **Configurar WiFi**: Ingresa tu SSID y contraseña WiFi
     - **Configurar localización**: Selecciona tu país/zona horaria
   - Haz clic en "Write" y espera a que termine

3. **Insertar tarjeta SD en Raspberry Pi**:
   - Apaga la Raspberry Pi si está encendida
   - Inserta la tarjeta SD
   - Conecta la cámara IMX219 al puerto CSI
   - Conecta la fuente de alimentación

---

## 3. Primera Conexión

### 3.1 Encontrar la IP de tu Raspberry Pi

**Opción 1: Desde el router**
- Accede a la interfaz de administración de tu router
- Busca dispositivos conectados
- Identifica "raspberrypi" en la lista

**Opción 2: Desde la red local**
```bash
# En Linux/Mac
ping raspberrypi.local

# O escanear la red
nmap -sn 192.168.1.0/24
```

**Opción 3: Desde la Raspberry Pi (si tienes acceso físico)**
```bash
hostname -I
```

### 3.2 Conectar vía SSH

```bash
ssh pi@<IP_RASPBERRY_PI>
# O si configuraste otro usuario:
ssh <usuario>@<IP_RASPBERRY_PI>
```

Si es la primera vez, acepta la clave SSH escribiendo `yes`.

---

## 4. Configuración de la Cámara

### 4.1 Habilitar Interfaz de Cámara

```bash
sudo raspi-config
```

Navega a:
- **Interface Options** → **Camera** → **Enable**

Presiona Enter para habilitar y luego **Finish**.

### 4.2 Verificar Detección de Cámara

```bash
libcamera-hello --list-cameras
```

Deberías ver algo como:
```
Available cameras
-----------------
0 : imx219 [3280x2464] (/base/soc/i2c0mux/i2c@1/imx219@10)
    Modes: 'SRGGB10_CSI2P' : 640x480 ... 3280x2464
```

### 4.3 Probar Captura de Video

```bash
# Captura de 5 segundos
libcamera-hello -t 5000

# O captura de imagen
libcamera-still -o test.jpg
```

Si ves la ventana de video o la imagen se guarda correctamente, la cámara está funcionando.

---

## 5. Instalación de Dependencias del Sistema

### 5.1 Actualizar Sistema

```bash
sudo apt update
sudo apt upgrade -y
```

### 5.2 Instalar Dependencias Base

```bash
sudo apt install -y \
    python3-pip \
    python3-venv \
    git \
    libcamera-dev \
    libopencv-dev \
    python3-opencv \
    build-essential \
    cmake \
    pkg-config
```

### 5.3 Instalar picamera2

```bash
sudo apt install -y python3-picamera2
```

### 5.4 Verificar Instalación

```bash
python3 -c "import picamera2; print('picamera2 OK')"
python3 -c "import cv2; print(f'OpenCV {cv2.__version__} OK')"
```

---

## 6. Configuración de Red (Opcional pero Recomendado)

### 6.1 Configurar IP Estática

Edita el archivo de configuración:

```bash
sudo nano /etc/dhcpcd.conf
```

Añade al final (ajusta según tu red):

```
interface eth0
static ip_address=192.168.1.100/24
static routers=192.168.1.1
static domain_name_servers=192.168.1.1 8.8.8.8
```

O para WiFi:

```
interface wlan0
static ip_address=192.168.1.100/24
static routers=192.168.1.1
static domain_name_servers=192.168.1.1 8.8.8.8
```

Guarda (Ctrl+O, Enter) y cierra (Ctrl+X).

Reinicia el servicio:

```bash
sudo systemctl restart dhcpcd
```

### 6.2 Configurar Firewall (Opcional)

```bash
sudo apt install -y ufw
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 5000/tcp  # Web server
sudo ufw enable
```

---

## 7. Clonación e Instalación del Proyecto

### 7.1 Clonar Repositorio

```bash
cd ~
git clone <URL_DEL_REPOSITORIO> Pi_camara
cd Pi_camara
```

O si estás copiando archivos manualmente:

```bash
cd ~
mkdir Pi_camara
cd Pi_camara
# Copia todos los archivos aquí
```

### 7.2 Crear Entorno Virtual

```bash
python3 -m venv venv
source venv/bin/activate
```

### 7.3 Instalar Dependencias Python

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Nota**: La instalación puede tardar varios minutos, especialmente torch y torchvision.

### 7.4 Crear Estructura de Directorios

```bash
mkdir -p data/videos data/episodes data/models
mkdir -p logs
```

### 7.5 Verificar Instalación

```bash
python3 -c "import fastapi; print('FastAPI OK')"
python3 -c "import lerobot; print('LeRobot OK')"
```

---

## 8. Configuración del Servicio Systemd

### 8.1 Crear Archivo de Servicio

```bash
sudo nano /etc/systemd/system/pi-camera.service
```

Pega el siguiente contenido (ajusta rutas según tu instalación):

```ini
[Unit]
Description=Pi Camera Security System
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/Pi_camara
Environment="PATH=/home/pi/Pi_camara/venv/bin"
ExecStart=/home/pi/Pi_camara/venv/bin/python src/main.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

Guarda y cierra.

### 8.2 Habilitar y Iniciar Servicio

```bash
sudo systemctl daemon-reload
sudo systemctl enable pi-camera
sudo systemctl start pi-camera
```

### 8.3 Verificar Estado

```bash
sudo systemctl status pi-camera
```

Deberías ver "active (running)".

### 8.4 Ver Logs

```bash
# Ver logs en tiempo real
sudo journalctl -u pi-camera -f

# Ver últimos 100 líneas
sudo journalctl -u pi-camera -n 100
```

---

## 9. Verificación Final

### 9.1 Probar Acceso Web

Abre un navegador y visita:

```
http://<IP_RASPBERRY_PI>:5000
```

Deberías ver la interfaz web con el stream de video.

### 9.2 Probar API

```bash
# Estado del sistema
curl http://<IP_RASPBERRY_PI>:5000/api/status

# Lista de episodios
curl http://<IP_RASPBERRY_PI>:5000/api/episodes
```

### 9.3 Probar Detección de Movimiento

- Mueve algo delante de la cámara
- Deberías ver rectángulos verdes en las áreas de movimiento
- Verifica que se guarden episodios en `data/episodes/`

---

## 10. Troubleshooting

### 10.1 Cámara No Detectada

```bash
# Verificar conexión física
# Verificar que la cámara esté habilitada
sudo raspi-config  # Interface Options → Camera

# Verificar permisos
groups $USER  # Debe incluir 'video'
```

### 10.2 Error al Iniciar Servicio

```bash
# Ver logs detallados
sudo journalctl -u pi-camera -n 50

# Probar manualmente
cd ~/Pi_camara
source venv/bin/activate
python src/main.py
```

### 10.3 Puerto 5000 Ya en Uso

```bash
# Ver qué proceso usa el puerto
sudo lsof -i :5000

# O cambiar puerto en config/camera_config.yaml
```

### 10.4 Problemas de Rendimiento

- Reducir resolución en `config/camera_config.yaml`
- Aumentar `min_area` para menos detecciones
- Verificar temperatura: `vcgencmd measure_temp`

---

## 11. Comandos Útiles

### Iniciar/Parar Servicio

```bash
sudo systemctl start pi-camera
sudo systemctl stop pi-camera
sudo systemctl restart pi-camera
```

### Ver Estado

```bash
sudo systemctl status pi-camera
```

### Ver Logs

```bash
sudo journalctl -u pi-camera -f
```

### Actualizar Código

```bash
cd ~/Pi_camara
git pull  # Si usas git
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart pi-camera
```

---

## 12. Próximos Pasos

Una vez configurado, consulta:

- **connection-guide.md**: Para acceso remoto avanzado (misma carpeta)
- **OPERATION.md**: Para operación diaria del sistema
- **README.md**: Para información general del proyecto

---

**Última Actualización**: 2025-01-15
