# ADR-010: Generar el acta desde una plantilla HTML separada del código

## Estado

Aceptado (2026-11-02)

## Contexto

Generar el acta final ([CU-09](../drivers.md#1-casos-de-uso-y-casos-de-uso-primarios)) es la razón de ser del sistema.

- [RN-03](../drivers.md#3-restricciones): el acta tiene que seguir el formato del reglamento de prácticas, que lo define el Consejo de Facultad y puede cambiar.
- [OB-04](../vision.md#2-objetivos-de-negocio): menos del 1% de actas reemitidas por errores en los datos.
- [OB-01](../vision.md#2-objetivos-de-negocio): máximo 5 días hábiles desde que se cumplen las horas hasta que se entrega el acta.
- [RN-05](../drivers.md#3-restricciones): nada de licencias pagas.
- La nota que pone la empresa en [CU-07](../drivers.md#1-casos-de-uso-y-casos-de-uso-primarios) va en el acta ([S-01](../vision.md#6-supuestos-y-riesgos-iniciales)).

## Alternativas consideradas

1. **Armar el PDF directamente en el código.** Se controla todo, pero cambiar el formato obliga a programar y desplegar, y el diseño del acta queda revuelto con la lógica. Va en contra de RN-03.
2. **Plantilla HTML con marcadores, guardada aparte y con versión, que se convierte a PDF con una librería libre.** Cambiar el formato es editar la plantilla sin tocar la lógica, y no hay licencias. El problema es que pasar de HTML a PDF tiene sus mañas (saltos de página, márgenes) y hay que probarlo bien.
3. **Un servicio comercial de documentos en la nube.** Tiene editor visual, pero es por suscripción (RN-05) y mandaría datos personales fuera de la Universidad ([RT-01](../drivers.md#3-restricciones), [RN-01](../drivers.md#3-restricciones)). Descartado.

## Decisión

Elegimos la opción 2. El acta se arma con datos que ya están en el sistema (lo académico del SIA, las horas validadas, la nota de la empresa y el docente asesor), sin que nadie digite nada, sobre una plantilla HTML versionada que está fuera del código. Cada acta guarda con qué versión de plantilla se generó. Antes de generarla, el sistema revisa que estén todos los datos que pide el reglamento y no la genera si falta alguno. Así cumplimos RN-03 y atacamos OB-04: si nadie retranscribe, no hay errores de transcripción.

## Consecuencias

**Positivas:** si el Consejo cambia el formato, solo se edita la plantilla; desaparecen los errores de transcripción que hoy obligan a reemitir actas; el acta sale en minutos cuando los datos están completos, lo que ayuda a OB-01.

**Negativas:** las plantillas son una cosa más que versionar y probar, y si una plantilla tiene un error, sale mal en todas las actas que se generen con ella. Qué tan fiel quede el PDF depende de la librería, y un formato muy elaborado puede costar varios ajustes. Además la plantilla la edita un desarrollador, no el Consejo.

**Riesgos:** que el formato oficial no se pueda reproducir bien en HTML a PDF. En la primera iteración hacemos un prototipo del acta y lo validamos con el director de programa.

**Vistas que modifica:** [Lógica](../vistas/01-logica.md), [Procesos](../vistas/02-procesos.md), [Desarrollo](../vistas/03-desarrollo.md). Se ve en ESC-03 ([cu09-generar-acta](../diagramas/secuencias/cu09-generar-acta.puml)).
