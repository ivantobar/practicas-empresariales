# ADR-012: Bitácora de auditoría de solo inserción en la base de datos

## Estado

Aceptado (2026-11-02)

## Contexto

Hay que decidir qué se registra, dónde y por cuánto tiempo ([PA-03](../drivers.md#4-preocupaciones-arquitectónicas)).

- [EAC-03](../drivers.md#eac-03-seguridad-confidencialidad-y-responsabilidad): cada intento con un enlace inválido queda registrado con fecha, hora e IP en menos de 1 minuto.
- [OB-06](../vision.md#2-objetivos-de-negocio): responder una auditoría o acreditación en máximo 1 día hábil.
- [RN-01](../drivers.md#3-restricciones): hay que registrar la autorización de tratamiento de datos y quién accede a ellos.
- [RN-02](../drivers.md#3-restricciones): conservar según la tabla de retención.
- La mesa de ayuda necesita ver por qué alguien no puede postularse o registrar horas ([stakeholders](../vision.md#4-stakeholders)).

## Alternativas consideradas

1. **Los archivos de log del servidor.** Ya existen y no hay que hacer nada, pero son texto libre difícil de consultar en una auditoría, se rotan y se borran, y cualquiera con acceso al servidor los puede editar. No sirven como evidencia.
2. **Una tabla de bitácora de solo inserción en la base de datos, escrita en la misma transacción del evento, y los logs técnicos aparte.** Los eventos se consultan con SQL; si la operación se guarda, su registro también (y si falla, ninguno); el usuario de la aplicación no puede modificar ni borrar filas. No agrega infraestructura ([ADR-003](ADR-003-persistencia-relacional.md)). Cada operación hace una escritura más y la tabla crece todo el tiempo.
3. **Una plataforma de logs como Elasticsearch, Logstash y Kibana.** Tiene búsquedas y tableros muy buenos, pero son varios servidores que operar, demasiado para la carga de [S-03](../vision.md#6-supuestos-y-riesgos-iniciales) ([R-04](../vision.md#6-supuestos-y-riesgos-iniciales)), y es fácil que termine guardando datos personales sin control.

## Decisión

Elegimos la opción 2. En la bitácora se registran: inicios de sesión, uso de enlaces válidos e inválidos ([ADR-007](ADR-007-enlace-unico-supervisores.md)), permisos negados ([ADR-008](ADR-008-autorizacion-por-roles.md)), la aceptación de la autorización de tratamiento de datos, cambios de estado de postulaciones y prácticas, validación de horas, evaluaciones, aprobaciones de actas ([ADR-011](ADR-011-aprobacion-trazable-acta-inmutable.md)) y cambios de reglas ([ADR-009](ADR-009-reglas-configurables-por-programa.md)). Cada registro guarda quién, qué, sobre qué, cuándo y desde dónde, pero no copia los datos personales. Cuánto tiempo se guarda es un parámetro que sale de la tabla de retención (RN-02). Los logs técnicos (errores, tiempos) van en archivos y son solo para diagnóstico.

## Consecuencias

**Positivas:** sacar el consolidado de una auditoría es una consulta y no una reconstrucción a mano; el intento con un enlace inválido queda registrado de una vez, dentro del minuto de EAC-03; la mesa de ayuda ve la historia de un trámite sin pedir acceso al servidor.

**Negativas:** cada operación registrada hace una escritura más (unos milisegundos), que aceptamos por la trazabilidad. La tabla crece hasta que la retención deje depurarla, y los respaldos se vuelven más pesados. Además, registrar quién consultó qué también es un dato personal, así que hay que protegerlo con los mismos permisos.

**Riesgos:** que un administrador de base de datos con permisos altos modifique la bitácora. Lo aceptamos como riesgo residual; con los respaldos del Área de Sistemas se pueden detectar diferencias.
