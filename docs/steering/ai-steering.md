# Steering File - Constitución del Proyecto

## Documento de Dirección del Agente de IA (AI-DLC)

**Versión**: 1.0  
**Fecha**: 2025-01-15  
**Estado**: Inmutable (solo modificar en fase de Inception/Construction)

---

## 1. Principios de Arquitectura

### 1.1 Separación de Capas

El sistema DEBE seguir una arquitectura en capas claramente definida:

```
┌─────────────────────────────────┐
│   Frontend (Web UI)             │
├─────────────────────────────────┤
│   API Layer (FastAPI)           │
├─────────────────────────────────┤
│   Business Logic                │
│   - Detection                   │
│   - Storage                     │
│   - Alerts                      │
├─────────────────────────────────┤
│   Data Layer                    │
│   - Database (SQLite)           │
│   - File System                 │
│   - LeRobotDataset              │
├─────────────────────────────────┤
│   Hardware Layer                │
│   - Camera (picamera2)          │
└─────────────────────────────────┘
```

**Regla**: Cada capa solo puede comunicarse con la capa inmediatamente inferior. No se permiten dependencias circulares.

### 1.2 Async/Await Obligatorio

**REQUISITO**: Todas las operaciones I/O (cámara, base de datos, red) DEBEN usar `async/await`.

**Prohibido**:
- Operaciones síncronas bloqueantes en el loop principal
- `time.sleep()` en código async (usar `asyncio.sleep()`)
- Llamadas síncronas a base de datos sin ejecutarlas en thread pool

**Permitido**:
- `async def` para todas las funciones que hacen I/O
- `await` para operaciones asíncronas
- Thread pools para operaciones que no pueden ser async (ej: OpenCV)

### 1.3 Manejo de Errores Robusto

**REQUISITO**: Todos los módulos DEBEN tener manejo de errores completo.

**Reglas**:
- Usar `try/except` específicos (no `except Exception` genérico)
- Logging de errores con contexto suficiente
- No silenciar errores sin registro
- Propagar errores con información útil
- Usar excepciones personalizadas cuando sea apropiado

**Ejemplo Prohibido**:
```python
def capture_frame():
    frame = camera.capture()  # Sin manejo de errores
    return frame
```

**Ejemplo Permitido**:
```python
async def capture_frame() -> Optional[np.ndarray]:
    """Captura un frame de la cámara.
    
    Returns:
        Frame capturado o None si hay error.
    """
    try:
        frame = await camera.capture_async()
        return frame
    except CameraError as e:
        logger.error(f"Error capturando frame: {e}", exc_info=True)
        return None
    except Exception as e:
        logger.critical(f"Error inesperado en captura: {e}", exc_info=True)
        raise
```

---

## 2. Estándares de Código

### 2.1 Type Hints Obligatorios

**REQUISITO**: Todas las funciones y métodos DEBEN tener type hints completos.

**Prohibido**:
```python
def process_frame(frame):
    return frame
```

**Permitido**:
```python
def process_frame(frame: np.ndarray) -> np.ndarray:
    """Procesa un frame de video."""
    return frame
```

**Excepciones**: Solo en casos donde el tipo es realmente `Any` o `Union` complejo, documentar claramente.

### 2.2 Docstrings en Formato Google

**REQUISITO**: Todas las clases y funciones públicas DEBEN tener docstrings en formato Google.

**Formato Requerido**:
```python
def function_name(param1: Type1, param2: Type2) -> ReturnType:
    """Breve descripción de una línea.
    
    Descripción más detallada si es necesario. Puede incluir
    múltiples párrafos.
    
    Args:
        param1: Descripción del parámetro 1.
        param2: Descripción del parámetro 2.
    
    Returns:
        Descripción del valor de retorno.
    
    Raises:
        ValueError: Cuando el parámetro es inválido.
        CameraError: Cuando la cámara no está disponible.
    
    Example:
        >>> result = function_name(value1, value2)
        >>> print(result)
        output
    """
    pass
```

### 2.3 Estructura Modular

**REQUISITO**: Cada módulo DEBE tener su propio `__init__.py` que exporte la API pública.

**Estructura Requerida**:
```
src/
  camera/
    __init__.py          # Exporta: IMX219Handler
    imx219_handler.py
  detection/
    __init__.py          # Exporta: MotionDetector
    motion_detector.py
```

**En `__init__.py`**:
```python
"""Módulo de manejo de cámara IMX219."""

from .imx219_handler import IMX219Handler

__all__ = ['IMX219Handler']
```

---

## 3. Restricciones Tecnológicas

### 3.1 Stack Tecnológico Obligatorio

**Backend Framework**: FastAPI (NO Flask)
- **Razón**: Mejor rendimiento async, documentación automática, type hints nativos
- **Prohibido**: Flask, Django, otros frameworks síncronos

**Base de Datos**: SQLite (Fase 1)
- **Razón**: Sin servidor, fácil setup, suficiente para fase inicial
- **Futuro**: PostgreSQL cuando se necesite escalar

**Cámara**: picamera2
- **Razón**: API moderna, soporte oficial Raspberry Pi
- **Prohibido**: picamera (legacy), OpenCV VideoCapture directo

**Visión**: OpenCV
- **Razón**: Estándar de la industria, optimizado
- **Versión**: opencv-python >= 4.8.0

**ML/Datos**: LeRobot, LeRobotDataset v3
- **Razón**: Formato estándar para datos de robótica
- **Versión**: lerobot >= 2.0.0

### 3.2 Dependencias Prohibidas

**NO usar**:
- Flask (usar FastAPI)
- Frameworks frontend pesados (React, Vue, Angular) - usar vanilla JS
- ORMs complejos (SQLAlchemy) - usar sqlite3 directo
- Librerías no mantenidas o deprecated

### 3.3 Versiones Mínimas

- Python: 3.9+
- FastAPI: 0.100.0+
- OpenCV: 4.8.0+
- picamera2: 0.3.12+

---

## 4. Patrones Prohibidos

### 4.1 Código Monolítico

**Prohibido**: Un solo archivo con toda la lógica.

**Permitido**: Separación en módulos según responsabilidad.

### 4.2 Hardcoding de Paths

**Prohibido**:
```python
video_path = "/home/pi/videos/episode_001.mp4"
```

**Permitido**:
```python
from pathlib import Path
from config import settings

video_path = Path(settings.storage.save_path) / "episode_001.mp4"
```

### 4.3 Falta de Manejo de Errores

**Prohibido**: Funciones sin manejo de errores.

**Requisito**: Todas las funciones que hacen I/O o llamadas externas DEBEN tener try/except.

### 4.4 Variables Globales sin Locks

**Prohibido**:
```python
current_frame = None  # Acceso desde múltiples threads sin lock
```

**Permitido**:
```python
from threading import Lock

frame_lock = Lock()
current_frame = None

# Uso:
with frame_lock:
    current_frame = new_frame
```

### 4.5 Magic Numbers

**Prohibido**: Números mágicos sin explicación.

**Permitido**: Constantes con nombres descriptivos.

```python
# Prohibido:
if area > 500:
    pass

# Permitido:
MIN_MOTION_AREA = 500
if area > MIN_MOTION_AREA:
    pass
```

---

## 5. Estructura de Carpetas Obligatoria

La estructura DEBE seguir exactamente la definida en `docs/construction/design.md`:

```
Pi_camara/
├── src/
│   ├── camera/
│   ├── detection/
│   ├── database/
│   ├── data/
│   ├── web/
│   └── alerts/
├── config/
├── tests/
├── scripts/
└── data/
```

**NO crear**:
- Carpetas fuera de esta estructura
- Archivos en la raíz excepto los especificados en design.md
- Carpetas temporales o de trabajo en el repositorio

---

## 6. Convenciones de Nomenclatura

### 6.1 Archivos y Módulos

- **Archivos Python**: `snake_case.py`
- **Clases**: `PascalCase`
- **Funciones/Métodos**: `snake_case`
- **Constantes**: `UPPER_SNAKE_CASE`
- **Variables**: `snake_case`

### 6.2 Base de Datos

- **Tablas**: `snake_case` (plural): `episodes`, `events`
- **Columnas**: `snake_case`: `episode_id`, `start_time`

### 6.3 API Endpoints

- **Rutas**: `snake_case` o `kebab-case`: `/api/episodes`, `/video_feed`
- **Métodos HTTP**: Usar verbos apropiados (GET, POST, PUT, DELETE)

---

## 7. Testing Requirements

### 7.1 Cobertura Mínima

**REQUISITO**: 70% de cobertura de código mínimo.

### 7.2 Tipos de Pruebas Requeridas

1. **Unitarias**: Cada módulo debe tener tests unitarios
2. **Integración**: Tests de flujo completo
3. **Sistema**: Tests end-to-end

### 7.3 Naming de Tests

**Formato**: `test_<functionality>_<scenario>_<expected_result>`

**Ejemplo**:
```python
def test_motion_detector_detects_movement_when_frame_changes():
    pass

def test_database_adds_episode_when_motion_detected():
    pass
```

---

## 8. Logging Standards

### 8.1 Niveles de Log

- **DEBUG**: Información detallada para debugging
- **INFO**: Eventos normales del sistema
- **WARNING**: Situaciones anómalas pero manejables
- **ERROR**: Errores que requieren atención
- **CRITICAL**: Errores críticos que pueden detener el sistema

### 8.2 Formato de Logs

**Requisito**: Incluir timestamp, nivel, módulo, y mensaje.

**Ejemplo**:
```python
logger.info("Motion detected", extra={
    "episode_id": episode_id,
    "area": motion_area,
    "timestamp": datetime.now().isoformat()
})
```

---

## 9. Configuración

### 9.1 Archivos de Configuración

**Requisito**: Toda configuración DEBE estar en archivos YAML o .env, NO hardcoded.

**Estructura**:
- `config/camera_config.yaml`: Configuración del sistema
- `.env`: Variables de entorno sensibles (opcional en Fase 1)

### 9.2 Validación de Configuración

**Requisito**: Validar configuración al inicio y fallar rápido si es inválida.

---

## 10. Documentación

### 10.1 Documentación de Código

- Docstrings en todas las funciones públicas
- Comentarios explicativos para lógica compleja
- Type hints como documentación viva

### 10.2 Documentación de Usuario

- README.md con instrucciones de instalación
- Guías de configuración (raspberry-pi-setup.md)
- Guías de conexión (connection-guide.md)

---

## 11. Git y Versionado

### 11.1 Commits

**Formato**: `type: descripción breve`

**Tipos**:
- `feat`: Nueva funcionalidad
- `fix`: Corrección de bug
- `docs`: Documentación
- `test`: Tests
- `refactor`: Refactorización
- `config`: Configuración

### 11.2 Branches

- `main`: Código estable
- `develop`: Desarrollo activo
- `feature/*`: Nuevas funcionalidades

---

## 12. Excepciones y Casos Especiales

### 12.1 Cuando Violar una Regla

Si es absolutamente necesario violar una regla de este steering file:

1. Documentar la razón en un comentario
2. Incluir referencia a este steering file
3. Obtener aprobación explícita (en código, comentario)

**Ejemplo**:
```python
# EXCEPCIÓN: Usando time.sleep() en lugar de asyncio.sleep()
# porque esta función debe ejecutarse en thread separado
# y asyncio no está disponible. Ver .ai-steering.md sección 1.2
time.sleep(0.1)
```

---

## 13. Referencias

- **Requirements**: `docs/inception/requirements.md`
- **Design**: `docs/construction/design.md`
- **AI-DLC Methodology**: `AIDLC.pdf`

---

## 14. Aprobación y Modificación

Este steering file es **INMUTABLE** durante la fase de implementación.

**Solo puede modificarse en**:
- Fase de Inception (cuando se definen requisitos)
- Fase de Construction (cuando se ajusta diseño)

**Proceso de modificación**:
1. Actualizar versión
2. Documentar razón del cambio
3. Obtener aprobación
4. Actualizar referencias en código

---

**Última Actualización**: 2025-01-15  
**Versión**: 1.0  
**Estado**: Activo
