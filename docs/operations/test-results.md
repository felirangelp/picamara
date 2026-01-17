# Resultados de Pruebas de Conectividad

**Fecha:** 2025-01-17  
**IP Raspberry Pi:** 192.168.0.105  
**Usuario:** picamara

## Resumen Ejecutivo

✅ **Conexión SSH:** Funcional  
✅ **picamera2:** Instalado y operativo  
✅ **Captura de frames:** Exitosa  
⚠️ **Modelo de cámara:** OV5647 detectada (no IMX219)

## Pruebas Realizadas

### 1. Conexión SSH
- **Estado:** ✅ Exitoso
- **Comando:** `ssh picamara@192.168.0.105`
- **Resultado:** Autenticación y conexión funcionando correctamente

### 2. Dispositivos de Video
- **Estado:** ✅ Detectados
- **Dispositivos encontrados:**
  - `/dev/video0` a `/dev/video31` (múltiples interfaces)
- **Permisos:** Correctos (usuario en grupo `video`)

### 3. picamera2
- **Estado:** ✅ Instalado y funcional
- **Prueba:** `python3 -c 'import picamera2; print("OK")'`
- **Resultado:** Importación exitosa

### 4. Captura de Frames
- **Estado:** ✅ Funcional
- **Prueba:** Captura de frame con `Picamera2().capture_array()`
- **Resultado:** Frame capturado con shape `(480, 640, 4)`
- **Formato:** XBGR8888/sRGB

### 5. Modelo de Cámara
- **Estado:** ⚠️ Detectada OV5647
- **Información:**
  - Modelo detectado: `ov5647`
  - Pipeline: `rpi/vc4`
  - Tuning file: `/usr/share/libcamera/ipa/rpi/vc4/ov5647.json`
- **Nota:** El sistema detectó una cámara OV5647 en lugar de IMX219. Esto puede deberse a:
  1. Otra cámara conectada físicamente
  2. El sistema detectó otra interfaz de cámara
  3. La IMX219 necesita configuración adicional

**Importante:** El código del proyecto debería funcionar con cualquier cámara compatible con `picamera2`, incluyendo tanto OV5647 como IMX219.

### 6. Proyecto en Raspberry Pi
- **Estado:** ⚠️ No encontrado
- **Ruta esperada:** `~/Pi_camara`
- **Acción requerida:** Transferir o clonar el proyecto a la Raspberry Pi

## Scripts de Prueba Creados

1. **`scripts/test_with_expect.sh`**
   - Prueba completa de conectividad usando `expect`
   - Maneja autenticación SSH con contraseña
   - Verifica SSH, cámara, picamera2 y proyecto

2. **`scripts/test_camera_detailed.sh`**
   - Prueba detallada de cámara
   - Verifica dispositivos, módulos y captura de frames

3. **`scripts/check_camera_model.sh`**
   - Verifica modelo exacto de cámara conectada
   - Obtiene información de propiedades de cámara

## Próximos Pasos

1. **Transferir proyecto a Raspberry Pi:**
   ```bash
   # Desde tu máquina local
   rsync -avz --exclude 'venv' --exclude '__pycache__' \
     /Users/feliperangel/Python/Pi_camara/ \
     picamara@192.168.0.105:~/Pi_camara/
   ```

2. **Instalar dependencias en Raspberry Pi:**
   ```bash
   ssh picamara@192.168.0.105
   cd ~/Pi_camara
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Ejecutar prueba local de cámara:**
   ```bash
   # En la Raspberry Pi
   python scripts/test_camera_local.py
   ```

4. **Iniciar servidor web:**
   ```bash
   # En la Raspberry Pi
   python src/main.py
   ```

## Notas Técnicas

- **libcamera version:** v0.6.0+rpt20251202
- **Sistema de archivos de cámara:** `/base/soc/i2c0mux/i2c@1/ov5647@36`
- **Dispositivos Unicam/ISP:** `/dev/media2` y `/dev/media1`
- **Resolución de prueba:** 640x480 (configurable)

## Referencias

- [Guía de Conexión](../operations/connection-guide.md)
- [Guía de Testing](../operations/testing-guide.md)
- [Configuración de Raspberry Pi](../operations/raspberry-pi-setup.md)
