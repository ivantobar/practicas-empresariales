# ADR-011: Aprobación trazable del acta y acta que no se puede modificar

## Estado

Aceptado (2026-11-02)

## Contexto

El docente asesor y el director de programa aprueban el acta electrónicamente ([CU-10](../drivers.md#1-casos-de-uso-y-casos-de-uso-primarios)).

- [S-06](../vision.md#6-supuestos-y-riesgos-iniciales): basta con una aprobación electrónica trazable de los dos. La firma digital certificada está fuera del alcance ([alcance](../vision.md#3-alcance)).
- [RN-02](../drivers.md#3-restricciones): las actas aprobadas se conservan según la tabla de retención y no se pueden modificar ni borrar.
- [OB-06](../vision.md#2-objetivos-de-negocio): en una auditoría hay que mostrar en máximo 1 día hábil quién aprobó cada acta y cuándo.
- [RN-05](../drivers.md#3-restricciones): sin licencias pagas.
- [R-03](../vision.md#6-supuestos-y-riesgos-iniciales): puede que el área jurídica termine pidiendo firma certificada.

## Alternativas consideradas

1. **Marcar el acta como "aprobada" con un campo en la base de datos.** Es lo más simple, pero no demuestra qué documento exacto se aprobó, y el acta podría cambiar después sin que nadie se dé cuenta. No cumple RN-02 ni sirve como evidencia para OB-06.
2. **Aprobación trazable y acta que no se puede modificar.** Al aprobar se guarda quién (con la identidad institucional de [ADR-006](ADR-006-autenticacion-institucional.md)), cuándo, desde dónde y una huella digital del PDF (un código que cambia si el archivo cambia aunque sea un poquito). Cuando los dos aprueban, el acta ya no se puede modificar ni borrar. Así se demuestra qué documento se aprobó y que no cambió, y sin pagar nada. Pero vale menos legalmente que una firma certificada.
3. **Firma digital certificada con una entidad de certificación.** Es lo que más vale legalmente, pero está fuera del alcance, cuesta (RN-05), y según S-06 no hace falta.

## Decisión

Elegimos la opción 2 porque cumple S-06, RN-02 y OB-06 sin violar RN-05 ni salirnos del alcance. El acta pasa por estos estados: generada, aprobada por el docente, aprobada por el director y cerrada. Cuando se cierra, el PDF y sus aprobaciones quedan de solo lectura: en esas tablas la base de datos solo deja insertar, y el archivo se guarda con la política de conservación de la tabla de retención. Si después se encuentra un error, el acta no se edita: se emite una nueva que reemplaza a la anterior y se guardan las dos. La opción 3 queda escrita por si pasa R-03.

## Consecuencias

**Positivas:** se puede demostrar en cualquier momento quién aprobó qué documento y cuándo; ningún acta aprobada se pierde ni se altera; no hay costos de certificados.

**Negativas:** legalmente vale menos que una firma certificada, y si alguien externo la exige, esta acta no le sirve. Para corregir un error toca emitir un acta nueva en vez de editarla, que es más trámite aunque deja la historia. Y el almacenamiento solo crece hasta que la tabla de retención deje borrar.

**Riesgos:** R-03, que el área jurídica no acepte S-06 y pida firma certificada. Lo validamos antes de construir CU-10; si la piden, se hace un ADR nuevo que reemplace este con la opción 3 y se renegocia RN-05 con la Decanatura.
