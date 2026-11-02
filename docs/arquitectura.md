# Documento de arquitectura: Sistema de Gestión de Prácticas Empresariales

Este documento consolida la arquitectura y enlaza a los demás archivos de `docs/` en lugar de copiar su contenido.

## 1. Introducción y objetivos

Los objetivos de negocio están en [vision.md, sección 2](vision.md#2-objetivos-de-negocio) (OB-01 a OB-06).

## 2. Restricciones

Las restricciones técnicas (RT-01 a RT-04) y de negocio (RN-01 a RN-05), con su tipo, origen e impacto arquitectónico, están en [drivers.md, sección 3](drivers.md#3-restricciones).

## 3. Contexto del sistema

*Pendiente.* Se completa en el tema de vistas.

## 4. Estrategia de solución

*Pendiente.*

## 5. Vistas

*Pendiente.* Se completa en el tema de vistas.

## 6. Conceptos transversales

*Pendiente.*

## 7. Decisiones de diseño

Las decisiones están en la carpeta [`adr/`](adr/), un archivo por decisión. Si alguna cambia no se edita el ADR, se hace uno nuevo que lo reemplace.

| ADR | Decisión | Estado | Drivers |
|---|---|---|---|
| [ADR-001](adr/ADR-001-monolito-modular.md) | Monolito modular con puertos y adaptadores | Aceptado | PA-01, EAC-01 |
| [ADR-002](adr/ADR-002-despliegue-institucional.md) | Despliegue con contenedores en los servidores de la Universidad | Aceptado | RT-01, RN-01 |
| [ADR-003](adr/ADR-003-persistencia-relacional.md) | Base de datos relacional de código abierto del catálogo institucional | Aceptado | RT-04, RN-05 |
| [ADR-004](adr/ADR-004-integracion-sia.md) | Integración con el SIA por un adaptador y verificación diferida | Aceptado | CU-01, EAC-02, RT-03 |
| [ADR-005](adr/ADR-005-reintentos-y-estados-pendientes.md) | Cola de trabajos pendientes en la base de datos para las fallas de integración | Aceptado | PA-04, EAC-02 |
| [ADR-006](adr/ADR-006-autenticacion-institucional.md) | Login con el proveedor de identidad institucional (OpenID Connect o SAML) | Aceptado | RT-02, PA-02 |
| [ADR-007](adr/ADR-007-enlace-unico-supervisores.md) | Enlaces de un solo uso con vencimiento para los supervisores de empresa | Aceptado | CU-07, EAC-03, RN-04, PA-02 |
| [ADR-008](adr/ADR-008-autorizacion-por-roles.md) | Permisos por rol y ámbito, manejados dentro del sistema | Aceptado | PA-02, RN-01 |
| [ADR-009](adr/ADR-009-reglas-configurables-por-programa.md) | Reglas de práctica configurables y versionadas por programa | Aceptado | CU-12, EAC-01 |
| [ADR-010](adr/ADR-010-acta-desde-plantilla.md) | Generar el acta desde una plantilla HTML separada del código | Aceptado | CU-09, RN-03, RN-05 |
| [ADR-011](adr/ADR-011-aprobacion-trazable-acta-inmutable.md) | Aprobación trazable del acta con hash del documento, y acta inmutable | Aceptado | CU-10, RN-02, RN-05 |
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
