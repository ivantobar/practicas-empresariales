# AGENTS.md: Sistema de Gestión de Prácticas Empresariales

## Fuentes de verdad

- `docs/arquitectura.md`: mapa de la arquitectura (visión, drivers, ADR, vistas y glosario).
- `docs/drivers.md`, sección 1: catálogo de casos de uso. Es la lista de funcionalidades del sistema.
- `specs/`: una carpeta por caso de uso del catálogo, con el mismo número
  (`CU-03` → `specs/003-<nombre>/`), con `spec.md`, `plan.md`, `tasks.md` y `validacion.md`.
  La columna "Se especifica en" del catálogo enlaza cada caso de uso con su carpeta.
- Si el código contradice una especificación, gana la especificación.
- Si la especificación parece incorrecta o incompleta: detenerse y preguntar. No suponer.

## Arquitectura

- Estructura general: monolito modular con puertos y adaptadores (ver `docs/adr/ADR-001-monolito-modular.md`).
- Organización interna del código: Clean Architecture en tres capas dentro de `src/`: `dominio/`, `aplicacion/` e `infraestructura/`. `aplicacion/` se divide en los módulos de `docs/vistas/03-desarrollo.md` (`postulacion/`, `reglas/`, `pendientes/`, `bitacora/`, `acceso/`) y un módulo solo usa a otro si la vista de usos lo permite (ver `docs/adr/ADR-001-monolito-modular.md`).
- Regla de dependencia: `dominio/` no importa nada de `aplicacion/` ni de `infraestructura/`, y `aplicacion/` no importa nada de `infraestructura/`. Solo `main.py` conoce todo.
- Puertos: como `Protocol` en `aplicacion/<modulo>/puertos/`; los define el módulo que los necesita y los implementa `infraestructura/`.
- Integración con el SIA: solo por el puerto `ConsultaAcademica`, con espera máxima de 5 s, y nunca mientras el estudiante espera (ver `docs/adr/ADR-004-integracion-sia.md`). Toda llamada externa que pueda fallar es un `TrabajoPendiente` con reintentos (ver `docs/adr/ADR-005-reintentos-y-estados-pendientes.md`).
- Seguridad: la sesión llega validada (ADR-006) y cada caso de uso valida rol y ámbito (ADR-008). Cada cambio de estado y cada permiso negado va a la bitácora (ADR-012).
- Persistencia: base de datos relacional de código abierto del catálogo (ver `docs/adr/ADR-003-persistencia-relacional.md`). En esta etapa, adaptadores en memoria.
- No se usa ninguna tecnología, librería o componente que no esté en un ADR o en el plan de la funcionalidad.

## Convenciones de código

- Lenguaje: Python 3.12, solo la librería estándar. Se corre desde la raíz con `python src/main.py` y los imports son absolutos desde `src/`.
- Una clase por archivo.
- Sin archivos `__init__.py` (paquetes de espacio de nombres).
- DTO en la entrada y en la salida de los casos de uso.
- Nombres de clases, atributos y métodos según el glosario (sección 10 de `docs/arquitectura.md`).

## Forma de trabajar

- Una fase o una tarea por sesión.
- Ejecutar solo lo que pide el prompt de la fase indicada; no adelantar fases.
- Implementar una sola tarea de `tasks.md` a la vez.
- Al terminar: listar los archivos creados o cambiados, marcar la tarea y detenerse.
- No inventar requisitos: lo que no esté en los documentos se marca con
  `[NECESITA ACLARACIÓN: <pregunta>]` en `spec.md` o se pregunta.
- No modificar archivos de `docs/` salvo que la persona lo pida.
