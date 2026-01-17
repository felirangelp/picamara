# Flujo de Trabajo con Git - MacBook + GitHub + Raspberry Pi

## 🎯 Estrategia: Desarrollo Híbrido con Git

```
MacBook Pro (Desarrollo)
    ↓ git push
GitHub (Repositorio Central)
    ↓ git pull
Raspberry Pi (Producción)
```

---

## 📝 Flujo de Trabajo Diario

### 1. Desarrollo en MacBook Pro

```bash
cd /Users/feliperangel/Python/Pi_camara

# Editar código...
# Probar localmente (tests unitarios)...

# Sincronizar con GitHub
./scripts/sync_to_github.sh
```

O manualmente:
```bash
git add .
git commit -m "feat: Descripción del cambio"
git push origin main
```

### 2. Actualizar Raspberry Pi

```bash
# Desde tu MacBook
./scripts/sync_from_github_pi.sh 192.168.1.50 picamara picamara
```

O manualmente desde la Pi:
```bash
ssh picamara@192.168.1.50
cd ~/Pi_camara
git pull origin main
```

### 3. Reiniciar Servidor (si es necesario)

```bash
ssh picamara@192.168.1.50 'pkill -f run.py && cd ~/Pi_camara && nohup ./venv/bin/python3 run.py > logs/server.log 2>&1 &'
```

---

## 🔧 Scripts Disponibles

### `scripts/sync_to_github.sh`
Sincroniza cambios locales con GitHub.

**Uso:**
```bash
./scripts/sync_to_github.sh
```

**Qué hace:**
1. Verifica estado de Git
2. Agrega todos los cambios
3. Crea commit (con mensaje automático o personalizado)
4. Hace push a GitHub

### `scripts/sync_from_github_pi.sh`
Actualiza código en Raspberry Pi desde GitHub.

**Uso:**
```bash
./scripts/sync_from_github_pi.sh [IP] [USER] [PASSWORD]
```

**Ejemplo:**
```bash
./scripts/sync_from_github_pi.sh 192.168.1.50 picamara picamara
```

**Qué hace:**
1. Verifica que el proyecto existe en Pi
2. Si no es Git, inicializa el repositorio
3. Hace `git pull` desde GitHub
4. Muestra el último commit

---

## 📋 Convenciones de Commits

Siguiendo el steering file (`.ai-steering.md`):

**Formato**: `type: descripción breve`

**Tipos:**
- `feat`: Nueva funcionalidad
- `fix`: Corrección de bug
- `docs`: Documentación
- `test`: Tests
- `refactor`: Refactorización
- `config`: Configuración

**Ejemplos:**
```bash
git commit -m "feat: Agregar detección de objetos"
git commit -m "fix: Corregir error en cálculo de FPS"
git commit -m "docs: Actualizar guía de deployment"
```

---

## 🚨 Resolución de Conflictos

### Si hay conflictos al hacer `git pull` en Pi:

```bash
# En Raspberry Pi
cd ~/Pi_camara
git stash  # Guardar cambios locales
git pull origin main
git stash pop  # Aplicar cambios locales de nuevo
# Resolver conflictos manualmente si es necesario
```

### Si necesitas descartar cambios locales en Pi:

```bash
# En Raspberry Pi
cd ~/Pi_camara
git reset --hard origin/main
```

**⚠️ CUIDADO**: Esto eliminará todos los cambios locales no commiteados.

---

## 📊 Estado del Repositorio

### Ver cambios pendientes (MacBook):
```bash
git status
git diff
```

### Ver historial:
```bash
git log --oneline -10
```

### Ver diferencias con GitHub:
```bash
git fetch origin
git log HEAD..origin/main
```

---

## 🔄 Flujo Completo de Ejemplo

### Escenario: Agregar nueva funcionalidad

1. **En MacBook - Desarrollo:**
   ```bash
   cd /Users/feliperangel/Python/Pi_camara
   # Editar src/detection/motion_detector.py
   # Probar cambios
   ./scripts/sync_to_github.sh
   ```

2. **En Raspberry Pi - Deployment:**
   ```bash
   ./scripts/sync_from_github_pi.sh 192.168.1.50 picamara picamara
   ```

3. **Reiniciar servidor:**
   ```bash
   ssh picamara@192.168.1.50 'pkill -f run.py && cd ~/Pi_camara && nohup ./venv/bin/python3 run.py > logs/server.log 2>&1 &'
   ```

4. **Verificar:**
   ```bash
   # Acceder a http://192.168.1.50:5000
   # Verificar que la nueva funcionalidad funciona
   ```

---

## 💡 Tips

1. **Commits frecuentes**: Haz commits pequeños y frecuentes
2. **Mensajes descriptivos**: Usa mensajes claros que expliquen el "qué" y "por qué"
3. **Pull antes de push**: Siempre haz `git pull` antes de `git push` si trabajas en equipo
4. **Branching**: Para features grandes, crea branches:
   ```bash
   git checkout -b feature/nueva-funcionalidad
   # ... trabajar ...
   git push origin feature/nueva-funcionalidad
   # Crear Pull Request en GitHub
   ```

---

## 🔗 Referencias

- **Repositorio GitHub**: https://github.com/felirangelp/picamara.git
- **Steering File**: `.ai-steering.md` (sección 11: Git y Versionado)
- **Ecosistema**: `docs/operations/ecosistema-proyecto.md`

---

**Última actualización**: 2026-01-17
