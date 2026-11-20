from dataclasses import dataclass

from dominio.tipo_requisito import TipoRequisito


@dataclass(frozen=True)
class Requisito:
    """Una condición académica de una versión de reglas: tipo y valor exigido (glosario)."""

    tipo: TipoRequisito
    valor_exigido: float
