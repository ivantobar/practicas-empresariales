# ADR-003: Base de datos relacional de código abierto del catálogo institucional

## Estado

Aceptado (2026-11-02)

## Contexto

[RT-04](../drivers.md#3-restricciones) dice que hay que usar el motor de base de datos del catálogo institucional y [RN-05](../drivers.md#3-restricciones) prohíbe licencias de pago recurrente. El motor exacto lo define el catálogo; aquí decidimos el tipo de base de datos y cómo escoger dentro del catálogo.

Los datos son muy relacionales (estudiante, práctica, docente, horas, evaluación y acta se referencian entre sí) y hay operaciones que tienen que ser atómicas, como aprobar un acta y guardar su evidencia. [OB-04](../vision.md#2-objetivos-de-negocio) pide integridad de los datos y [RN-02](../drivers.md#3-restricciones) pide conservar actas y evidencias.

## Alternativas consideradas

1. **Relacional de código abierto del catálogo** (PostgreSQL o MySQL/MariaDB, la que esté en el catálogo). Tiene transacciones, llaves foráneas y restricciones que protegen la integridad, no cuesta licencia y el Área de Sistemas ya la soporta. Los cambios de modelo hay que hacerlos con migraciones, y no sirve para guardar los PDF adentro.
2. **Relacional comercial** (Oracle o SQL Server, si estuvieran en el catálogo). Mismas ventajas, pero la licencia es de pago recurrente y RN-05 lo prohíbe.
3. **Documental (MongoDB).** El esquema es flexible, pero nuestros datos son relacionales y necesitan transacciones entre entidades. La integridad quedaría en el código. Y si no está en el catálogo, RT-04 la descarta.

## Decisión

Elegimos la opción 1. Solo se accede a la base desde los adaptadores de persistencia ([ADR-001](ADR-001-monolito-modular.md)). Los PDF de las actas van en el almacenamiento de archivos del servidor y en la base se guarda la ruta y la huella ([ADR-011](ADR-011-aprobacion-trazable-acta-inmutable.md)). El esquema se versiona con migraciones en el repositorio.

## Consecuencias

**Positivas:** el motor protege la integridad, lo que ayuda a OB-04; no se paga licencia y el Área de Sistemas la soporta; la misma base sirve para la bitácora ([ADR-012](ADR-012-bitacora-auditoria.md)) y para la cola de pendientes ([ADR-005](ADR-005-reintentos-y-estados-pendientes.md)), sin agregar otra tecnología.

**Negativas:** cada cambio de modelo necesita una migración probada. Quedamos atados a las versiones que maneje el Área de Sistemas. Y al tener datos, bitácora y cola en la misma base, si la base falla se cae todo; eso se cubre con los respaldos del Área de Sistemas.

**Riesgos:** que el catálogo no tenga ningún motor relacional libre. Se confirma la primera semana (S-09) y, si pasa, se escala a la Decanatura el choque entre RT-04 y RN-05.

**Vistas que modifica:** [Procesos](../vistas/02-procesos.md), [Desarrollo](../vistas/03-desarrollo.md), [Física](../vistas/04-fisica.md).
