from enum import Enum


class TipoRequisito(Enum):
    """Tipo de requisito académico de una versión de reglas (glosario)."""

    PROMEDIO_MINIMO = "promedio mínimo"
    CREDITOS_APROBADOS_MINIMOS = "créditos aprobados mínimos"
