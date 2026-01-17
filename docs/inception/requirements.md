# Especificación de Requisitos - Sistema de Seguridad Inteligente

## Documento de Especificación de Requisitos (AI-DLC - Fase 1: Inception)

**Versión**: 1.0  
**Fecha**: 2025-01-15  
**Estado**: Aprobado

---

## 1. Contexto del Sistema

### 1.1 Descripción General

Sistema de Seguridad Inteligente Escalable diseñado para Raspberry Pi 4 con cámara IMX219 8MP. El sistema detecta movimiento en tiempo real, almacena episodios automáticamente y proporciona una interfaz web para visualización y control remoto.

### 1.2 Objetivo del Sistema

Proporcionar un sistema de seguridad básico pero escalable que:
- Detecte movimiento en tiempo real usando algoritmos de visión por computadora
- Almacene episodios de video de forma estructurada para análisis futuro
- Permita acceso remoto vía interfaz web
- Siga metodología AI-DLC para desarrollo y mantenimiento

### 1.3 Alcance

**Incluye**:
- Detección de movimiento en tiempo real
- Almacenamiento automático de episodios
- Interfaz web para visualización
- API REST para consulta de datos
- Integración con LeRobotDataset para almacenamiento estructurado

**No incluye** (Fase 1):
- Reconocimiento de objetos específicos
- Alertas por email/SMS
- Múltiples cámaras simultáneas
- Análisis de video avanzado

---

## 2. Actores del Sistema

1. **Usuario Final (Local/Remoto)**: Persona que accede al sistema vía navegador web o SSH
2. **Sistema de Alertas**: Componente interno que registra eventos y genera logs
3. **LeRobotDataset**: Sistema de almacenamiento estructurado de episodios
4. **Navegador Web**: Cliente que consume la interfaz web y streaming de video

---

## 3. Requisitos Funcionales

### RF-001: Detección de Movimiento en Tiempo Real

**Descripción**: El sistema debe detectar movimiento en tiempo real usando algoritmo de diferencia de frames.

**Prioridad**: Alta

**Criterios de Aceptación**:
- CA-001.1: El sistema detecta movimiento cuando hay cambios significativos en la escena
- CA-001.2: La detección funciona con mínimo 15 FPS
- CA-001.3: El algoritmo es configurable (threshold, área mínima)
- CA-001.4: Los frames con movimiento detectado se anotan visualmente con rectángulos

**Entradas**:
- Stream de video desde cámara IMX219
- Parámetros de configuración (threshold, min_area)

**Salidas**:
- Indicador booleano de movimiento detectado
- Frame anotado con áreas de movimiento marcadas

---

### RF-002: Captura y Almacenamiento Automático de Episodios

**Descripción**: Cuando se detecta movimiento, el sistema debe capturar y almacenar automáticamente un episodio de video.

**Prioridad**: Alta

**Criterios de Aceptación**:
- CA-002.1: Un episodio se inicia automáticamente al detectar movimiento
- CA-002.2: El episodio se guarda cuando el movimiento cesa o alcanza duración máxima
- CA-002.3: Cada episodio tiene un identificador único
- CA-002.4: Los episodios se almacenan en formato compatible con LeRobotDataset

**Entradas**:
- Señal de movimiento detectado
- Frames de video capturados

**Salidas**:
- Archivo de episodio guardado en sistema de archivos
- Registro en base de datos con metadatos

---

### RF-003: Almacenamiento en Formato LeRobotDataset v3

**Descripción**: Los episodios deben almacenarse en formato LeRobotDataset v3 para compatibilidad futura con herramientas de ML.

**Prioridad**: Media

**Criterios de Aceptación**:
- CA-003.1: Cada episodio se guarda en estructura de carpetas compatible con LeRobotDataset
- CA-003.2: Los metadatos incluyen timestamp, duración, y flags de movimiento
- CA-003.3: El formato permite streaming y carga eficiente

**Entradas**:
- Frames de video del episodio
- Metadatos del episodio

**Salidas**:
- Estructura de directorios LeRobotDataset
- Archivos de metadatos en formato JSON

---

### RF-004: API REST FastAPI

**Descripción**: El sistema debe proporcionar una API REST usando FastAPI para consulta de metadatos, episodios y eventos.

**Prioridad**: Alta

**Criterios de Aceptación**:
- CA-004.1: Endpoint `/api/episodes` retorna lista de episodios con filtros
- CA-004.2: Endpoint `/api/events` retorna eventos recientes
- CA-004.3: Endpoint `/api/status` retorna estado del sistema
- CA-004.4: Endpoint `/api/config` permite actualizar configuración
- CA-004.5: Todos los endpoints retornan JSON válido
- CA-004.6: La API incluye documentación automática en `/docs`

**Endpoints Requeridos**:
- `GET /api/episodes?start_date=&end_date=&motion_only=`
- `GET /api/events?limit=`
- `GET /api/status`
- `POST /api/config`

---

### RF-005: Streaming de Video en Tiempo Real vía Web

**Descripción**: El sistema debe proporcionar streaming de video en tiempo real usando protocolo MJPEG accesible vía navegador web.

**Prioridad**: Alta

**Criterios de Aceptación**:
- CA-005.1: El stream está disponible en endpoint `/video_feed`
- CA-005.2: La latencia es menor a 500ms
- CA-005.3: El stream funciona en navegadores modernos (Chrome, Firefox, Safari)
- CA-005.4: El stream muestra frames anotados con detección de movimiento

**Entradas**:
- Frames capturados de la cámara
- Frames anotados con detección

**Salidas**:
- Stream MJPEG continuo

---

### RF-006: Interfaz Web Responsive con Dashboard

**Descripción**: El sistema debe proporcionar una interfaz web responsive con dashboard en tiempo real.

**Prioridad**: Alta

**Criterios de Aceptación**:
- CA-006.1: La interfaz es accesible desde navegador en `/`
- CA-006.2: El diseño es responsive (funciona en móvil y desktop)
- CA-006.3: El dashboard muestra stream de video en tiempo real
- CA-006.4: La interfaz se actualiza automáticamente sin recargar página

**Componentes Requeridos**:
- Stream de video en tiempo real
- Panel de estado del sistema
- Lista de episodios recientes
- Controles de configuración

---

### RF-007: Visualización de Estado y Controles

**Descripción**: La interfaz web debe mostrar estado de detección, contador de eventos y controles básicos.

**Prioridad**: Media

**Criterios de Aceptación**:
- CA-007.1: Indicador visual de movimiento detectado (rojo/verde)
- CA-007.2: Contador de detecciones de movimiento
- CA-007.3: Muestra FPS actual del sistema
- CA-007.4: Controles para ajustar parámetros de detección

**Información a Mostrar**:
- Estado: Movimiento detectado / Calmado
- Contador de detecciones
- FPS actual
- Timestamp del último evento

---

### RF-008: Sistema de Alertas y Logs Estructurados

**Descripción**: El sistema debe registrar eventos y generar logs estructurados.

**Prioridad**: Media

**Criterios de Aceptación**:
- CA-008.1: Todos los eventos se registran en base de datos
- CA-008.2: Los logs incluyen timestamp, tipo de evento y severidad
- CA-008.3: Los eventos son consultables vía API

**Tipos de Eventos**:
- `motion_detected`: Movimiento detectado
- `episode_started`: Inicio de episodio
- `episode_saved`: Episodio guardado
- `error`: Error del sistema

---

### RF-009: Acceso Remoto vía SSH y Navegador Web

**Descripción**: El sistema debe ser accesible remotamente vía SSH y navegador web.

**Prioridad**: Alta

**Criterios de Aceptación**:
- CA-009.1: Acceso SSH configurado y funcional
- CA-009.2: Acceso web disponible desde cualquier dispositivo en la red local
- CA-009.3: El sistema puede iniciarse/pararse remotamente
- CA-009.4: Los logs son accesibles remotamente

---

### RF-010: Configuración de Parámetros desde Interfaz Web

**Descripción**: Los parámetros de detección deben ser configurables desde la interfaz web.

**Prioridad**: Baja

**Criterios de Aceptación**:
- CA-010.1: Formulario web para ajustar threshold de movimiento
- CA-010.2: Formulario para ajustar área mínima de detección
- CA-010.3: Los cambios se aplican sin reiniciar el sistema
- CA-010.4: Los cambios se guardan en archivo de configuración

---

## 4. Requisitos No Funcionales

### RNF-001: Rendimiento

**Descripción**: El sistema debe mantener mínimo 15 FPS en detección de movimiento.

**Prioridad**: Alta

**Métricas**:
- FPS mínimo: 15
- FPS objetivo: 30
- CPU usage: < 80% en Raspberry Pi 4

---

### RNF-002: Latencia de Streaming

**Descripción**: La latencia del streaming web debe ser menor a 500ms.

**Prioridad**: Media

**Métricas**:
- Latencia máxima: 500ms
- Latencia objetivo: < 200ms

---

### RNF-003: Almacenamiento Eficiente

**Descripción**: El sistema debe gestionar almacenamiento de forma eficiente.

**Prioridad**: Alta

**Requisitos**:
- Videos guardados en sistema de archivos
- Metadatos en base de datos SQLite
- Organización por fecha (YYYY/MM/DD)
- Limpieza automática de episodios antiguos (opcional, futura fase)

---

### RNF-004: Compatibilidad de Navegadores

**Descripción**: La interfaz web debe funcionar en navegadores modernos.

**Prioridad**: Media

**Navegadores Soportados**:
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

---

### RNF-005: Accesibilidad Móvil

**Descripción**: La interfaz debe ser usable desde dispositivos móviles.

**Prioridad**: Media

**Requisitos**:
- Diseño responsive (mobile-first)
- Touch-friendly controls
- Optimización para pantallas pequeñas

---

### RNF-006: Seguridad Básica

**Descripción**: El sistema debe incluir medidas de seguridad básicas.

**Prioridad**: Baja (Fase 1)

**Requisitos**:
- Acceso web opcional con autenticación básica (futura fase)
- Validación de inputs en API
- Manejo seguro de errores (no exponer información sensible)

---

### RNF-007: Mantenibilidad

**Descripción**: El código debe seguir estándares de calidad y estructura.

**Prioridad**: Alta

**Requisitos**:
- Type hints en todas las funciones
- Docstrings en formato Google
- Separación de responsabilidades (módulos independientes)
- Código siguiendo .ai-steering.md

---

## 5. Restricciones Técnicas

1. **Hardware**: Raspberry Pi 4 (mínimo 4GB RAM recomendado)
2. **Cámara**: IMX219 8MP conectada vía CSI
3. **Sistema Operativo**: Raspberry Pi OS (64-bit)
4. **Python**: Versión 3.9 o superior
5. **Almacenamiento**: Limitado por tamaño de tarjeta SD/disco externo
6. **Red**: Requiere conexión a red local (WiFi o Ethernet)

---

## 6. Criterios de Aceptación Globales

1. ✅ **CA-001**: Sistema detecta movimiento y guarda episodios automáticamente
2. ✅ **CA-002**: Interfaz web muestra stream en tiempo real sin interrupciones
3. ✅ **CA-003**: Base de datos registra todos los eventos correctamente
4. ✅ **CA-004**: Sistema funciona de forma estable durante 24 horas continuas

---

## 7. Glosario

- **Episodio**: Secuencia de frames capturados durante un evento de movimiento
- **LeRobotDataset**: Formato de almacenamiento estructurado para datos de robótica
- **MJPEG**: Motion JPEG, protocolo de streaming de video
- **Threshold**: Umbral de diferencia de píxeles para detección de movimiento
- **Min Area**: Área mínima de contorno para considerar movimiento válido

---

## 8. Referencias

- Documento de Diseño: `docs/construction/design.md`
- Steering File: `docs/steering/ai-steering.md`
- Metodología AI-DLC: `AIDLC.pdf`

---

**Aprobado por**: [Pendiente]  
**Fecha de Aprobación**: [Pendiente]
