# ADR-007: Enlaces de un solo uso con vencimiento para los supervisores de empresa

## Estado

Aceptado (2026-11-02)

## Contexto

El supervisor de empresa evalúa al practicante ([CU-07](../drivers.md#1-casos-de-uso-y-casos-de-uso-primarios)) y valida las horas ([CU-05](../drivers.md#1-casos-de-uso-y-casos-de-uso-primarios)), pero es externo y no tiene cuenta institucional.

- [RN-04](../drivers.md#3-restricciones): no se le puede pedir cuenta ni registro con contraseña.
- [EAC-03](../drivers.md#eac-03-seguridad-confidencialidad-y-responsabilidad): un enlace ya usado, con más de 15 días o alterado se rechaza el 100% de las veces, sin mostrar datos personales, y queda en la bitácora en menos de 1 minuto.
- [R-01](../vision.md#6-supuestos-y-riesgos-iniciales) y [OB-02](../vision.md#2-objetivos-de-negocio): si el trámite es complicado el supervisor no responde, y sin evaluación no hay acta.
- Este acceso tiene que convivir con el login institucional ([ADR-006](ADR-006-autenticacion-institucional.md), [PA-02](../drivers.md#4-preocupaciones-arquitectónicas)).

## Alternativas consideradas

1. **Un enlace fijo por práctica que no vence.** Es lo más cómodo, pero cualquiera que consiga el enlace (por ejemplo, un correo reenviado) puede entrar siempre. No cumple EAC-03.
2. **Enlace de un solo uso que vence a los 15 días.** Por cada solicitud (una evaluación o una semana de horas) se genera un código aleatorio largo, imposible de adivinar, y se manda al correo del supervisor. En la base no se guarda el código tal cual, sino una versión cifrada, junto con la fecha de vencimiento. Cuando se usa, se invalida. Cumple RN-04 y EAC-03 y el supervisor entra con un clic. El problema es que quien tenga acceso al correo del supervisor puede usarlo antes que él, y si lo pierde tiene que pedir otro.
3. **Enlace más un código que llega al mismo correo al abrirlo.** Es un poco más difícil de usar si el enlace se filtra, pero son dos pasos y dos correos por cada validación semanal, y como el código llega al mismo correo casi no protege más que la opción 2. Además mete fricción justo donde R-01 pide quitarla.

## Decisión

Elegimos la opción 2 porque cumple EAC-03 y RN-04 con lo mínimo de esfuerzo para el supervisor, que es lo que cuida OB-02. El código nunca se guarda tal cual en la base. Si el enlace no sirve, se muestra un mensaje genérico ("este enlace no es válido o ya venció; pídale uno nuevo al docente asesor") sin datos del practicante, y el intento queda en la bitácora con fecha, hora e IP ([ADR-012](ADR-012-bitacora-auditoria.md)). El supervisor es un rol más del control de acceso ([ADR-008](ADR-008-autorizacion-por-roles.md)), limitado a la práctica del enlace.

## Consecuencias

**Positivas:** el supervisor no crea cuentas ni recuerda contraseñas; un enlace robado sirve máximo una vez y por 15 días, y uno alterado nunca sirve; si se filtra la base de datos, los enlaces vigentes no se pueden reconstruir porque no están guardados tal cual.

**Negativas:** la seguridad depende del correo del supervisor: quien entre a su buzón puede evaluar por él. Lo aceptamos porque RN-04 no deja poner un segundo factor propio, y de todas formas el docente asesor revisa la evaluación antes del acta. También, cada validación semanal manda un correo, lo que puede cansar a supervisores con varios practicantes. Y hay que hacer el flujo para pedir un enlace nuevo.

**Riesgos:** que los correos lleguen a spam. Se mandan desde el dominio institucional y con copia al docente asesor, como dice R-01.

**Vistas que modifica:** [Contexto](../contexto.md), [Lógica](../vistas/01-logica.md), [Desarrollo](../vistas/03-desarrollo.md). Se ve en ESC-02 ([cu07-evaluar-practicante](../diagramas/secuencias/cu07-evaluar-practicante.puml)).
