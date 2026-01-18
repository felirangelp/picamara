# Configuración de Red de la Raspberry Pi

**Fecha**: 2026-01-17  
**Última actualización**: 2026-01-17

## Configuración de Red

La Raspberry Pi está configurada con **IP dinámica (DHCP)** y usa **hostname** para acceso.

### Configuración Actual

- **Hostname**: `picamara.local` ⭐ **RECOMENDADO - Usa este en todos los scripts**
- **IP Actual**: 192.168.1.50 (puede cambiar)
- **Puerto SSH**: 22
- **Puerto Web**: 5000

### ¿Por qué usar el hostname?

El hostname `picamara.local` se resuelve automáticamente mediante mDNS (multicast DNS), lo que significa:
- ✅ **No importa si la IP cambia** - siempre encontrarás la Raspberry Pi
- ✅ **Funciona en cualquier red** - mientras esté en la misma LAN
- ✅ **Más fácil de recordar** - no necesitas saber la IP
- ✅ **Todos los scripts usan el hostname por defecto**

## Acceso al Sistema

### Interfaz Web
```
http://picamara.local:5000
```

**Nota**: Si el hostname no funciona, puedes usar la IP actual:
```bash
# Encontrar la IP actual
ping picamara.local
# Luego usar: http://<IP_ACTUAL>:5000
```

### SSH
```bash
# RECOMENDADO: Usar hostname
ssh picamara@picamara.local

# Alternativa: Usar IP (si el hostname no funciona)
ssh picamara@192.168.1.50
```

## Comandos Útiles

### Verificar que el servidor esté corriendo
```bash
ssh picamara@picamara.local 'ps aux | grep run.py'
```

### Iniciar el servidor
```bash
ssh picamara@picamara.local 'cd ~/Pi_camara && nohup ./venv/bin/python3 run.py > logs/server.log 2>&1 &'
```

### Ver logs
```bash
ssh picamara@picamara.local 'tail -f ~/Pi_camara/logs/server.log'
```

### Detener el servidor
```bash
ssh picamara@picamara.local 'pkill -f run.py'
```

## Encontrar la IP Actual

Si necesitas saber la IP actual (por ejemplo, para acceder desde un navegador que no soporta mDNS):

```bash
# Opción 1: Ping al hostname (muestra la IP)
ping picamara.local

# Opción 2: Desde la Raspberry Pi
ssh picamara@picamara.local 'hostname -I'

# Opción 3: Escanear la red
nmap -sn 192.168.1.0/24 | grep -B 2 "picamara"
```

## Ventajas de Usar Hostname

✅ **No necesitas actualizar scripts** cuando la IP cambia  
✅ **Funciona automáticamente** en cualquier red local  
✅ **Más fácil de recordar** que una IP  
✅ **Todos los scripts del proyecto usan `picamara.local` por defecto**
