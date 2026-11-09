# Vista lógica: modelo de dominio

Diagrama: [../diagramas/01-logica.puml](../diagramas/01-logica.puml) (UML, clases de análisis)

Para: usuarios finales, analistas y el director de programa. Responde qué conceptos maneja el sistema y cómo se relacionan.

## 1. Presentación principal

Es un modelo de dominio, no un diagrama de clases del código. Por eso no tiene tipos, ni visibilidad, ni métodos, ni cosas técnicas como repositorios o la cola de pendientes. Las multiplicidades guardan reglas del negocio.

## 2. Catálogo de elementos

| Entidad | Qué representa | Atributos clave | Regla del negocio |
|---|---|---|---|
| Programa | Programa académico de la Facultad | nombre | Cada uno tiene sus propias reglas (S-07) |
| VersionReglas | Las reglas de práctica de un programa en un periodo | número, fecha de vigencia, horas mínimas, plazos | No se modifica: un cambio es una versión nueva (ADR-009) |
| Requisito | Una condición académica de una versión de reglas | tipo, valor exigido | Cada tipo tiene un validador en el Módulo Reglas |
| Estudiante | Quien hace la práctica | documento, nombre | Solo ve sus propias postulaciones y prácticas (RN-01) |
| Postulacion | La solicitud del estudiante ante la Facultad | fecha, estado | Queda amarrada a la VersionReglas vigente al postularse; puede quedar "pendiente de verificación" si el SIA falla (ADR-004) |
| Practica | La práctica aprobada, de la postulación al cierre | fecha de inicio, estado, horas acumuladas | Una postulación da origen a máximo una práctica |
| Empresa | Donde se hace la práctica | nombre, convenio vigente | Solo se consulta si el convenio está vigente (alcance) |
| SupervisorEmpresa | La persona de la empresa que supervisa | nombre, correo | No tiene cuenta institucional (RN-04) |
| DocenteAsesor | Docente que asesora la práctica | nombre, carga actual | Ve solo las prácticas que asesora (ADR-008) |
| DirectorPrograma | Director del programa | nombre | Ve solo las prácticas de su programa (ADR-008) |
| RegistroHoras | Las horas de una semana | semana, horas, estado | Las registra el estudiante y las valida el supervisor (S-05) |
| EnlaceSupervisor | Acceso de un solo uso para validar horas o evaluar | propósito, fecha de vencimiento, estado | Vence a los 15 días y sirve una vez (ADR-007, EAC-03) |
| Evaluacion | La evaluación que la empresa hace del practicante | fecha, nota, observaciones | Máximo una por práctica; su nota va al acta (S-01) |
| Acta | El acta final de la práctica | número, estado, huella del PDF | Cerrada no se modifica; un error se corrige con un acta que la reemplaza (ADR-011, RN-02) |
| PlantillaActa | El formato oficial del acta | versión, vigente desde | Separada del código; cada acta guarda con qué versión se hizo (ADR-010, RN-03) |
| AprobacionActa | Una aprobación electrónica del acta | fecha y hora, origen, huella aprobada | Máximo 2: docente asesor y director (S-06) |
| EventoBitacora | Un evento de auditoría | quién, qué, sobre qué, cuándo, desde dónde | Solo se inserta, no copia datos personales (ADR-012) |

## 3. Justificación

- CU-01, CU-07, CU-09, CU-10 y CU-12: de ellos salen Postulacion, Evaluacion, Acta, AprobacionActa y VersionReglas.
- EAC-01 y [ADR-009](../adr/ADR-009-reglas-configurables-por-programa.md): las reglas son datos versionados (VersionReglas y Requisito). Un programa nuevo con otros valores no toca código, y como cada Postulacion apunta a su versión, 0 prácticas en curso cambian de reglas.
- EAC-02 y [ADR-004](../adr/ADR-004-integracion-sia.md): el estado "pendiente de verificación" de Postulacion es lo que permite no perder ninguna postulación cuando el SIA no responde.
- EAC-03 y [ADR-007](../adr/ADR-007-enlace-unico-supervisores.md): EnlaceSupervisor tiene estado y vencimiento.
- RN-02, RN-03, OB-04 y [ADR-010](../adr/ADR-010-acta-desde-plantilla.md), [ADR-011](../adr/ADR-011-aprobacion-trazable-acta-inmutable.md): Acta con huella, PlantillaActa con versión y la relación "reemplaza".
- OB-06, PA-03 y [ADR-012](../adr/ADR-012-bitacora-auditoria.md): EventoBitacora.
- RN-01 y [ADR-008](../adr/ADR-008-autorizacion-por-roles.md): las relaciones Practica con DocenteAsesor y Programa con DirectorPrograma son las que definen el ámbito de cada rol.

## 4. Comportamiento

- [cu01-postularse](../diagramas/secuencias/cu01-postularse.puml): Postulacion pasa de "pendiente de verificación" a "verificada" o "no cumple requisitos".
- [cu07-evaluar-practicante](../diagramas/secuencias/cu07-evaluar-practicante.puml): EnlaceSupervisor pasa a "usado" y se crea la Evaluacion.
- [cu09-generar-acta](../diagramas/secuencias/cu09-generar-acta.puml) y [cu10-aprobar-acta](../diagramas/secuencias/cu10-aprobar-acta.puml): Acta pasa por generada, aprobada por el docente y cerrada.
- [cu12-configurar-reglas](../diagramas/secuencias/cu12-configurar-reglas.puml): se crea una VersionReglas nueva sin tocar la anterior.

## 5. Vistas relacionadas

- [Desarrollo](03-desarrollo.md): estas entidades viven en la capa `dominio/` y los módulos las usan.
- [Procesos](02-procesos.md): se guardan en la Base de datos de prácticas; el PDF del Acta y la PlantillaActa en el Almacenamiento de documentos.
