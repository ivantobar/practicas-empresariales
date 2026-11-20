Este proyecto contiene la documentación y el código fuente del sistema. Su estructura permite organizar los archivos y facilitar la comprensión y el desarrollo.


- `docs/`: Documentación del proyecto, arquitectura, decisiones (ADR) y vistas (4+1). Los diagramas están en `docs/diagramas/` como archivos `.puml` y se ven en VS Code con la extensión PlantUML.
- `AGENTS.md`: Reglas que sigue el agente de IA (arquitectura, convenciones de código y forma de trabajar).
- `prompts/`: Prompts de cada fase de Spec Driven Development (arranque, especificar, planear, descomponer, implementar y validar).
- `specs/`: Una carpeta por caso de uso con `spec.md`, `plan.md`, `tasks.md` y `validacion.md`. Por ahora, `specs/001-postularse/` (CU-01).
- `src/`: Código fuente en Python, organizado con Clean Architecture en `dominio/`, `aplicacion/` e `infraestructura/`, y `main.py`, que arma el sistema.
- `estructura.txt`: Organización de carpetas y archivos.



Requisitos: Python 3.12 o superior. Solo usa la librería estándar, así que no hay que instalar nada.

Para ejecutar el proyecto desde Visual Studio Code:

1. Abrir la carpeta del proyecto.
2. Abrir una terminal en la raíz del proyecto (no dentro de `src`).
3. Ejecutar el siguiente comando:

```bash
python src/main.py
```

Ejecuta los 11 escenarios de `specs/001-postularse/spec.md` con datos de ejemplo y muestra `[cumple]` o `[NO cumple]` en cada verificación. Al final debe decir `Verificaciones cumplidas: 48 de 48`.

La documentación se encuentra en la carpeta `docs/`, donde se describen la arquitectura, la visión y las decisiones técnicas del sistema. El resultado de la validación está en `specs/001-postularse/validacion.md`.

