# ADR-009: Reglas de práctica configurables y versionadas por programa

## Estado

Aceptado (2026-11-02)

## Contexto

Los requisitos y las horas mínimas cambian de un programa a otro ([S-07](../vision.md#6-supuestos-y-riesgos-iniciales)) y el reglamento puede cambiar ([OB-05](../vision.md#2-objetivos-de-negocio)). El director configura las reglas de su programa en [CU-12](../drivers.md#1-casos-de-uso-y-casos-de-uso-primarios).

El driver más fuerte aquí es [EAC-01](../drivers.md#eac-01-mantenibilidad-modificabilidad): un desarrollador con un mes en el proyecto tiene que poder meter las reglas de un programa nuevo (otras horas mínimas y un requisito más) en máximo 16 horas, tocando máximo 2 módulos, y sin que ninguna práctica en curso de otro programa cambie de estado o de reglas.

## Alternativas consideradas

1. **Reglas en el código con condiciones por programa.** Es lo más rápido al principio, pero cada programa nuevo obliga a cambiar código en todas partes donde se validan reglas, y un error puede dañar otros programas. No cumple EAC-01.
2. **Parámetros por programa en la base de datos, con versión y fecha de vigencia, más validadores intercambiables (patrón estrategia) en el módulo de reglas.** Los valores (horas, créditos, promedio, plazos) los cambia el director sin programar. Un tipo de requisito nuevo es un validador nuevo dentro del mismo módulo. Y cada práctica queda amarrada a la versión de reglas con la que se postuló, entonces un cambio no afecta las que están en curso. Requiere más diseño al inicio y el versionado complica las consultas.
3. **Un motor de reglas como Drools.** Permite reglas de cualquier tipo sin programar, pero es otra tecnología que aprender y operar, puede que no esté en el catálogo ([RT-04](../drivers.md#3-restricciones)), y las reglas en su lenguaje son más difíciles de probar. Nuestras reglas (horas, créditos, promedio, materias) no son tan variadas como para justificarlo.

## Decisión

Elegimos la opción 2. El módulo de reglas guarda, por programa, versiones de reglas con fecha de vigencia. Al postularse, cada práctica queda con la versión vigente hasta que se cierra. Los valores los configura el director en CU-12, y los tipos de requisito ("promedio mínimo", "materia aprobada", etc.) son validadores que consultan el SIA por [ADR-004](ADR-004-integracion-sia.md). Con esto cumplimos EAC-01: un programa con valores nuevos no toca código, y un tipo de requisito nuevo solo toca el módulo de reglas y su configuración.

## Consecuencias

**Positivas:** cambiar valores de reglas no necesita desarrollador ni despliegue (OB-05); las prácticas en curso conservan sus reglas; cada validador se prueba por separado.

**Negativas:** un tipo de requisito que no existía sí toca programarlo y desplegarlo, la configuración no cubre todo. El versionado hace más complejo el modelo de datos y la pantalla de configuración. Y si el director se equivoca configurando, afecta todas las postulaciones nuevas de su programa; por eso cada versión pide confirmación y queda en la bitácora ([ADR-012](ADR-012-bitacora-auditoria.md)).

**Riesgos:** que el Consejo apruebe reglas que no encajen en los parámetros (por ejemplo, que dependan de la empresa). Antes de cerrar el modelo revisamos el reglamento de todos los programas.
