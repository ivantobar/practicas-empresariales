# Documento de arquitectura: Sistema de Gestión de Prácticas Empresariales

Este documento consolida la arquitectura y enlaza a los demás archivos de `docs/` en lugar de copiar su contenido.

## 1. Introducción y objetivos

Los objetivos de negocio están en [vision.md, sección 2](vision.md#2-objetivos-de-negocio) (OB-01 a OB-06).

## 2. Restricciones

Las restricciones técnicas (RT-01 a RT-04) y de negocio (RN-01 a RN-05), con su tipo, origen e impacto arquitectónico, están en [drivers.md, sección 3](drivers.md#3-restricciones).

## 3. Contexto del sistema

El contexto (C4, nivel 1) está en [contexto.md](contexto.md), con su diagrama [diagramas/contexto.puml](diagramas/contexto.puml). Ahí el sistema es una caja negra con sus 5 tipos de usuario y 3 sistemas externos (SIA, proveedor de identidad y correo).

## 4. Estrategia de solución

*Pendiente.*

## 5. Vistas

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

*Pendiente.*

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

Los escenarios de atributos de calidad (EAC-01 a EAC-03) están en [drivers.md, sección 2](drivers.md#2-escenarios-de-atributos-de-calidad).

## 9. Riesgos y deuda técnica

*Pendiente.*
