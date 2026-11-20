from dataclasses import dataclass


@dataclass(frozen=True)
class DatosAcademicos:
    """Lo que el SIA devuelve de un estudiante: promedio y créditos aprobados (glosario).

    Es un objeto de valor: no se modifica. Son datos personales (RN-01),
    por eso no se copian a la bitácora (ADR-012).
    """

    promedio: float
    creditos_aprobados: int
