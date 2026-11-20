from dataclasses import dataclass
from datetime import date

from dominio.requisito import Requisito


@dataclass(frozen=True)
class VersionReglas:
    """Las reglas de práctica de un programa desde una fecha de vigencia (glosario).

    No se modifica: un cambio en las reglas es una versión nueva (ADR-009).
    Los requisitos se guardan como tupla para que tampoco se puedan cambiar.
    """

    programa: str
    numero: int
    fecha_vigencia: date
    requisitos: tuple[Requisito, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "requisitos", tuple(self.requisitos))
