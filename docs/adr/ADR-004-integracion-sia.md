# ADR-004: Integración con el SIA por un adaptador y verificación diferida

## Estado

Aceptado (2026-11-02)

## Contexto

Cuando el estudiante se postula ([CU-01](../drivers.md#1-casos-de-uso-y-casos-de-uso-primarios)) hay que verificar sus requisitos académicos en el SIA ([S-02](../vision.md#6-supuestos-y-riesgos-iniciales)).

- [RT-03](../drivers.md#3-restricciones): solo podemos usar los servicios que expone el SIA, nada de conectarnos a su base de datos.
- [EAC-02](../drivers.md#eac-02-fiabilidad-tolerancia-a-fallos): si el SIA no responde en 5 s o da error, no se puede perder ninguna postulación, el estudiante debe recibir confirmación en menos de 3 s (95%) y la verificación debe completarse máximo 30 minutos después de que el SIA vuelva.
- [R-02](../vision.md#6-supuestos-y-riesgos-iniciales): puede que el SIA falle seguido o que no tenga los servicios que necesitamos.

## Alternativas consideradas

1. **Llamar al SIA de forma sincrónica durante la postulación.** Es lo más simple y el estudiante sabe de una si cumple. Pero si el SIA se demora o falla, el estudiante se queda esperando o pierde la postulación. No cumple EAC-02.
2. **Adaptador del SIA detrás de un puerto, con verificación diferida.** Primero se guarda la postulación como "pendiente de verificación", se le confirma al estudiante, y la verificación se hace en segundo plano reintentando si el SIA falla ([ADR-005](ADR-005-reintentos-y-estados-pendientes.md)). Cumple EAC-02 y el resto del sistema no conoce los detalles del SIA. A cambio, el estudiante no sabe en el momento si cumple y aparecen estados intermedios.
3. **Copia local con una exportación periódica del SIA.** No dependemos del SIA en línea, pero los datos pueden estar viejos (alguien que acaba de pasar una materia saldría sin el requisito) y tendríamos que mantener una réplica parcial del SIA.

## Decisión

Elegimos la opción 2 porque es la única que cumple EAC-02 sin violar RT-03 ni trabajar con datos desactualizados. El adaptador espera máximo 5 s; si el SIA responde, la postulación pasa a "verificada" o "no cumple requisitos", y si falla, queda pendiente y se reintenta.

La opción 3 la dejamos como plan B para R-02: si resulta que el SIA no tiene servicios de consulta, se hace otro adaptador sobre la exportación periódica, detrás del mismo puerto.

## Consecuencias

**Positivas:** no se pierde ninguna postulación por fallas del SIA; la confirmación al estudiante no depende de lo que tarde el SIA; si toca pasar al plan B, solo cambia un adaptador.

**Negativas:** el estudiante primero ve "recibida" y después le llega el resultado, y eso hay que explicarlo bien en la pantalla. El director no puede aprobar una postulación ([CU-02](../drivers.md#1-casos-de-uso-y-casos-de-uso-primarios)) mientras siga pendiente. Hay un componente más que probar, y para eso hace falta un simulador del SIA.

**Riesgos:** que el SIA esté caído varios días al inicio del periodo y se acumulen pendientes. Ponemos una alerta al administrador cuando haya postulaciones pendientes con más de 2 horas.

**Vistas que modifica:** [Contexto](../contexto.md), [Lógica](../vistas/01-logica.md), [Procesos](../vistas/02-procesos.md), [Desarrollo](../vistas/03-desarrollo.md). Se ve en ESC-01 ([cu01-postularse](../diagramas/secuencias/cu01-postularse.puml)).
