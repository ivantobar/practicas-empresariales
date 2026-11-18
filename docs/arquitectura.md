# Documento de arquitectura: Sistema de Gestión de Prácticas Empresariales

> Versión 0.4 | Estado: listo para SDD (la sección 9 se sigue llenando con la deuda que aparezca al implementar)

Este documento es el mapa del proyecto. Enlaza a los demás archivos de `docs/` y no los copia, porque un dato escrito en dos lugares termina diciendo dos cosas distintas. La estructura es una adaptación de arc42. Junto con [AGENTS.md](../AGENTS.md) es lo primero que lee el agente en cada sesión.

## 1. Introducción y objetivos

El sistema reemplaza el Excel y el correo con los que la Facultad de Ingenierías gestiona las prácticas empresariales de 500 estudiantes al año y 50 docentes asesores: postulación, asignación del docente asesor, horas, evaluación de la empresa y acta final. Los seis objetivos de negocio (OB-01 a OB-06) apuntan a entregar el acta en 5 días hábiles, recibir a tiempo las evaluaciones, quitarle trabajo de consolidación al docente asesor, bajar los errores del acta, aplicar reglas nuevas sin parar la operación y responder auditorías en 1 día.

Detalle: [Visión](vision.md)

Funcionalidades: [catálogo de casos de uso](drivers.md#1-casos-de-uso-y-casos-de-uso-primarios) (CU-01 a CU-15). La columna "Se especifica en" enlaza cada caso de uso con su carpeta de [`specs/`](../specs/).

## 2. Restricciones

Nueve restricciones: infraestructura de la Universidad (RT-01), cuenta institucional (RT-02), datos académicos solo por los servicios del SIA (RT-03), tecnologías del catálogo institucional (RT-04), Ley 1581 (RN-01), retención documental (RN-02), formato oficial del acta (RN-03), supervisores sin cuenta (RN-04) y nada de licencias de pago recurrente (RN-05).

Detalle: [Restricciones](drivers.md#3-restricciones)

## 3. Contexto del sistema

El sistema se relaciona con 5 tipos de persona (estudiante, docente asesor, director de programa, supervisor de empresa y administrador del sistema) y 3 sistemas externos (SIA, proveedor de identidad institucional y servicio de correo).

Detalle: [Contexto](contexto.md) y su diagrama [diagramas/contexto.puml](diagramas/contexto.puml)

## 4. Estrategia de solución

Las decisiones de alto nivel: la estructura general (PA-01) y lo que decidimos para cumplir los escenarios de calidad. El resto de decisiones está en la [sección 7](#7-decisiones-de-diseño).

| Driver | Enfoque | ADR |
|---|---|---|
| PA-01, EAC-01 | Monolito modular con puertos y adaptadores: un módulo por tema de negocio y dependencias que apuntan hacia el dominio | [ADR-001](adr/ADR-001-monolito-modular.md) |
| RT-01, RN-01 | Contenedores en la infraestructura de la Universidad | [ADR-002](adr/ADR-002-despliegue-institucional.md) |
| RT-04, RN-05 | Base de datos relacional de código abierto del catálogo | [ADR-003](adr/ADR-003-persistencia-relacional.md) |
| CU-01, EAC-02, RT-03 | El SIA queda detrás de un adaptador; la postulación se guarda primero y se verifica después | [ADR-004](adr/ADR-004-integracion-sia.md) |
| PA-04, EAC-02 | Toda llamada externa que puede fallar es un trabajo pendiente en la base de datos, con reintentos de espera creciente | [ADR-005](adr/ADR-005-reintentos-y-estados-pendientes.md) |
| CU-07, EAC-03, RN-04 | Enlace de un solo uso que vence a los 15 días para los supervisores | [ADR-007](adr/ADR-007-enlace-unico-supervisores.md) |
| CU-12, EAC-01 | Reglas por programa como datos versionados, con validadores intercambiables | [ADR-009](adr/ADR-009-reglas-configurables-por-programa.md) |
| PA-03, EAC-03 | Bitácora de solo inserción en la misma transacción del evento | [ADR-012](adr/ADR-012-bitacora-auditoria.md) |

## 5. Vistas (4+1)

Usamos el modelo 4+1. Cada vista está en [`vistas/`](vistas/) y su diagrama tiene el mismo nombre en [`diagramas/`](diagramas/) (archivos `.puml`, se ven en VS Code con la extensión PlantUML). Cada una tiene sus 5 partes: diagrama, catálogo, justificación, comportamiento y vistas relacionadas.

| Vista | Para quién | Notación | Documento | Diagrama |
|---|---|---|---|---|
| Contexto (marco) | Todos | C4 nivel 1 | [contexto.md](contexto.md) | [contexto.puml](diagramas/contexto.puml) |
| Lógica | Usuarios y analistas | UML, modelo de dominio | [01-logica.md](vistas/01-logica.md) | [01-logica.puml](diagramas/01-logica.puml) |
| Procesos | Integradores | C4 nivel 2, contenedores | [02-procesos.md](vistas/02-procesos.md) | [02-procesos.puml](diagramas/02-procesos.puml) |
| Desarrollo | Programadores | C4 nivel 3, componentes y vista de usos | [03-desarrollo.md](vistas/03-desarrollo.md) | [03-desarrollo.puml](diagramas/03-desarrollo.puml) |
| Física | Área de Sistemas | C4 despliegue | [04-fisica.md](vistas/04-fisica.md) | [04-fisica.puml](diagramas/04-fisica.puml) |
| +1 Escenarios | Todos, para validar | UML secuencia arquitectónica | [drivers.md, sección 6](drivers.md#6-escenarios-1) | [secuencias/](diagramas/secuencias/) |

### Matriz de cobertura: drivers y ADR por vista

Revisamos que ningún driver ni ADR quedara sin verse en alguna vista. No hay filas vacías.

| Driver o ADR | Contexto | Lógica | Procesos | Desarrollo | Física | Escenario |
|---|:-:|:-:|:-:|:-:|:-:|:-:|
| CU-01 Postularse | ✓ | ✓ | ✓ | ✓ | | ESC-01 |
| CU-07 Evaluar al practicante | ✓ | ✓ | ✓ | ✓ | | ESC-02 |
| CU-09 Generar el acta | ✓ | ✓ | ✓ | ✓ | | ESC-03 |
| CU-10 Aprobar el acta | ✓ | ✓ | | ✓ | | ESC-04 |
| CU-12 Configurar reglas | ✓ | ✓ | | ✓ | | ESC-05 |
| EAC-01 Mantenibilidad (16 h, 2 módulos, 0 prácticas afectadas) | | ✓ | | ✓ | | ESC-05 |
| EAC-02 Fiabilidad (SIA caído, 0 postulaciones perdidas) | | ✓ | ✓ | ✓ | ✓ | ESC-01 |
| EAC-03 Seguridad (enlace inválido rechazado y registrado) | ✓ | ✓ | ✓ | ✓ | | ESC-02 |
| RT-01 Infraestructura de la Universidad | | | | | ✓ | |
| RT-02 Cuenta institucional | ✓ | | ✓ | ✓ | ✓ | |
| RT-03 Solo servicios del SIA | ✓ | | ✓ | ✓ | ✓ | ESC-01 |
| RT-04 Catálogo institucional | | | ✓ | | ✓ | |
| RN-01 Ley 1581 | | ✓ | | ✓ | ✓ | |
| RN-02 Retención documental | | ✓ | ✓ | | ✓ | ESC-04 |
| RN-03 Formato del acta | | ✓ | ✓ | ✓ | | ESC-03 |
| RN-04 Supervisores sin cuenta | ✓ | ✓ | | ✓ | | ESC-02 |
| RN-05 Sin licencias pagas | | | ✓ | ✓ | ✓ | |
| PA-01 Estructura general | | | ✓ | ✓ | | |
| PA-02 Autenticación y autorización | ✓ | ✓ | ✓ | ✓ | | ESC-02, ESC-04 |
| PA-03 Registro y trazabilidad | | ✓ | ✓ | ✓ | | ESC-02 |
| PA-04 Manejo de fallas | | | ✓ | ✓ | ✓ | ESC-01 |
| PA-05 Migración inicial | ✓ | | | ✓ | | |
| ADR-001 Monolito modular | | | ✓ | ✓ | ✓ | |
| ADR-002 Despliegue con contenedores | | | | | ✓ | |
| ADR-003 Base de datos relacional | | | ✓ | ✓ | ✓ | |
| ADR-004 Integración con el SIA | ✓ | ✓ | ✓ | ✓ | | ESC-01 |
| ADR-005 Cola de pendientes | | | ✓ | ✓ | ✓ | ESC-01 |
| ADR-006 Login institucional | ✓ | | ✓ | ✓ | ✓ | |
| ADR-007 Enlace para supervisores | ✓ | ✓ | | ✓ | | ESC-02 |
| ADR-008 Roles con ámbito | | ✓ | | ✓ | | ESC-03, ESC-04 |
| ADR-009 Reglas por programa | | ✓ | | ✓ | | ESC-05 |
| ADR-010 Acta desde plantilla | | ✓ | ✓ | ✓ | | ESC-03 |
| ADR-011 Acta que no se modifica | | ✓ | ✓ | | ✓ | ESC-04 |
| ADR-012 Bitácora | | ✓ | ✓ | ✓ | | ESC-02 |
| ADR-013 Migración desde Excel | ✓ | | | ✓ | | |

## 6. Conceptos transversales

Son las preocupaciones arquitectónicas de [drivers.md, sección 4](drivers.md#4-preocupaciones-arquitectónicas) ya resueltas. Si un desarrollador (o el agente) tiene que tocar alguna de estas cosas, lo hace como dice aquí y no a su manera.

| Concepto | Cómo se resuelve | Dónde se ve |
|---|---|---|
| Estructura general (PA-01) | Capas `dominio/`, `aplicacion/` e `infraestructura/`; `aplicacion/` dividida en los módulos de la vista de desarrollo. `dominio/` no importa nada de afuera y los módulos solo se usan según la vista de usos | [ADR-001](adr/ADR-001-monolito-modular.md), [Desarrollo](vistas/03-desarrollo.md) |
| Autenticación y autorización (PA-02) | Los internos entran con la cuenta institucional y los supervisores con enlace de un solo uso. Las dos formas terminan en una sesión con usuario, rol y ámbito, y cada caso de uso valida el permiso antes de ejecutar | [ADR-006](adr/ADR-006-autenticacion-institucional.md), [ADR-007](adr/ADR-007-enlace-unico-supervisores.md), [ADR-008](adr/ADR-008-autorizacion-por-roles.md) |
| Registro y trazabilidad (PA-03) | Evento de bitácora con quién, qué, sobre qué, cuándo y desde dónde, sin copiar datos personales. Se registran los cambios de estado y los permisos negados | [ADR-012](adr/ADR-012-bitacora-auditoria.md), [Lógica](vistas/01-logica.md) |
| Manejo de fallas de integración (PA-04) | La llamada al SIA o al correo se guarda como trabajo pendiente junto con el dato. El Procesador de pendientes reintenta cada minuto con espera de 1, 2, 4, 8 y máximo 15 min; a las 24 h el trabajo queda "fallido" y se avisa al administrador | [ADR-005](adr/ADR-005-reintentos-y-estados-pendientes.md), [Procesos](vistas/02-procesos.md), ESC-01 |
| Integración con el SIA | Solo por el puerto ConsultaAcademica, con espera máxima de 5 s. El adaptador traduce las fallas a un error de aplicación | [ADR-004](adr/ADR-004-integracion-sia.md), [Desarrollo](vistas/03-desarrollo.md) |
| Configuración de reglas | Las reglas son datos versionados por programa y cada postulación guarda la versión con la que se hizo | [ADR-009](adr/ADR-009-reglas-configurables-por-programa.md), ESC-05 |
| Migración inicial (PA-05) | Plantilla Excel estándar y un importador que valida, dentro del Módulo Administración | [ADR-013](adr/ADR-013-migracion-desde-excel.md) |
| Despliegue | Imagen de contenedor en una máquina virtual de la Universidad; el Procesador de pendientes es la misma imagen con otro punto de entrada | [ADR-002](adr/ADR-002-despliegue-institucional.md), [Física](vistas/04-fisica.md) |

## 7. Decisiones de diseño

Las decisiones están en la carpeta [`adr/`](adr/), un archivo por decisión. Si alguna cambia no se edita el ADR, se hace uno nuevo que lo reemplace. Cada ADR dice al final qué vistas modifica, y la [matriz de la sección 5](#matriz-de-cobertura-drivers-y-adr-por-vista) muestra dónde se ve cada uno.

| ADR | Decisión | Estado | Drivers |
|---|---|---|---|
| [ADR-001](adr/ADR-001-monolito-modular.md) | Monolito modular con puertos y adaptadores | Aceptado | PA-01, EAC-01 |
| [ADR-002](adr/ADR-002-despliegue-institucional.md) | Despliegue con contenedores en los servidores de la Universidad | Aceptado | RT-01, RN-01 |
| [ADR-003](adr/ADR-003-persistencia-relacional.md) | Base de datos relacional de código abierto del catálogo institucional | Aceptado | RT-04, RN-05 |
| [ADR-004](adr/ADR-004-integracion-sia.md) | Integración con el SIA por un adaptador y verificación diferida | Aceptado | CU-01, EAC-02, RT-03 |
| [ADR-005](adr/ADR-005-reintentos-y-estados-pendientes.md) | Cola de trabajos pendientes en la base de datos para las fallas de integración | Aceptado | PA-04, EAC-02 |
| [ADR-006](adr/ADR-006-autenticacion-institucional.md) | Login con la cuenta institucional a través del proveedor de la Universidad | Aceptado | RT-02, PA-02 |
| [ADR-007](adr/ADR-007-enlace-unico-supervisores.md) | Enlaces de un solo uso con vencimiento para los supervisores de empresa | Aceptado | CU-07, EAC-03, RN-04, PA-02 |
| [ADR-008](adr/ADR-008-autorizacion-por-roles.md) | Permisos por rol y ámbito, manejados dentro del sistema | Aceptado | PA-02, RN-01 |
| [ADR-009](adr/ADR-009-reglas-configurables-por-programa.md) | Reglas de práctica configurables y versionadas por programa | Aceptado | CU-12, EAC-01 |
| [ADR-010](adr/ADR-010-acta-desde-plantilla.md) | Generar el acta desde una plantilla HTML separada del código | Aceptado | CU-09, RN-03, RN-05 |
| [ADR-011](adr/ADR-011-aprobacion-trazable-acta-inmutable.md) | Aprobación trazable del acta y acta que no se puede modificar | Aceptado | CU-10, RN-02, RN-05 |
| [ADR-012](adr/ADR-012-bitacora-auditoria.md) | Bitácora de auditoría de solo inserción en la base de datos | Aceptado | PA-03, EAC-03, RN-01 |
| [ADR-013](adr/ADR-013-migracion-desde-excel.md) | Migración con una plantilla Excel estándar y un importador que valida | Aceptado | PA-05 |

### Cobertura de los drivers

Revisamos que los 22 drivers de [drivers.md](drivers.md) tuvieran al menos un ADR. No quedó ninguno pendiente, entonces no hay drivers declarados como riesgo (los riesgos de cada decisión están dentro de su ADR).

| Driver | ADR |
|---|---|
| [CU-01](drivers.md#1-casos-de-uso-y-casos-de-uso-primarios) Postularse a la práctica | ADR-004 |
| [CU-07](drivers.md#1-casos-de-uso-y-casos-de-uso-primarios) Evaluar al practicante | ADR-007 |
| [CU-09](drivers.md#1-casos-de-uso-y-casos-de-uso-primarios) Generar el acta | ADR-010 |
| [CU-10](drivers.md#1-casos-de-uso-y-casos-de-uso-primarios) Aprobar el acta | ADR-011 |
| [CU-12](drivers.md#1-casos-de-uso-y-casos-de-uso-primarios) Configurar reglas | ADR-009 |
| [EAC-01](drivers.md#eac-01-mantenibilidad-modificabilidad) Mantenibilidad | ADR-001, ADR-009 |
| [EAC-02](drivers.md#eac-02-fiabilidad-tolerancia-a-fallos) Fiabilidad | ADR-004, ADR-005 |
| [EAC-03](drivers.md#eac-03-seguridad-confidencialidad-y-responsabilidad) Seguridad | ADR-007, ADR-012 |
| [RT-01](drivers.md#3-restricciones) Infraestructura de la Universidad | ADR-002 |
| [RT-02](drivers.md#3-restricciones) Cuenta institucional | ADR-006 |
| [RT-03](drivers.md#3-restricciones) Solo servicios del SIA | ADR-004 |
| [RT-04](drivers.md#3-restricciones) Catálogo institucional | ADR-003 |
| [RN-01](drivers.md#3-restricciones) Ley 1581 | ADR-002, ADR-008, ADR-012 |
| [RN-02](drivers.md#3-restricciones) Retención documental | ADR-011 |
| [RN-03](drivers.md#3-restricciones) Formato del acta | ADR-010 |
| [RN-04](drivers.md#3-restricciones) Supervisores sin cuenta | ADR-007 |
| [RN-05](drivers.md#3-restricciones) Sin licencias pagas | ADR-003, ADR-010, ADR-011 |
| [PA-01](drivers.md#4-preocupaciones-arquitectónicas) Estructura general | ADR-001 |
| [PA-02](drivers.md#4-preocupaciones-arquitectónicas) Autenticación y autorización | ADR-006, ADR-007, ADR-008 |
| [PA-03](drivers.md#4-preocupaciones-arquitectónicas) Registro y trazabilidad | ADR-012 |
| [PA-04](drivers.md#4-preocupaciones-arquitectónicas) Manejo de errores | ADR-005 |
| [PA-05](drivers.md#4-preocupaciones-arquitectónicas) Migración inicial | ADR-013 |

## 8. Requisitos de calidad

El detalle de cada escenario (las seis partes) está en [drivers.md, sección 2](drivers.md#2-escenarios-de-atributos-de-calidad) y la prioridad sale de la [matriz de priorización](drivers.md#5-matriz-de-priorización).

| EAC | Atributo | Prioridad | ADR | Se verifica en |
|---|---|---|---|---|
| EAC-01 | Mantenibilidad | Alta (atender primero) | ADR-001, ADR-009 | Revisión del cambio al agregar un programa (horas gastadas y módulos tocados). La parte de "0 prácticas cambian de reglas" se verifica en specs/012 cuando se especifique CU-12; mientras tanto [specs/001](../specs/001-postularse/spec.md), escenario 10, revisa que la postulación conserve su versión |
| EAC-02 | Fiabilidad | Alta (atender primero) | ADR-004, ADR-005 | [specs/001](../specs/001-postularse/spec.md), escenarios 5, 6, 7 y 8 |
| EAC-03 | Seguridad | Alta (hacer ya) | ADR-007, ADR-012 | Todavía en ninguna spec: le toca a specs/007 (CU-07) |

La columna "Se verifica en" es el puente con SDD. Hoy EAC-03 no tiene escenario en ninguna spec, o sea que nadie lo está verificando todavía; por eso CU-07 va justo después de CU-01.

## 9. Riesgos y deuda técnica

Riesgo es lo que puede salir mal; deuda técnica es lo que ya sabemos que quedó mal o incompleto, con su respuesta.

| ID | Riesgo o deuda | Origen | Impacto | Respuesta |
|---|---|---|---|---|
| R-01 | Los supervisores no responden a tiempo | [vision.md](vision.md#6-supuestos-y-riesgos-iniciales) | No hay acta (OB-01, OB-02) | Enlace sin cuenta, formulario corto y recordatorios con copia al docente asesor (ADR-007) |
| R-02 | El SIA no tiene servicios de consulta o falla seguido | [vision.md](vision.md#6-supuestos-y-riesgos-iniciales) | No se verifican los requisitos a tiempo | Adaptador aislado y verificación diferida; plan B con exportación periódica detrás del mismo puerto (ADR-004) |
| R-03 | Se exige firma digital certificada del acta | [vision.md](vision.md#6-supuestos-y-riesgos-iniciales) | Rediseño del cierre del acta | Validar S-06 con el área jurídica antes de construir CU-10 |
| R-04 | Sobredimensionar la solución | [vision.md](vision.md#6-supuestos-y-riesgos-iniciales) | Costo y operación innecesarios | Cada ADR se justifica con S-03; sin bróker ni microservicios (ADR-001, ADR-005) |
| R-05 | El SIA queda caído varios días al inicio del periodo y se acumulan pendientes | ADR-004 (riesgo asumido) | Estudiantes sin respuesta varios días | Alerta al administrador cuando haya postulaciones pendientes con más de 2 h |
| R-06 | Un trabajo pendiente falla siempre por datos malos | ADR-005 (riesgo asumido) | Reintentos sin fin | A las 24 h pasa a "fallido" y se avisa al administrador |
| R-07 | Los módulos se acoplan con el tiempo | ADR-001 (riesgo asumido) | Se pierde EAC-01 | Revisión de la regla de dependencia en cada `validacion.md` |
| R-08 | Las reglas que apruebe el Consejo no caben en los parámetros | ADR-009 (riesgo asumido) | Toca programar validadores nuevos | Revisar el reglamento de todos los programas antes de cerrar el modelo |
| R-09 | Un administrador de base de datos modifica la bitácora | ADR-012 (riesgo residual) | Evidencia de auditoría alterada | Se acepta; los respaldos permiten detectar diferencias |
| DT-01 | En esta etapa todo corre con adaptadores en memoria: no hay base de datos ni la transacción única de ADR-005 (postulación, trabajo y bitácora juntos) | [AGENTS.md](../AGENTS.md), [plan de specs/001](../specs/001-postularse/plan.md) | Si el proceso se reinicia se pierde todo (solo afecta desarrollo) | Se acepta para la etapa del taller; el adaptador de base de datos es una tarea antes de salir a producción |
| DT-02 | Si el trabajo "verificar en SIA" queda "fallido", la postulación sigue "pendiente de verificación" y depende de que el administrador la revise a mano; no hay caso de uso para reprocesarla | ESC-01, [specs/001](../specs/001-postularse/spec.md) escenario 8 | Estudiante esperando sin respuesta | Se acepta; si pasa seguido, se agrega un caso de uso de reprocesar con su ADR |
| DT-03 | Usamos Python 3.12 suponiendo que está en el catálogo institucional (RT-04), pero eso no está confirmado (S-09) | [AGENTS.md](../AGENTS.md) | Si no está, toca cambiar de lenguaje | Confirmar con el Área de Sistemas; si no está, ADR nuevo que lo reemplace |
| DT-04 | Los controladores web y el login real no se construyen en esta etapa: la sesión llega ya armada al caso de uso | [plan de specs/001](../specs/001-postularse/plan.md) | No hay interfaz para el estudiante | Specs y tareas propias de la capa web después de las specs de los casos primarios |

## 10. Glosario

Una sola palabra para cada concepto, en la documentación, en las specs y en el código. Si en el código aparecen Solicitud, Inscripcion y Postulacion para lo mismo, el glosario no se respetó. En el código los nombres van sin tildes ni eñes.

| Término | Definición | Nombre en el código |
|---|---|---|
| Programa | Programa académico de la Facultad; cada uno tiene sus reglas | `programa` (texto) |
| Versión de reglas | Las reglas de práctica de un programa desde una fecha de vigencia; no se modifica, un cambio es una versión nueva | `VersionReglas` |
| Requisito | Una condición académica de una versión de reglas (tipo y valor exigido) | `Requisito` |
| Validador de requisito | La pieza del Módulo Reglas que revisa un tipo de requisito contra los datos académicos | `ValidadorRequisito` |
| Datos académicos | Lo que el SIA devuelve de un estudiante: promedio y créditos aprobados | `DatosAcademicos` |
| Consulta académica | Puerto para consultar los datos académicos en el SIA (RT-03) | `ConsultaAcademica` |
| Estudiante | Quien se postula y hace la práctica; solo ve lo suyo | `Estudiante` (en la sesión, rol `estudiante`) |
| Postulación | La solicitud del estudiante ante la Facultad para hacer la práctica, con la plaza ya conseguida | `Postulacion` |
| Estado de la postulación | Pendiente de verificación, verificada o no cumple requisitos (CU-02 agregará aprobada y rechazada) | `EstadoPostulacion` |
| Postulación activa | Una postulación pendiente de verificación o verificada; un estudiante solo puede tener una | `esta_activa()` |
| Práctica | La práctica aprobada, desde la postulación hasta el cierre | `Practica` |
| Empresa | Donde se hace la práctica; solo se consulta si el convenio está vigente | `Empresa` |
| Supervisor de empresa | La persona de la empresa que valida horas y evalúa; no tiene cuenta institucional | `SupervisorEmpresa` |
| Docente asesor | Docente que asesora la práctica; solo ve las que asesora | `DocenteAsesor` |
| Director de programa | Director del programa; configura reglas y aprueba; solo ve su programa | `DirectorPrograma` |
| Administrador del sistema | Asigna roles, hace la migración y recibe los avisos de trabajos fallidos | `AdministradorSistema` |
| Registro de horas | Las horas de una semana de práctica | `RegistroHoras` |
| Enlace de supervisor | Acceso de un solo uso para validar horas o evaluar; vence a los 15 días | `EnlaceSupervisor` |
| Evaluación | La evaluación que la empresa hace del practicante | `Evaluacion` |
| Acta | El acta final de la práctica, con la huella de su PDF | `Acta` |
| Plantilla del acta | El formato oficial del acta, separado del código | `PlantillaActa` |
| Aprobación del acta | Una aprobación electrónica del acta; máximo dos | `AprobacionActa` |
| Evento de bitácora | Un registro de auditoría: quién, qué, sobre qué, cuándo y desde dónde | `EventoBitacora` |
| Registro de bitácora | Puerto donde se guardan los eventos de bitácora | `RegistroBitacora` |
| Sesión | Quién es el usuario, qué rol tiene y cuál es su ámbito (programa) | `Sesion` |
| Trabajo pendiente | Una llamada externa que puede fallar (verificar en SIA, enviar correo), guardada para hacerla y reintentarla en segundo plano | `TrabajoPendiente` |
| Cola de pendientes | Puerto donde se guardan los trabajos pendientes | `ColaPendientes` |
| Procesador de pendientes | El proceso que cada minuto toma los trabajos vencidos y los ejecuta | `ProcesadorPendientes` |
| Manejador de trabajo | La interfaz que implementa cada módulo para ejecutar un tipo de trabajo | `ManejadorTrabajo` |
| Notificador | Puerto para enviar correos | `Notificador` |

