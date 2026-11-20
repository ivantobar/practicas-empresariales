from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, kw_only=True)
class EventoBitacora:
    """Un registro de auditoría: quién, qué, sobre qué, cuándo y desde dónde (glosario).

    Solo se inserta y no se modifica (ADR-012). No tiene ningún campo para datos
    personales: nada de nombre, documento, promedio ni créditos del estudiante;
    a las personas y objetos se les nombra solo por su identificador.
    "Sobre qué" es opcional, porque un permiso negado no recae sobre ningún objeto.
    """

    quien: str
    que: str
    sobre_que: str | None = None
    cuando: datetime
    desde_donde: str
