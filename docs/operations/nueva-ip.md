# Nueva IP de la Raspberry Pi

**Fecha**: 2026-01-17  
**IP Anterior**: 192.168.0.105  
**IP Nueva**: **192.168.1.50**

## Cambio de IP

La Raspberry Pi cambió de IP debido a que ahora está conectada por Ethernet a la LAN.

### Nueva Configuración

- **IP**: 192.168.1.50
- **Hostname**: picamara.local (resuelve correctamente)
- **Puerto SSH**: 22
- **Puerto Web**: 5000

## Acceso al Sistema

### Interfaz Web
```
http://192.168.1.50:5000
```

### SSH
```bash
ssh picamara@192.168.1.50
# o
ssh picamara@picamara.local
```

## Comandos Útiles

### Verificar que el servidor esté corriendo
```bash
ssh picamara@192.168.1.50 'ps aux | grep run.py'
```

### Iniciar el servidor
```bash
ssh picamara@192.168.1.50 'cd ~/Pi_camara && nohup ./venv/bin/python3 run.py > logs/server.log 2>&1 &'
```

### Ver logs
```bash
ssh picamara@192.168.1.50 'tail -f ~/Pi_camara/logs/server.log'
```

### Detener el servidor
```bash
ssh picamara@192.168.1.50 'pkill -f run.py'
```

## Nota

Si cambias de red o la IP cambia nuevamente, puedes encontrar la nueva IP con:

```bash
ping picamara.local
# o
ping raspberrypi.local
```

El output mostrará la IP actual.
