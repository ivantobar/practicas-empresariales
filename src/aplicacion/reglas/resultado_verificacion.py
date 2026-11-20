from dataclasses import dataclass

from dominio.requisito import Requisito


@dataclass(frozen=True, kw_only=True)
class ResultadoVerificacion:
    """DTO de salida de VerificarRequisitos: si cumple y los requisitos incumplidos (plan de specs/001).

    Cada Requisito incumplido lleva su tipo y su valor exigido, que es lo que lista
    el aviso de "no cumple" (spec de specs/001, nota 6). Si cumple, la lista va vacía.
    Escenarios 2 y 3 de specs/001.
    """

    cumple: bool
    requisitos_incumplidos: tuple[Requisito, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "requisitos_incumplidos", tuple(self.requisitos_incumplidos))
