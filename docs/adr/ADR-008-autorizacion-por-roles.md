# ADR-008: Permisos por rol y ámbito, manejados dentro del sistema

## Estado

Aceptado (2026-11-02)

## Contexto

Hay dos formas de entrar: el login institucional ([ADR-006](ADR-006-autenticacion-institucional.md)) y el enlace sin cuenta ([ADR-007](ADR-007-enlace-unico-supervisores.md)). Falta decidir cómo se controlan los permisos de los cinco roles: estudiante, docente asesor, director de programa, supervisor y administrador ([PA-02](../drivers.md#4-preocupaciones-arquitectónicas)).

Según [RN-01](../drivers.md#3-restricciones), los datos personales solo los puede ver quien esté autorizado: un docente ve solo a sus practicantes y un director solo las prácticas de su programa. Con [EAC-03](../drivers.md#eac-03-seguridad-confidencialidad-y-responsabilidad) el supervisor solo ve la práctica de su enlace. Y aprobar actas ([CU-10](../drivers.md#1-casos-de-uso-y-casos-de-uso-primarios)) o configurar reglas ([CU-12](../drivers.md#1-casos-de-uso-y-casos-de-uso-primarios)) son cosas de roles específicos.

## Alternativas consideradas

1. **Tomar los roles de los grupos del directorio institucional.** Todo se administraría en un solo lugar, pero el directorio no sabe quién es asesor de qué práctica ni director de qué programa, dependeríamos de que el Área de Sistemas cree grupos para nosotros, y no sirve para el supervisor porque no está en el directorio.
2. **Validar permisos en cada pantalla o controlador.** Es rápido para empezar, pero cada quien lo hace distinto, es fácil que se olvide una validación y no hay un lugar donde ver quién puede hacer qué.
3. **Roles con ámbito, asignados en el sistema y validados en cada caso de uso.** El rol dice qué puede hacer y el ámbito dice sobre qué (sus practicantes, su programa o la práctica del enlace). Sirve igual para los dos tipos de acceso y los permisos se pueden probar sin interfaz. Hay que construir la administración de roles.

## Decisión

Elegimos la opción 3. Las dos formas de entrar terminan en lo mismo: una sesión con quién es el usuario, qué rol tiene y cuál es su ámbito. Cada caso de uso valida el permiso antes de ejecutar, en la capa de negocio y no en la interfaz. Los roles de estudiante y docente salen de los datos del SIA, y los de director y administrador los asigna el administrador del sistema. Es la única opción que aplica RN-01 al nivel que se necesita (por práctica y por programa) y que también cubre al supervisor.

## Consecuencias

**Positivas:** hay un solo lugar para revisar y probar los permisos; las pruebas los cubren sin levantar la interfaz; cada acceso negado queda en la bitácora ([ADR-012](ADR-012-bitacora-auditoria.md)).

**Negativas:** hay que hacer una tabla de permisos y una pantalla para administrar roles. Todas las consultas tienen que filtrar por ámbito, lo que agrega condiciones (aunque con la carga de S-03 no se nota). Y si alguien deja de ser director, hay que quitarle el rol a mano.

**Riesgos:** que alguien cree un caso de uso nuevo y se le olvide validar permisos. Ponemos una prueba automática que falle si un caso de uso no declara qué permiso necesita.

**Vistas que modifica:** [Lógica](../vistas/01-logica.md), [Desarrollo](../vistas/03-desarrollo.md). Se ve en ESC-03 ([cu09-generar-acta](../diagramas/secuencias/cu09-generar-acta.puml)) y ESC-04 ([cu10-aprobar-acta](../diagramas/secuencias/cu10-aprobar-acta.puml)).
