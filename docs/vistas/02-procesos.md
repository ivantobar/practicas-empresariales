# Vista de procesos: contenedores

Diagrama: [../diagramas/02-procesos.puml](../diagramas/02-procesos.puml) (C4, nivel 2)

Para: integradores y el Área de Sistemas. Responde qué se ejecuta por separado, cómo se comunica y qué pasa cuando algo externo falla.

## 1. Presentación principal

Abrimos la caja del contexto. Adentro hay 4 contenedores. Ojo que aquí contenedor no quiere decir Docker: es cualquier cosa que corre o guarda datos por separado.

## 2. Catálogo de elementos

| Elemento | Responsabilidad | Tecnología | Se comunica con |
|---|---|---|---|
| Aplicación de prácticas | Páginas web y todos los casos de uso (monolito modular). Le responde al usuario sin esperar al SIA ni al correo | Lenguaje y framework del catálogo institucional (RT-04), imagen de contenedor (ADR-002) | Navegadores (HTTPS), Proveedor de identidad institucional (HTTPS), Base de datos de prácticas (SQL), Almacenamiento de documentos (archivos), SIA (HTTPS, solo para el acta) |
| Procesador de pendientes | Toma los trabajos pendientes cada minuto: verifica en el SIA, envía correos y reintenta con espera creciente. Si un trabajo lleva 24 h fallando lo marca "fallido" y avisa al administrador | La misma imagen de la Aplicación de prácticas con otro punto de entrada | Base de datos de prácticas (SQL), SIA (HTTPS), Servicio de correo institucional (SMTP) |
| Base de datos de prácticas | Prácticas, reglas versionadas, tabla de trabajos pendientes y bitácora de solo inserción | Motor relacional libre del catálogo (ADR-003) | Aplicación y Procesador (SQL) |
| Almacenamiento de documentos | Plantillas del acta con versión y PDF de las actas | Sistema de archivos con respaldo | Aplicación (lee y escribe) |

## 3. Justificación

- PA-01 y EAC-01, [ADR-001](../adr/ADR-001-monolito-modular.md): una sola aplicación, no microservicios. Con la carga de S-03 no hace falta más.
- EAC-02, PA-04, [ADR-004](../adr/ADR-004-integracion-sia.md) y [ADR-005](../adr/ADR-005-reintentos-y-estados-pendientes.md): la verificación en el SIA no la hace la Aplicación mientras el estudiante espera, la hace el Procesador de pendientes. Por eso la respuesta al estudiante no depende del SIA (menos de 3 s) y la postulación ya está guardada antes de llamar al SIA (0 perdidas). Elegimos una tabla en la base de datos y no un bróker de mensajes; por eso no aparece un contenedor de bróker.
- RT-03: solo la Aplicación y el Procesador hablan con el SIA, y siempre por sus servicios.
- RT-02, PA-02, [ADR-006](../adr/ADR-006-autenticacion-institucional.md): la Aplicación delega el inicio de sesión al Proveedor de identidad institucional.
- RT-04, RN-05, [ADR-003](../adr/ADR-003-persistencia-relacional.md): base de datos relacional libre del catálogo. Bitácora y pendientes viven ahí mismo, sin otra tecnología.
- RN-02, RN-03, [ADR-010](../adr/ADR-010-acta-desde-plantilla.md), [ADR-011](../adr/ADR-011-aprobacion-trazable-acta-inmutable.md): las plantillas y los PDF van en un almacenamiento aparte de la base, que aplica la política de conservación.
- EAC-03, [ADR-007](../adr/ADR-007-enlace-unico-supervisores.md), [ADR-012](../adr/ADR-012-bitacora-auditoria.md): el enlace inválido se registra en la bitácora en la misma petición; el aviso al docente lo manda el Procesador.

## 4. Comportamiento

Todos los escenarios de la [sección 6 de drivers.md](../drivers.md#6-escenarios-1) usan estos contenedores como participantes, con el mismo nombre. El más importante para esta vista es [cu01-postularse](../diagramas/secuencias/cu01-postularse.puml), donde se ve el loop del Procesador de pendientes cuando el SIA no responde.

## 5. Vistas relacionadas

- [Contexto](../contexto.md): de dónde salen los actores y los sistemas externos.
- [Desarrollo](03-desarrollo.md): cómo está organizada por dentro la Aplicación de prácticas.
- [Física](04-fisica.md): en qué servidor corre cada contenedor.
