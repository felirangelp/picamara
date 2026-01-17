# Prueba Rápida de Conectividad

## Obtener la IP de tu Raspberry Pi

### Opción 1: Desde la Raspberry Pi (si tienes acceso físico/pantalla)
```bash
hostname -I
```

### Opción 2: Desde tu router
- Accede a la interfaz de administración de tu router
- Busca en la lista de dispositivos conectados
- Identifica "raspberrypi" o el nombre que configuraste

### Opción 3: Desde tu computadora (si están en la misma red)
```bash
# En Mac/Linux
ping raspberrypi.local
# O
arp -a | grep -i raspberry
```

## Ejecutar Pruebas

Una vez que tengas la IP, ejecuta:

```bash
cd /Users/feliperangel/Python/Pi_camara
source venv/bin/activate
python scripts/test_raspberry_connection.py --host <TU_IP> --user picamara
```

**Ejemplo:**
```bash
python scripts/test_raspberry_connection.py --host 192.168.1.50 --user picamara
```

## Qué Prueba el Script

1. ✅ Conexión SSH
2. ✅ Detección de cámara IMX219
3. ✅ Importación de picamera2
4. ✅ Captura de frames
5. ✅ Servidor web (opcional)

## Si No Tienes la IP

Puedes ejecutar este comando en la Raspberry Pi para obtenerla:
```bash
hostname -I
```
