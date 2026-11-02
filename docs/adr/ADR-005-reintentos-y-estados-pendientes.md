# ADR-005: Cola de trabajos pendientes en la base de datos para las fallas de integración

## Estado

Aceptado (2026-11-02)

## Contexto

Necesitamos una sola forma de manejar las fallas del SIA y del correo: reintentos, estados pendientes y mensajes al usuario ([PA-04](../drivers.md#4-preocupaciones-arquitectónicas)). Si no, cada caso de uso va a manejar la caída del SIA a su manera ([R-02](../vision.md#6-supuestos-y-riesgos-iniciales)).

[EAC-02](../drivers.md#eac-02-fiabilidad-tolerancia-a-fallos) pide 0 postulaciones perdidas y verificar máximo 30 minutos después de que el SIA vuelva. Además los enlaces a supervisores ([ADR-007](ADR-007-enlace-unico-supervisores.md)), los recordatorios y los avisos de [EAC-03](../drivers.md#eac-03-seguridad-confidencialidad-y-responsabilidad) dependen del correo, que también puede fallar. Y la carga es baja ([S-03](../vision.md#6-supuestos-y-riesgos-iniciales)), así que no queremos meter infraestructura de más ([R-04](../vision.md#6-supuestos-y-riesgos-iniciales)).

## Alternativas consideradas

1. **Reintentar en memoria dentro de la misma petición.** No hay que agregar nada, pero si el servidor se reinicia los reintentos se pierden y cada caso de uso tendría su propia lógica. No cumple EAC-02.
2. **Un bróker de mensajes como RabbitMQ.** Está hecho para esto y trae reintentos, pero es otro servidor que instalar, monitorear y respaldar, y puede que no esté en el catálogo ([RT-04](../drivers.md#3-restricciones)). Para unas decenas de trabajos por hora es demasiado.
3. **Una tabla de trabajos pendientes en la base de datos, procesada por una tarea programada.** El trabajo se guarda en la misma transacción que el dato (la postulación y su verificación pendiente quedan juntas o ninguna), no agrega tecnología ([ADR-003](ADR-003-persistencia-relacional.md)) y sobrevive a reinicios. Toca programar el procesador y los reintentos.

## Decisión

Elegimos la opción 3. Toda llamada externa que pueda fallar (verificar en el SIA, mandar correos) se guarda como trabajo pendiente en la misma transacción del caso de uso. Una tarea programada revisa la tabla cada minuto y reintenta con esperas crecientes (1, 2, 5 y 10 minutos, y después cada 10 minutos). Así, cuando el SIA vuelve, los pendientes se verifican en el siguiente ciclo, dentro de los 30 minutos de EAC-02. Los mensajes al usuario para estados pendientes se definen una sola vez y los usan todos los casos de uso.

## Consecuencias

**Positivas:** una sola estrategia de fallas para todo el sistema; no se pierden trabajos por reinicios ni caídas; la mesa de ayuda puede ver por qué un trámite sigue pendiente.

**Negativas:** es código propio que mantener (el procesador, los reintentos y el bloqueo para que dos procesos no tomen el mismo trabajo), cosas que un bróker ya trae. Puede haber hasta un minuto de retraso entre que el SIA vuelve y el siguiente intento. La tabla crece y hay que limpiarla cada cierto tiempo.

**Riesgos:** que un trabajo falle siempre (por datos malos) y se quede reintentando para siempre. Después de 24 horas pasa a "fallido" y se avisa al administrador. Si el volumen creciera mucho más que S-03, se cambiaría por un bróker con un ADR nuevo.
