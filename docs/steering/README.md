# Steering Files - Reglas Inmutables

Esta carpeta contiene los **Steering Files** (Archivos de Dirección) del proyecto.

## Propósito

Los Steering Files actúan como la "constitución" del proyecto. Son reglas inmutables que gobiernan:
- El comportamiento del agente de IA
- Los estándares de código
- Las decisiones arquitectónicas
- Los patrones permitidos/prohibidos

## Documentos

### Steering File Principal

- **[ai-steering.md](ai-steering.md)** - Reglas inmutables de desarrollo
  - Principios de arquitectura
  - Estándares de código
  - Restricciones tecnológicas
  - Patrones prohibidos
  - Convenciones de nomenclatura
  - Requisitos de testing
  - Estándares de logging

## Inmutabilidad

Los Steering Files son **INMUTABLES** durante la fase de implementación.

**Solo pueden modificarse en**:
- Fase de Inception (cuando se definen requisitos)
- Fase de Construction (cuando se ajusta diseño)

**Proceso de modificación**:
1. Actualizar versión del steering file
2. Documentar razón del cambio
3. Obtener aprobación explícita
4. Actualizar referencias en código

## Uso

El agente de IA debe:
- **Consultar** steering files antes de generar código
- **Seguir** todas las reglas definidas
- **Documentar** cualquier excepción necesaria

Los desarrolladores deben:
- **Revisar** steering files antes de hacer cambios
- **Cumplir** con los estándares definidos
- **Reportar** inconsistencias encontradas

## Referencias

- **Steering File en raíz**: [../../.ai-steering.md](../../.ai-steering.md) (símbolo/referencia)
- **Requirements**: [../inception/requirements.md](../inception/requirements.md)
- **Design**: [../construction/design.md](../construction/design.md)

---

**Tipo**: Steering File  
**Estado**: Activo  
**Versión**: 1.0
