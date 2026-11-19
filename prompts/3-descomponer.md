# Fase 3: Descomponer

## Entrada

- AGENTS.md y docs/arquitectura.md.
- `specs/<NNN-nombre>/spec.md` y `plan.md`, ya aprobados.

## Produce

`specs/<NNN-nombre>/tasks.md` con este formato:

```markdown
# Tareas: <NNN> <nombre>

- [ ] T-01 <Título corto>
      Archivos: <rutas que se crean o cambian>
      Escenarios: <números de los escenarios de spec.md que atiende>
      Depende de: <T-xx o "ninguna">

- [ ] T-02 ...
```

## Reglas

- Cada tarea toca una sola clase o archivo y se puede revisar en pocos minutos.
- Ordenar de adentro hacia afuera según las capas: dominio, aplicación, infraestructura y composición.
- Todo escenario de spec.md aparece en al menos una tarea.
- Incluir tareas de seguridad y de manejo de errores cuando apliquen.
- La última tarea es la validación, que produce validacion.md.
- No escribir código.
- Al terminar, detenerse y esperar revisión.
