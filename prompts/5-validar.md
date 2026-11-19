# Fase 5: Validar

## Entrada

- AGENTS.md y docs/arquitectura.md.
- `specs/<NNN-nombre>/spec.md`, `plan.md` y `tasks.md`.
- El código implementado.

## Produce

`specs/<NNN-nombre>/validacion.md` con estas dos secciones:

```markdown
# Validación: <NNN> <nombre>

## Validación funcional

| Escenario | Resultado | Evidencia |
|-----------|-----------|-----------|
| <nombre del escenario> | Cumple o No cumple | <archivo, clase o método que lo demuestra, y cómo> |

## Validación arquitectónica

- Regla de dependencia: <cumple o no; si no, los imports que la violan>.
- ADR citados en plan.md: <dónde se ve cada uno en el código>.
- Convenciones de AGENTS.md: <cumple o no, con ejemplos>.
```

## Reglas

- Revisar escenario por escenario. Un escenario sin evidencia concreta se marca "No cumple".
- No corregir nada en esta fase: solo reportar.
- Para cada "No cumple", indicar si el problema está en el código o en la especificación.
- Al terminar, detenerse y esperar revisión.
