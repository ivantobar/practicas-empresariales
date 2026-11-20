from enum import Enum


class EstadoPostulacion(Enum):
    """Estado de la postulación (glosario). CU-02 agregará aprobada y rechazada."""

    PENDIENTE_DE_VERIFICACION = "pendiente de verificación"
    VERIFICADA = "verificada"
    NO_CUMPLE_REQUISITOS = "no cumple requisitos"
