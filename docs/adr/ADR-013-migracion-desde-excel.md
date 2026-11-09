# ADR-013: Migración con una plantilla Excel estándar y un importador que valida

## Estado

Aceptado (2026-11-02)

## Contexto

Hay que pasar al sistema las prácticas que están en curso, que hoy cada docente asesor lleva en su propio Excel ([PA-05](../drivers.md#4-preocupaciones-arquitectónicas), [CU-15](../drivers.md#1-casos-de-uso-y-casos-de-uso-primarios), [alcance](../vision.md#3-alcance)). Son entre 170 y 250 prácticas ([S-03](../vision.md#6-supuestos-y-riesgos-iniciales)) y esto define el primer despliegue.

En la matriz, PA-05 quedó en "cuestionar" (poca importancia y mucha dificultad), así que la idea es resolverlo con el menor esfuerzo posible. Pero hay que cuidar [OB-04](../vision.md#2-objetivos-de-negocio): estos datos van a terminar en actas, así que un error en la migración es un error en un acta. Los datos académicos no se migran del Excel, se sacan del SIA ([RT-03](../drivers.md#3-restricciones), [ADR-004](ADR-004-integracion-sia.md)).

## Alternativas consideradas

1. **Digitar a mano cada práctica en el sistema nuevo.** No hay que construir nada, pero digitar 170 a 250 prácticas con sus horas es repetir justo el error de transcripción que queremos eliminar.
2. **Un programa que lea cada Excel en su formato original.** Los docentes no tendrían que hacer nada, pero pueden ser hasta 50 formatos distintos, y es muchísimo trabajo para algo que se usa una vez.
3. **Una plantilla Excel estándar que cada docente llena, más un importador que valida y muestra los errores antes de cargar.** Solo hay que leer un formato, los errores salen antes de entrar al sistema, y el que corrige es el docente, que conoce sus datos. A cambio, cada docente tiene que hacer ese trabajo una vez.

## Decisión

Elegimos la opción 3. La plantilla solo pide lo que no está en el SIA: el estudiante (por documento), la empresa, el supervisor y su correo, el docente asesor y las horas acumuladas a la fecha de corte. El importador revisa cada fila (que el estudiante exista en el SIA, que no haya duplicados, que las horas tengan sentido), saca un reporte de errores y solo carga los archivos que no tengan errores. Las prácticas migradas quedan con la versión de reglas vigente de su programa ([ADR-009](ADR-009-reglas-configurables-por-programa.md)) y marcadas como "migrada" en la bitácora ([ADR-012](ADR-012-bitacora-auditoria.md)). Protege OB-04 con mucho menos esfuerzo que la opción 2, que es lo que pide el cuadrante "cuestionar".

## Consecuencias

**Positivas:** los datos entran validados; es un importador sencillo que se usa una vez y se retira; se puede probar la carga en el ambiente de pruebas las veces que haga falta.

**Negativas:** cada docente tiene que gastar tiempo pasando sus datos a la plantilla justo en el lanzamiento, lo que va en contra de OB-03 durante unas semanas. No se migra la historia anterior a la fecha de corte (las horas semana a semana, los correos), solo el acumulado; eso es coherente con el alcance, que deja por fuera el histórico. Y es código de un solo uso que igual hay que hacer y probar.

**Riesgos:** que algunos docentes no entreguen la plantilla a tiempo. El director pone una fecha de corte, y lo que llegue tarde se carga en una segunda tanda con el mismo importador.

**Vistas que modifica:** [Contexto](../contexto.md), [Desarrollo](../vistas/03-desarrollo.md).
