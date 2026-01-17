# Fase 1: Inception - Mob Elaboration

Esta carpeta contiene todos los documentos de la **Fase 1: Inception** del ciclo AI-DLC.

## Propósito

La fase de Inception es la más crítica en AI-DLC. Su objetivo es eliminar la ambigüedad en los requisitos y generar especificaciones formales y "computables" antes de escribir una sola línea de código.

## Ritual: Mob Elaboration

El ritual de **Mob Elaboration** (Elaboración en Grupo) incluye:

- **Actores**: Product Owner, Arquitecto, Desarrolladores Senior, Agente de IA
- **Entrada**: Intención de negocio de alto nivel
- **Proceso**:
  1. IA analiza intención y cruza con conocimiento existente
  2. IA genera preguntas aclaratorias proactivas
  3. Equipo humano responde refinando contexto
  4. IA genera artefactos detallados (historias, criterios, diagramas)
- **Salida**: Requisitos validados y computables

## Documentos

### Especificaciones Principales

- **[requirements.md](requirements.md)** - Especificaciones formales del sistema
  - Contexto del sistema
  - Actores
  - Requisitos funcionales (RF-001 a RF-010)
  - Requisitos no funcionales (RNF-001 a RNF-007)
  - Criterios de aceptación
  - Restricciones técnicas

### Especificaciones Detalladas

- **[specs/](specs/)** - Especificaciones técnicas detalladas
  - (Carpeta para futuras especificaciones más granulares)

## Principios

1. **No se escribe código** hasta que los requisitos estén aprobados
2. **Especificaciones formales** - Todo debe ser "computable"
3. **Validación humana** - Los humanos aprueban antes de continuar
4. **Inmutabilidad** - Una vez aprobados, los requisitos son inmutables durante implementación

## Referencias

- **Siguiente fase**: [../construction/README.md](../construction/README.md)
- **Steering File**: [../steering/ai-steering.md](../steering/ai-steering.md)
- **AI-DLC**: [../../AIDLC.pdf](../../AIDLC.pdf)

---

**Fase**: Inception  
**Ritual**: Mob Elaboration  
**Estado**: Completado
