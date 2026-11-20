from dataclasses import dataclass, field
from datetime import datetime

from dominio.estado_postulacion import EstadoPostulacion
from dominio.requisito import Requisito


@dataclass
class Postulacion:
    """La solicitud del estudiante ante la Facultad para hacer la práctica (glosario).

    Queda amarrada al número de la versión de reglas vigente al postularse (ADR-009)
    y se verifica con esa versión aunque después entre en vigencia otra (EAC-01).
    Solo puede pasar a "verificada" o a "no cumple requisitos" desde
    "pendiente de verificación" (ADR-004).
    """

    id: str
    estudiante: str
    programa: str
    empresa: str
    numero_version_reglas: int
    fecha: datetime
    estado: EstadoPostulacion = EstadoPostulacion.PENDIENTE_DE_VERIFICACION
    requisitos_incumplidos: tuple[Requisito, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        self.requisitos_incumplidos = tuple(self.requisitos_incumplidos)

    def esta_activa(self) -> bool:
        """Una postulación activa está pendiente de verificación o verificada (glosario)."""
        return self.estado in (
            EstadoPostulacion.PENDIENTE_DE_VERIFICACION,
            EstadoPostulacion.VERIFICADA,
        )

    def marcar_verificada(self) -> None:
        self._validar_desde_pendiente(EstadoPostulacion.VERIFICADA)
        self.estado = EstadoPostulacion.VERIFICADA

    def marcar_no_cumple_requisitos(self, requisitos_incumplidos: tuple[Requisito, ...]) -> None:
        self._validar_desde_pendiente(EstadoPostulacion.NO_CUMPLE_REQUISITOS)
        self.estado = EstadoPostulacion.NO_CUMPLE_REQUISITOS
        self.requisitos_incumplidos = tuple(requisitos_incumplidos)

    def _validar_desde_pendiente(self, nuevo_estado: EstadoPostulacion) -> None:
        if self.estado is not EstadoPostulacion.PENDIENTE_DE_VERIFICACION:
            raise ValueError(
                f"La postulación {self.id} no puede pasar de "
                f"'{self.estado.value}' a '{nuevo_estado.value}': "
                f"solo se permite desde '{EstadoPostulacion.PENDIENTE_DE_VERIFICACION.value}'."
            )
