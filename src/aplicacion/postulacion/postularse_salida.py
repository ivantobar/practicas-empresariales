from dataclasses import dataclass

from dominio.estado_postulacion import EstadoPostulacion


@dataclass(frozen=True, kw_only=True)
class PostularseSalida:
    """DTO de salida del caso de uso Postularse: id, estado y mensaje (plan de specs/001).

    El caso de uso responde sin consultar el SIA (ADR-004), así que el estado es
    "pendiente de verificación" y el mensaje es la confirmación que recibe el
    estudiante: "postulación recibida, te avisamos el resultado".
    Escenarios 1 y 5 de specs/001.
    """

    id: str
    estado: EstadoPostulacion
    mensaje: str = "postulación recibida, te avisamos el resultado"
