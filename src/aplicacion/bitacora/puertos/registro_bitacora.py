from typing import Protocol

from dominio.evento_bitacora import EventoBitacora


class RegistroBitacora(Protocol):
    """Puerto donde se guardan los eventos de bitácora (glosario).

    Es de solo inserción (ADR-012): no hay operaciones para modificar ni borrar
    eventos. Lo define el Módulo Bitácora y lo implementa infraestructura/.
    """

    def insertar(self, evento: EventoBitacora) -> None:
        """Agrega el evento al final de la bitácora."""
        ...

    def listar(self) -> tuple[EventoBitacora, ...]:
        """Devuelve todos los eventos en el orden en que se insertaron."""
        ...
