# Fase 2: Planear

## Entrada

- AGENTS.md y docs/arquitectura.md.
- `specs/<NNN-nombre>/spec.md`, ya aprobado y sin marcas `[NECESITA ACLARACIÓN]`.
- Los ADR, las vistas y los diagramas de secuencia que enlaza docs/arquitectura.md.

## Produce

`specs/<NNN-nombre>/plan.md` con estas secciones:

```markdown
# Plan: <NNN> <nombre>

## Decisiones que aplican
<ADR por su ID y qué implica cada uno para esta funcionalidad>

## Componentes
<Según vistas/03-desarrollo.md: archivos y clases que se crean o cambian, agrupados por capa>

## Flujo
<Diagrama de secuencia que se sigue, si existe: diagramas/secuencias/...>

## Datos
<Entidades del modelo de dominio que intervienen>

## Fuera de alcance
<Lo que esta funcionalidad no hace>

## Decisiones pendientes
<Solo si hace falta una decisión que no está en ningún ADR>
```

## Reglas

- Si spec.md todavía tiene marcas `[NECESITA ACLARACIÓN]`, no planear: avisar y detenerse.
- El plan aterriza la arquitectura existente en esta funcionalidad; no la rediseña.
- Solo componentes que existan en las vistas y tecnologías aprobadas en un ADR.
- Si hace falta una decisión que no existe, no tomarla: registrarla en "Decisiones pendientes" y detenerse.
- Cada escenario de spec.md debe quedar cubierto por al menos un componente.
- No escribir código.
- Al terminar, detenerse y esperar revisión.
