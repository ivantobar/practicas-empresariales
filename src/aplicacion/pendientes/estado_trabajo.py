from enum import Enum


class EstadoTrabajo(Enum):
    """Estado de un trabajo pendiente (ADR-005). Concepto técnico, fuera del modelo de dominio."""

    PENDIENTE = "pendiente"
    TERMINADO = "terminado"
    FALLIDO = "fallido"
