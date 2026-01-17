# Sistema de Seguridad Inteligente - Raspberry Pi

Sistema de seguridad con detección de movimiento en tiempo real para Raspberry Pi 4 con cámara IMX219 8MP.

## Características

- ✅ Detección de movimiento en tiempo real
- ✅ Almacenamiento automático de episodios
- ✅ Interfaz web responsive con streaming en vivo
- ✅ API REST para consulta de datos
- ✅ Integración con LeRobotDataset
- ✅ Base de datos SQLite para metadatos
- ✅ Sistema de alertas y logging

## Requisitos

- Raspberry Pi 4 (mínimo 4GB RAM recomendado)
- Cámara IMX219 8MP conectada vía CSI
- Raspberry Pi OS (64-bit)
- Python 3.9+
- Conexión a red (WiFi o Ethernet)

## Instalación

### 1. Configuración Inicial de Raspberry Pi

Sigue la guía completa en [docs/operations/raspberry-pi-setup.md](docs/operations/raspberry-pi-setup.md)

Resumen rápido:
```bash
# Habilitar cámara
sudo raspi-config  # Interface Options → Camera → Enable

# Instalar dependencias del sistema
sudo apt update
sudo apt install -y python3-pip python3-venv git libcamera-dev libopencv-dev python3-opencv
sudo apt install -y python3-picamera2
```

### 2. Clonar e Instalar Proyecto

```bash
cd ~
git clone <URL_DEL_REPOSITORIO> Pi_camara
cd Pi_camara

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias Python
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Configuración

El archivo de configuración está en `config/camera_config.yaml`. Puedes ajustar:
- Resolución de cámara
- Parámetros de detección de movimiento
- Rutas de almacenamiento
- Configuración del servidor web

### 4. Ejecutar

**Modo desarrollo:**
```bash
source venv/bin/activate
python src/main.py
```

**Como servicio systemd:**
```bash
# Instalar servicio
./scripts/install_service.sh

# Iniciar servicio
sudo systemctl start pi-camera

# Ver logs
sudo journalctl -u pi-camera -f
```

## Uso

### Acceso Web

Una vez iniciado, abre tu navegador en:
```
http://<IP_RASPBERRY_PI>:5000
```

### API REST

- `GET /api/status` - Estado del sistema
- `GET /api/episodes` - Lista de episodios
- `GET /api/events` - Eventos recientes
- `POST /api/config` - Actualizar configuración
- `GET /docs` - Documentación automática (Swagger UI)

### Ejemplos

**Obtener estado:**
```bash
curl http://localhost:5000/api/status
```

**Listar episodios con movimiento:**
```bash
curl http://localhost:5000/api/episodes?motion_only=true&limit=10
```

## Estructura del Proyecto

```
Pi_camara/
├── src/                    # Código fuente
│   ├── camera/            # Manejo de cámara IMX219
│   ├── detection/         # Detección de movimiento
│   ├── database/          # Gestión SQLite
│   ├── data/              # Integración LeRobotDataset
│   ├── web/               # FastAPI server y frontend
│   └── alerts/            # Sistema de alertas
├── docs/                   # Documentación completa (AI-DLC)
│   ├── inception/         # Fase 1: Especificaciones
│   ├── construction/      # Fase 2: Diseño técnico
│   ├── operations/        # Fase 3: Guías operacionales
│   └── steering/          # Steering files
├── config/                 # Archivos de configuración
├── tests/                  # Tests
├── scripts/                # Scripts de deployment
├── systemd/                # Archivos de servicio systemd
├── data/                   # Datos (videos, episodios, BD)
└── logs/                   # Logs del sistema
```

## Documentación

Toda la documentación está organizada en la carpeta [`docs/`](docs/). Ver el [índice de documentación](docs/README.md) para una guía completa.

**Documentos principales:**
- [docs/inception/requirements.md](docs/inception/requirements.md) - Especificaciones formales
- [docs/construction/design.md](docs/construction/design.md) - Diseño técnico
- [docs/operations/raspberry-pi-setup.md](docs/operations/raspberry-pi-setup.md) - Guía de configuración
- [docs/operations/connection-guide.md](docs/operations/connection-guide.md) - Guía de conexión remota
- [docs/steering/ai-steering.md](docs/steering/ai-steering.md) - Reglas de desarrollo

## Desarrollo

### Ejecutar Tests

```bash
source venv/bin/activate
pytest tests/ -v
```

### Estructura de Código

El proyecto sigue la metodología AI-DLC:
- **docs/inception/requirements.md**: Especificaciones formales (Fase 1)
- **docs/construction/design.md**: Diseño técnico (Fase 2)
- **docs/steering/ai-steering.md**: Reglas inmutables de código

## Troubleshooting

### Cámara no detectada
```bash
libcamera-hello --list-cameras
sudo raspi-config  # Verificar que cámara esté habilitada
```

### Error al iniciar servicio
```bash
sudo journalctl -u pi-camera -n 50
```

### Puerto 5000 en uso
Cambiar puerto en `config/camera_config.yaml` o:
```bash
sudo lsof -i :5000
```

## Licencia

[Especificar licencia]

## Contribuciones

[Instrucciones para contribuir]

## Autor

[Tu nombre/información]

---

**Última actualización**: 2025-01-15
