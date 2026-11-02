# ADR-001: Monolito modular con puertos y adaptadores

## Estado

Aceptado (2026-11-02)

## Contexto

Tenemos que decidir cómo dividir el sistema en bloques grandes ([PA-01](../drivers.md#4-preocupaciones-arquitectónicas)).

Por un lado la carga es baja: según [S-03](../vision.md#6-supuestos-y-riesgos-iniciales) hay entre 170 y 250 prácticas activas y unas decenas de usuarios a la vez, y [R-04](../vision.md#6-supuestos-y-riesgos-iniciales) dice que no hay que sobredimensionar. Por otro lado las reglas cambian según el programa, y [EAC-01](../drivers.md#eac-01-mantenibilidad-modificabilidad) pide que un cambio de reglas toque máximo 2 módulos. Además dependemos de cosas externas que pueden cambiar o fallar: el SIA ([RT-03](../drivers.md#3-restricciones)), el login institucional ([RT-02](../drivers.md#3-restricciones)) y el correo.

## Alternativas consideradas

1. **Monolito en capas normales (presentación, negocio, datos).** Es lo más fácil y lo que más conocemos. El problema es que las capas quedan organizadas por tipo de clase y no por tema, entonces cambiar una regla obliga a tocar controladores, servicios y repositorios en varias partes. Tampoco se puede probar la lógica sin la base de datos. No cumpliría EAC-01.
2. **Monolito modular con puertos y adaptadores.** Un solo desplegable y una sola base de datos, pero dividido por módulos de negocio (postulación, horas, evaluación, actas, reglas, administración). El SIA, el login, el correo y la base de datos se conectan por interfaces, así que se pueden cambiar sin tocar el negocio. Tiene más clases e interfaces que la opción 1.
3. **Microservicios.** Cada módulo escala y se despliega aparte, pero con esta carga eso no se necesita. Habría que manejar red entre servicios, consistencia eventual y un bus de mensajes, y todo eso lo tendría que operar el Área de Sistemas. Es justo lo que advierte R-04.

## Decisión

Elegimos la opción 2. Las reglas quedan en su propio módulo y el resto no se entera cuando cambian (EAC-01), y no pagamos la complejidad de los microservicios, que con la carga de S-03 no se justifica. Las dependencias siempre apuntan hacia el negocio y los módulos solo se hablan por sus interfaces públicas.

## Consecuencias

**Positivas:** un cambio de reglas se queda en el módulo de reglas; cambiar el SIA o la base de datos toca solo un adaptador; la lógica se puede probar sin SIA ni base de datos; hay un solo artefacto para desplegar y respaldar.

**Negativas:** hay más código de "soporte" (interfaces, adaptadores, mapeos). Si algún día un módulo necesita mucha más capacidad, toca escalar todo el sistema. Y nada en el lenguaje impide que un módulo use cosas internas de otro: depende de la disciplina del equipo.

**Riesgos:** que con el tiempo los módulos se acoplen. Para evitarlo ponemos pruebas de arquitectura que fallen si un módulo importa el interior de otro. Si la carga real fuera mucho mayor que S-03, se separaría un módulo con un ADR nuevo.
