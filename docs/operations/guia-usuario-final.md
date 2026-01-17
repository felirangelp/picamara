# Guía de Usuario Final - Sistema de Seguridad Pi Camera

**Versión**: 1.0  
**Fecha**: 2026-01-17  
**Para**: Usuarios finales del sistema

---

## 🎯 ¿Qué es este sistema?

Es un sistema de seguridad inteligente que:
- 📹 **Graba video** desde una cámara en tiempo real
- 🔍 **Detecta movimiento** automáticamente
- 💾 **Guarda episodios** cuando hay movimiento
- 🌐 **Permite ver** todo desde tu navegador web

---

## 🚀 Cómo Acceder al Sistema

### Paso 1: Abrir el Navegador

1. Abre tu navegador favorito (Chrome, Firefox, Safari, Edge)
2. Ve a la siguiente dirección:

```
http://192.168.1.50:5000
```

**Nota**: Si la IP cambió, puedes encontrarla con:
```bash
ping picamara.local
```

### Paso 2: Ver la Interfaz

Deberías ver:
- **Stream de video en vivo** (parte superior)
- **Panel de estado** (movimiento, detecciones, FPS)
- **Lista de episodios** grabados
- **Controles de configuración**

---

## 📹 Cómo Usar el Sistema

### Ver el Video en Vivo

El stream de video aparece automáticamente en la parte superior de la pantalla. Deberías ver:
- La imagen de la cámara en tiempo real
- Rectángulos verdes alrededor de áreas con movimiento (cuando detecta algo)

### Monitorear el Estado

En el panel **"Estado del Sistema"** verás:

| Indicador | Qué Significa |
|-----------|---------------|
| **Movimiento** | Estado actual: "Calmado" (verde) o "¡MOVIMIENTO DETECTADO!" (rojo) |
| **Detecciones** | Número total de veces que se ha detectado movimiento |
| **FPS** | Frames por segundo (velocidad del video, ideal: 15-30) |
| **Uptime** | Tiempo que lleva el sistema funcionando |

### Ver Episodios Grabados

En el panel **"Episodios Recientes"** verás:
- Lista de grabaciones automáticas
- Cada episodio muestra:
  - **ID único**
  - **Fecha y hora** de inicio
  - **Duración** del episodio
  - **Estado** (movimiento detectado)

---

## ⚙️ Ajustar la Sensibilidad

### Panel de Configuración

Puedes ajustar cómo detecta el movimiento:

1. **Umbral de Movimiento** (Motion Threshold):
   - **Valor bajo (10-20)**: Muy sensible, detecta movimientos pequeños
   - **Valor medio (25-35)**: Sensibilidad normal (recomendado)
   - **Valor alto (40-60)**: Menos sensible, solo movimientos grandes

2. **Área Mínima** (Min Area):
   - **Valor bajo (200-500)**: Detecta objetos pequeños
   - **Valor medio (500-1000)**: Detecta objetos medianos (recomendado)
   - **Valor alto (1000-2000)**: Solo objetos grandes

3. **Aplicar cambios**:
   - Ajusta los valores
   - Haz clic en **"Actualizar Configuración"**
   - Los cambios se aplican inmediatamente

---

## 🧪 Pruebas Sugeridas

### Prueba 1: Verificación Básica (2 minutos)

1. ✅ Abre `http://192.168.1.50:5000`
2. ✅ Verifica que ves el video en vivo
3. ✅ Verifica que el estado muestra "Calmado" cuando no hay movimiento
4. ✅ Muévete frente a la cámara
5. ✅ Verifica que aparece "¡MOVIMIENTO DETECTADO!" y rectángulos verdes

### Prueba 2: Ajuste de Sensibilidad (3 minutos)

1. Configura **Umbral = 50** y **Área = 1000** (poco sensible)
2. Intenta movimientos pequeños → NO debería detectar
3. Haz movimientos grandes → SÍ debería detectar
4. Ajusta valores hasta encontrar tu configuración ideal

### Prueba 3: Episodios Automáticos (5 minutos)

1. Genera varios movimientos seguidos
2. Observa cómo se crean episodios en la lista
3. Verifica que el contador de detecciones aumenta
4. Revisa que los episodios tienen fecha y hora correctas

---

## 🔧 Solución de Problemas

### Problema: "No veo el video"

**Soluciones:**
1. Verifica que el servidor esté corriendo:
   ```bash
   ssh picamara@192.168.1.50 'ps aux | grep run.py'
   ```
2. Si no está corriendo, inícialo:
   ```bash
   ssh picamara@192.168.1.50 'cd ~/Pi_camara && nohup ./venv/bin/python3 run.py > logs/server.log 2>&1 &'
   ```
3. Refresca el navegador (F5 o Cmd+R)

### Problema: "No detecta movimiento"

**Soluciones:**
1. Reduce el **Umbral** a 20
2. Reduce el **Área Mínima** a 300
3. Asegúrate de tener buena iluminación
4. Muévete más lentamente o con movimientos más grandes

### Problema: "Detecta demasiado (muy sensible)"

**Soluciones:**
1. Aumenta el **Umbral** a 40-50
2. Aumenta el **Área Mínima** a 1000-1500
3. Verifica que no haya luces parpadeantes o sombras moviéndose

### Problema: "La página no carga"

**Soluciones:**
1. Verifica la IP: `ping picamara.local`
2. Verifica que estés en la misma red WiFi/Ethernet
3. Verifica el puerto: `http://192.168.1.50:5000`
4. Revisa el firewall de tu router

---

## 📊 Interpretando los Indicadores

### Indicadores Visuales

| Símbolo/Color | Significado |
|---------------|-------------|
| 🟢 **Verde** | Sistema funcionando correctamente |
| 🔴 **Rojo** | Movimiento detectado o error |
| ⚪ **Gris** | Sistema inactivo o desconectado |

### Valores Típicos

| Métrica | Valor Normal | Qué Hacer si es Diferente |
|---------|--------------|---------------------------|
| **FPS** | 15-30 fps | Si es < 10: Problema de rendimiento |
| **Uptime** | Aumenta continuamente | Si se resetea: Servidor se reinició |
| **Detecciones** | Aumenta con movimiento | Si no aumenta: Revisar sensibilidad |

---

## 🎯 Casos de Uso Comunes

### Caso 1: Monitoreo de Entrada

**Configuración recomendada:**
- Umbral: 30
- Área Mínima: 800

**Qué verás:**
- Detección cuando alguien entra por la puerta
- Episodios automáticos guardados
- Notificación visual en tiempo real

### Caso 2: Monitoreo de Patio/Exterior

**Configuración recomendada:**
- Umbral: 40 (menos sensible para evitar falsos positivos)
- Área Mínima: 1200

**Qué verás:**
- Detección de personas o vehículos
- Menos falsos positivos por hojas o sombras

### Caso 3: Monitoreo de Objetos Pequeños

**Configuración recomendada:**
- Umbral: 20
- Área Mínima: 300

**Qué verás:**
- Detección de mascotas pequeñas
- Movimientos sutiles

---

## 📱 Acceso desde Móvil

El sistema es **responsive** y funciona en móviles:

1. Conéctate a la misma red WiFi
2. Abre el navegador en tu móvil
3. Ve a: `http://192.168.1.50:5000`
4. La interfaz se adaptará automáticamente

---

## 🔐 Seguridad

**Nota importante**: Actualmente el sistema **NO tiene autenticación**. Cualquiera en tu red puede acceder.

**Recomendaciones:**
- Usa solo en redes de confianza
- Considera agregar autenticación básica en el futuro
- No expongas el puerto 5000 a internet sin protección

---

## 📞 Comandos Útiles (Para Usuarios Avanzados)

### Ver Estado del Sistema vía API

```bash
curl http://192.168.1.50:5000/api/status
```

### Ver Episodios

```bash
curl http://192.168.1.50:5000/api/episodes
```

### Ver Logs del Sistema

```bash
ssh picamara@192.168.1.50 'tail -f ~/Pi_camara/logs/server.log'
```

---

## ✅ Checklist de Verificación

Antes de usar el sistema, verifica:

- [ ] Puedo acceder a `http://192.168.1.50:5000`
- [ ] Veo el stream de video en vivo
- [ ] El panel de estado muestra información
- [ ] El indicador de estado está en verde
- [ ] Puedo moverme y ver detección de movimiento
- [ ] Los episodios se crean automáticamente

---

## 🎓 Tips y Mejores Prácticas

1. **Iluminación**: Mejor iluminación = mejor detección
2. **Ángulo de cámara**: Apunta hacia áreas de interés
3. **Configuración inicial**: Empieza con valores por defecto y ajusta según necesidad
4. **Monitoreo regular**: Revisa los episodios periódicamente
5. **Mantenimiento**: Reinicia el servidor si notas problemas de rendimiento

---

## 📖 Referencias

- **Documentación técnica**: `docs/construction/design.md`
- **Guía de conexión**: `docs/operations/connection-guide.md`
- **Troubleshooting**: `docs/operations/testing-guide.md`

---

**¡Disfruta de tu sistema de seguridad inteligente!** 🎉
