# Ecosistema del Proyecto - Arquitectura de Desarrollo y Deployment

**Fecha**: 2026-01-17  
**Metodología**: AI-DLC  
**Estado**: Documentación de Arquitectura Operacional

---

## 🎯 Visión General del Ecosistema

Este proyecto sigue una arquitectura **"Desarrollo Local - Deployment Remoto"** donde:

- **MacBook Pro (Local)**: Ambiente de desarrollo, edición de código, pruebas unitarias
- **Raspberry Pi (Remoto)**: Ambiente de producción, ejecución del sistema en hardware real

---

## 📁 Estructura del Ecosistema

```
┌─────────────────────────────────────────────────────────────┐
│                    MACBOOK PRO (LOCAL)                       │
│  /Users/feliperangel/Python/Pi_camara/                       │
│                                                              │
│  ✅ Código fuente (src/)                                     │
│  ✅ Documentación (docs/)                                    │
│  ✅ Scripts de deployment (scripts/)                         │
│  ✅ Configuración (config/)                                  │
│  ✅ Tests (tests/)                                           │
│  ✅ venv/ (entorno virtual para desarrollo)                 │
│  ❌ data/ (excluido - solo en Pi)                            │
│  ❌ logs/ (excluido - solo en Pi)                            │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       │ rsync (scripts/deploy_to_pi.sh)
                       │
┌──────────────────────▼──────────────────────────────────────┐
│              RASPBERRY PI (PRODUCCIÓN)                       │
│  /home/picamara/Pi_camara/                                  │
│                                                              │
│  ✅ Código fuente (src/) - Sincronizado                     │
│  ✅ Documentación (docs/) - Sincronizada                     │
│  ✅ Scripts (scripts/) - Sincronizados                      │
│  ✅ Configuración (config/) - Sincronizada                  │
│  ✅ venv/ (entorno virtual independiente)                    │
│  ✅ data/ (episodios, videos, modelos) - LOCAL              │
│  ✅ logs/ (logs del sistema) - LOCAL                      │
│  ✅ database.db (SQLite) - LOCAL                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔄 Flujo de Sincronización

### 1. Desarrollo en MacBook Pro

**Qué haces aquí:**
- ✏️ Editas código en `src/`
- 📝 Actualizas documentación en `docs/`
- 🧪 Ejecutas tests unitarios (si no requieren hardware)
- 📦 Preparas cambios para deployment

**Qué NO puedes hacer aquí:**
- ❌ Probar la cámara (no hay hardware)
- ❌ Ejecutar el sistema completo (requiere picamera2)
- ❌ Generar episodios reales

### 2. Sincronización con Raspberry Pi

**Script de deployment**: `scripts/deploy_to_pi.sh`

**Qué se transfiere:**
```bash
✅ src/              # Todo el código fuente
✅ docs/             # Documentación
✅ scripts/          # Scripts de utilidad
✅ config/           # Archivos de configuración
✅ tests/            # Tests (para ejecutar en Pi)
✅ requirements.txt  # Dependencias
✅ run.py            # Script de inicio
❌ venv/             # NO se transfiere (se crea en Pi)
❌ data/             # NO se transfiere (datos locales de Pi)
❌ logs/             # NO se transfiere (logs locales de Pi)
❌ __pycache__/      # NO se transfiere (caché Python)
```

### 3. Ejecución en Raspberry Pi

**Qué pasa aquí:**
- 🎥 El sistema se ejecuta con hardware real
- 💾 Se generan episodios en `data/episodes/`
- 📊 Se guardan logs en `logs/`
- 🗄️ Se actualiza la base de datos SQLite

---

## ✅ ¿Está Bien Esta Estrategia?

### **SÍ, está bien diseñada** por las siguientes razones:

#### 1. **Separación de Ambientes** ✅
- **Desarrollo**: MacBook Pro (rápido, cómodo para editar)
- **Producción**: Raspberry Pi (hardware real, cámara)

#### 2. **Sincronización Controlada** ✅
- Usas `rsync` para transferir solo lo necesario
- No transfieres datos pesados (videos, logs)
- No transfieres venv (cada ambiente tiene el suyo)

#### 3. **Independencia de Ambientes** ✅
- Cada ambiente tiene su propio `venv/`
- Dependencias se instalan independientemente
- Configuración puede diferir (ej: paths, IPs)

#### 4. **Datos Locales en Pi** ✅
- `data/episodes/` solo en Pi (son grandes, específicos del hardware)
- `logs/` solo en Pi (específicos de ejecución)
- `database.db` solo en Pi (datos de producción)

---

## 🔧 Mejoras Sugeridas (Opcionales)

### Opción A: Git como Fuente de Verdad (Recomendado)

**Estrategia mejorada:**
```
MacBook Pro (desarrollo)
    ↓ git push
Repositorio Git (GitHub/GitLab)
    ↓ git pull
Raspberry Pi (producción)
```

**Ventajas:**
- ✅ Versionado de código
- ✅ Historial de cambios
- ✅ Rollback fácil
- ✅ Colaboración

**Implementación:**
```bash
# En MacBook Pro
git add .
git commit -m "Cambios"
git push

# En Raspberry Pi
cd ~/Pi_camara
git pull
```

### Opción B: Mantener rsync (Actual)

**Ventajas:**
- ✅ Simple y directo
- ✅ No requiere repositorio Git
- ✅ Control total sobre qué transferir

**Desventajas:**
- ❌ Sin historial de versiones
- ❌ Más difícil hacer rollback

---

## 📋 Checklist de Sincronización

### Antes de Transferir Código:

- [ ] ¿Probé el código localmente (tests unitarios)?
- [ ] ¿Actualicé la documentación si cambié algo?
- [ ] ¿Verifiqué que no hay paths hardcodeados?
- [ ] ¿Revisé que los imports funcionen en ambos ambientes?

### Después de Transferir:

- [ ] ¿El servidor inicia sin errores?
- [ ] ¿La cámara funciona?
- [ ] ¿La interfaz web carga?
- [ ] ¿Los logs no muestran errores críticos?

---

## 🎓 Buenas Prácticas

### 1. **Desarrollo Local**
```bash
# En MacBook Pro
cd /Users/feliperangel/Python/Pi_camara
source venv/bin/activate

# Editar código
# Ejecutar tests (los que no requieren hardware)
pytest tests/test_database.py
pytest tests/test_detection.py  # (con mocks)
```

### 2. **Deployment**
```bash
# Transferir cambios
./scripts/deploy_to_pi.sh 192.168.1.50 picamara picamara

# O si usas Git:
ssh picamara@192.168.1.50 'cd ~/Pi_camara && git pull'
```

### 3. **Testing en Producción**
```bash
# En Raspberry Pi
cd ~/Pi_camara
source venv/bin/activate
python scripts/test_camera_local.py
```

---

## 🔍 Archivos que NO se Sincronizan (y por qué)

| Archivo/Carpeta | ¿Por qué NO? |
|----------------|--------------|
| `venv/` | Cada ambiente tiene su propio entorno virtual con dependencias específicas |
| `data/episodes/` | Son archivos grandes, específicos de la ejecución en Pi |
| `data/videos/` | Videos generados, no necesarios en desarrollo |
| `logs/` | Logs de ejecución, específicos de producción |
| `*.db` | Base de datos SQLite con datos de producción |
| `__pycache__/` | Caché de Python, se regenera automáticamente |
| `.DS_Store` | Archivos del sistema macOS |

---

## 🚨 Problemas Comunes y Soluciones

### Problema 1: "Cambié código pero no se refleja en Pi"

**Solución:**
```bash
# Re-transferir código
./scripts/deploy_to_pi.sh 192.168.1.50 picamara picamara

# Reiniciar servidor en Pi
ssh picamara@192.168.1.50 'pkill -f run.py && cd ~/Pi_camara && nohup ./venv/bin/python3 run.py > logs/server.log 2>&1 &'
```

### Problema 2: "Dependencias diferentes entre ambientes"

**Solución:**
- Cada `venv/` es independiente
- Instalar dependencias en cada ambiente:
  ```bash
  # En MacBook Pro
  pip install -r requirements.txt
  
  # En Raspberry Pi
  ssh picamara@192.168.1.50 'cd ~/Pi_camara && source venv/bin/activate && pip install -r requirements.txt'
  ```

### Problema 3: "Configuración diferente"

**Solución:**
- Usar variables de entorno o archivos `.env`
- O mantener `config/camera_config.yaml` sincronizado pero con valores diferentes

---

## 📊 Resumen: Estrategia Implementada

### **Estrategia Final: Git como Fuente de Verdad** ✅

La estrategia implementada es **óptima y escalable** porque:

1. ✅ **Separación clara** entre desarrollo y producción
2. ✅ **Sincronización automática** con Git/GitHub
3. ✅ **Datos locales** donde deben estar (no se versionan)
4. ✅ **Independencia** de ambientes (cada uno tiene su venv)
5. ✅ **Versionado completo** con historial de cambios
6. ✅ **Backup automático** en GitHub

### **Repositorio GitHub**
- URL: https://github.com/felirangelp/picamara.git
- Branch principal: `main`
- Scripts de sincronización: `scripts/sync_*.sh`

---

## 🎯 Recomendación Final

**Mantén la estrategia actual** y considera agregar Git solo si:
- Trabajas en equipo
- Necesitas historial de versiones
- Quieres hacer rollbacks frecuentes

Para desarrollo individual, **rsync es suficiente y más simple**.

---

**Última actualización**: 2026-01-17  
**Siguiente revisión**: Cuando agregues Git o cambies la estrategia de deployment
