# Guía de Pruebas - Conectividad y Cámara

Esta guía explica cómo probar la conectividad con la Raspberry Pi y verificar que la cámara funcione correctamente.

## Pruebas Disponibles

### 1. Prueba Remota (desde tu computadora)

Ejecuta el script de prueba remota que verifica:
- ✅ Conexión SSH
- ✅ Detección de cámara
- ✅ Importación de picamera2
- ✅ Captura de frames
- ✅ Servidor web (opcional)

#### Opción A: Script con expect (recomendado, maneja contraseña automáticamente)

**Uso:**
```bash
# Desde tu computadora
cd Pi_camara
./scripts/test_with_expect.sh <IP> <USER> <PASSWORD>

# Ejemplo
./scripts/test_with_expect.sh 192.168.0.105 picamara picamara
```

Este script usa `expect` para manejar la autenticación SSH automáticamente.

#### Opción B: Script Python (requiere SSH keys configuradas)

**Uso:**
```bash
# Desde tu computadora
cd Pi_camara
source venv/bin/activate
python scripts/test_raspberry_connection.py --host <IP_RASPBERRY_PI>

# Con opciones
python scripts/test_raspberry_connection.py \
    --host 192.168.1.100 \
    --user pi \
    --project-path ~/Pi_camara
```

**Opciones:**
- `--host`: IP o hostname de la Raspberry Pi (requerido)
- `--user`: Usuario SSH (default: pi)
- `--project-path`: Ruta al proyecto en la Pi (default: ~/Pi_camara)
- `--skip-ssh`: Saltar prueba SSH (si ya estás en la Pi)
- `--skip-web`: Saltar prueba de servidor web

**Ejemplo:**
```bash
python scripts/test_raspberry_connection.py --host 192.168.1.100
```

#### Prueba Detallada de Cámara

Para una verificación más exhaustiva de la cámara:

```bash
./scripts/test_camera_detailed.sh <IP> <USER> <PASSWORD>
```

Este script verifica:
- Dispositivos de video (`/dev/video*`)
- Módulos de cámara cargados
- Captura de frames con picamera2
- Propiedades de la cámara

### 2. Prueba Local (en la Raspberry Pi)

Ejecuta el script directamente en la Raspberry Pi:

**Uso:**
```bash
# En la Raspberry Pi
cd ~/Pi_camara
source venv/bin/activate
python scripts/test_camera_local.py
```

Este script prueba:
- ✅ Inicialización de cámara
- ✅ Captura de frames
- ✅ Detección de movimiento

## Verificación Manual

### 1. Verificar Cámara con libcamera

```bash
# En Raspberry Pi
libcamera-hello --list-cameras
```

Deberías ver algo como:
```
Available cameras
-----------------
0 : imx219 [3280x2464] (/base/soc/i2c0mux/i2c@1/imx219@10)
```

### 2. Probar Captura de Video

```bash
# Captura de 5 segundos
libcamera-hello -t 5000
```

### 3. Verificar picamera2

```bash
# En Raspberry Pi, con venv activado
source venv/bin/activate
python3 -c "import picamera2; print('picamera2 OK')"
```

### 4. Probar Código del Proyecto

```bash
# En Raspberry Pi
cd ~/Pi_camara
source venv/bin/activate

# Probar importación
python3 -c "from src.camera.imx219_handler import IMX219Handler; print('OK')"
```

## Troubleshooting

### Error: "picamera2 no disponible"

**Solución:**
```bash
sudo apt install python3-picamera2
```

### Error: "Cámara no detectada"

**Solución:**
1. Verificar conexión física de la cámara
2. Habilitar cámara:
   ```bash
   sudo raspi-config
   # Interface Options → Camera → Enable
   ```
3. Reiniciar Raspberry Pi

### Error: "SSH connection failed"

**Solución:**
1. Verificar que SSH esté habilitado:
   ```bash
   sudo systemctl status ssh
   ```
2. Verificar IP de la Raspberry Pi:
   ```bash
   hostname -I
   ```
3. Verificar que estés en la misma red

### Error: "Module not found"

**Solución:**
1. Asegúrate de estar en el entorno virtual:
   ```bash
   source venv/bin/activate
   ```
2. Instala dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## Checklist de Verificación

Antes de ejecutar el sistema completo, verifica:

- [ ] Raspberry Pi encendida y conectada a red
- [ ] Cámara IMX219 conectada físicamente
- [ ] Cámara habilitada en raspi-config
- [ ] SSH habilitado y accesible
- [ ] Proyecto clonado en ~/Pi_camara
- [ ] Entorno virtual creado y activado
- [ ] Dependencias instaladas
- [ ] picamera2 instalado (sudo apt install python3-picamera2)
- [ ] Pruebas de conectividad pasan

## Resultados de Pruebas

Para ver los resultados de las pruebas realizadas, consulta:
- [Resultados de Pruebas](./test-results.md)

## Siguiente Paso

Una vez que todas las pruebas pasen, puedes iniciar el sistema completo:

```bash
# En Raspberry Pi
cd ~/Pi_camara
source venv/bin/activate
python src/main.py
```

Luego accede a `http://<IP_RASPBERRY_PI>:5000` desde tu navegador.

---

**Última actualización**: 2025-01-17
