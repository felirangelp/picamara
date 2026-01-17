# Documentación del Proyecto - AI-DLC

Este directorio contiene toda la documentación del Sistema de Seguridad Inteligente, organizada según la metodología **AI-Driven Development Lifecycle (AI-DLC)**.

## 📚 Estructura AI-DLC

La documentación está organizada en las tres fases principales del AI-DLC:

```
docs/
├── README.md                    # Este archivo (índice)
├── inception/                   # Fase 1: Inception - Mob Elaboration
│   ├── requirements.md         # Especificaciones formales
│   └── specs/                  # Especificaciones detalladas
├── construction/                # Fase 2: Construction - Mob Construction
│   ├── design.md               # Diseño técnico completo
│   └── architecture/           # Documentos de arquitectura
├── operations/                  # Fase 3: Operations
│   ├── raspberry-pi-setup.md   # Configuración hardware
│   ├── connection-guide.md     # Conexión remota
│   └── testing-guide.md        # Guía de pruebas
└── steering/                    # Steering Files (reglas inmutables)
    └── ai-steering.md          # Reglas de desarrollo
```

## 🎯 Fase 1: Inception (Mob Elaboration)

**Propósito**: Definir requisitos formales y especificaciones computables antes de escribir código.

### Documentos

- **[inception/requirements.md](inception/requirements.md)** - Especificaciones formales del sistema
  - Requisitos funcionales (RF)
  - Requisitos no funcionales (RNF)
  - Criterios de aceptación
  - Restricciones técnicas
  - Actores del sistema

### Ritual: Mob Elaboration

En esta fase, la IA analiza la intención de negocio y genera:
- Historias de usuario
- Criterios de aceptación
- Diagramas de flujo
- Preguntas aclaratorias

**Salida**: Requisitos validados y "computables" - NO se escribe código hasta aprobación.

## 🔨 Fase 2: Construction (Mob Construction)

**Propósito**: Diseño técnico detallado y planificación antes de la implementación.

### Documentos

- **[construction/design.md](construction/design.md)** - Diseño técnico completo
  - Arquitectura del sistema
  - Stack tecnológico
  - Modelos de datos
  - APIs y endpoints
  - Flujos de datos
  - Diagramas de componentes

### Ritual: Mob Construction

En esta fase, la IA propone:
- Arquitectura técnica
- Estructura de módulos
- Decisiones de diseño
- Plan de implementación

**Salida**: Diseño técnico aprobado - Base para implementación.

## ⚙️ Fase 3: Operations

**Propósito**: Guías operacionales, configuración y mantenimiento del sistema.

### Documentos

- **[operations/raspberry-pi-setup.md](operations/raspberry-pi-setup.md)** - Configuración inicial de Raspberry Pi
- **[operations/connection-guide.md](operations/connection-guide.md)** - Guía de conexión remota
- **[operations/testing-guide.md](operations/testing-guide.md)** - Guía de pruebas y verificación

## 📋 Steering Files

**Propósito**: Reglas inmutables y constitución del proyecto.

### Documentos

- **[steering/ai-steering.md](steering/ai-steering.md)** - Reglas inmutables de desarrollo
  - Principios de arquitectura
  - Estándares de código
  - Restricciones tecnológicas
  - Patrones prohibidos

**Nota**: El archivo `.ai-steering.md` en la raíz es una copia/símbolo del steering file principal.

## 📖 Documentos en la Raíz del Proyecto

Los siguientes documentos permanecen en la raíz por convención:

- **[../README.md](../README.md)** - Documentación principal del proyecto (estándar)
- **[../.ai-steering.md](../.ai-steering.md)** - Steering file (archivo de configuración del agente)

## 📝 Orden de Lectura Recomendado

### Para Desarrolladores Nuevos

1. **[../README.md](../README.md)** - Visión general del proyecto
2. **[inception/requirements.md](inception/requirements.md)** - Qué hace el sistema
3. **[construction/design.md](construction/design.md)** - Cómo está construido
4. **[steering/ai-steering.md](steering/ai-steering.md)** - Reglas de desarrollo
5. **[operations/raspberry-pi-setup.md](operations/raspberry-pi-setup.md)** - Configuración

### Para Operadores/Usuarios

1. **[../README.md](../README.md)** - Inicio rápido
2. **[operations/raspberry-pi-setup.md](operations/raspberry-pi-setup.md)** - Instalación
3. **[operations/connection-guide.md](operations/connection-guide.md)** - Acceso remoto
4. **[operations/testing-guide.md](operations/testing-guide.md)** - Verificación

## 🔄 Metodología AI-DLC

Este proyecto sigue estrictamente la metodología **AI-Driven Development Lifecycle**:

### Fases del Ciclo

```
┌─────────────────────────────────────────┐
│  Fase 1: INCEPTION                     │
│  Mob Elaboration                       │
│  → requirements.md                     │
│  → Especificaciones formales           │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│  Fase 2: CONSTRUCTION                   │
│  Mob Construction                       │
│  → design.md                            │
│  → Arquitectura técnica                 │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│  Fase 3: IMPLEMENTATION                 │
│  → Código fuente (src/)                │
│  → Tests (tests/)                       │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│  Fase 4: OPERATIONS                     │
│  → Guías operacionales                  │
│  → Deployment                           │
└─────────────────────────────────────────┘
```

### Principios Clave

1. **Inmutabilidad**: Los documentos de Inception y Construction son inmutables durante implementación
2. **Especificaciones Formales**: Todo debe estar especificado antes de codificar
3. **Steering Files**: Reglas que gobiernan el comportamiento del agente de IA
4. **Trazabilidad**: Cada decisión debe estar documentada y referenciable

## 🔗 Referencias

- **AI-DLC Methodology**: `../AIDLC.pdf` - Documento completo de la metodología
- **Steering File**: `steering/ai-steering.md` - Reglas inmutables
- **Requirements**: `inception/requirements.md` - Especificaciones
- **Design**: `construction/design.md` - Diseño técnico

## 📌 Notas Importantes

- **No modificar** documentos de Inception/Construction sin proceso formal
- **Consultar** steering files antes de hacer cambios
- **Seguir** el orden de fases: Inception → Construction → Implementation
- **Documentar** cualquier excepción a las reglas

---

**Última actualización**: 2025-01-17  
**Metodología**: AI-DLC v1.0  
**Estado**: Activo
