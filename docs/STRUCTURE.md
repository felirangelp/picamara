# Estructura de Documentación AI-DLC

## 📁 Organización Completa

```
docs/
├── README.md                    # Índice principal de documentación
│
├── inception/                   # 🔵 FASE 1: INCEPTION
│   ├── README.md               # Guía de la fase
│   ├── requirements.md         # Especificaciones formales
│   └── specs/                  # Especificaciones detalladas (futuro)
│
├── construction/                # 🟢 FASE 2: CONSTRUCTION
│   ├── README.md               # Guía de la fase
│   ├── design.md               # Diseño técnico completo
│   └── architecture/           # Documentos de arquitectura (futuro)
│
├── operations/                  # 🟡 FASE 3: OPERATIONS
│   ├── README.md               # Guía de la fase
│   ├── raspberry-pi-setup.md   # Configuración hardware
│   ├── connection-guide.md     # Conexión remota
│   └── testing-guide.md       # Guía de pruebas
│
└── steering/                    # ⚪ STEERING FILES
    ├── README.md               # Guía de steering files
    └── ai-steering.md          # Reglas inmutables
```

## 🎯 Flujo AI-DLC

```
INCEPTION (Mob Elaboration)
    ↓
    requirements.md
    ↓
CONSTRUCTION (Mob Construction)
    ↓
    design.md
    ↓
IMPLEMENTATION
    ↓
    src/ (código)
    ↓
OPERATIONS
    ↓
    Guías operacionales
```

## 📋 Mapeo de Documentos

| Documento Original | Nueva Ubicación | Fase AI-DLC |
|-------------------|-----------------|-------------|
| `requirements.md` | `docs/inception/requirements.md` | Inception |
| `design.md` | `docs/construction/design.md` | Construction |
| `raspberry-pi-setup.md` | `docs/operations/raspberry-pi-setup.md` | Operations |
| `connection-guide.md` | `docs/operations/connection-guide.md` | Operations |
| `testing-guide.md` | `docs/operations/testing-guide.md` | Operations |
| `.ai-steering.md` | `docs/steering/ai-steering.md` | Steering |

## 🔗 Referencias Actualizadas

Todas las referencias entre documentos han sido actualizadas para reflejar la nueva estructura organizada según AI-DLC.

## 📖 Cómo Navegar

1. **Empezar**: `README.md` (raíz del proyecto)
2. **Índice**: `docs/README.md`
3. **Por fase**: Navegar a `inception/`, `construction/`, `operations/`
4. **Steering**: `steering/ai-steering.md`

---

**Última actualización**: 2025-01-17
