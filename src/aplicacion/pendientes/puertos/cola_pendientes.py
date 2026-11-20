from datetime import datetime
from typing import Protocol

from aplicacion.pendientes.trabajo_pendiente import TrabajoPendiente


class ColaPendientes(Protocol):
    """Puerto donde se guardan los trabajos pendientes (glosario).

    Lo define el Módulo Pendientes y lo implementa infraestructura/ (ADR-005). En esta
    etapa el adaptador es en memoria (DT-01).
    """

    def guardar(self, trabajo: TrabajoPendiente) -> None:
        """Agrega un trabajo nuevo a la cola."""
        ...

    def actualizar(self, trabajo: TrabajoPendiente) -> None:
        """Guarda los cambios de un trabajo que ya está en la cola (estado, intentos y próximo intento)."""
        ...

    def listar(self) -> tuple[TrabajoPendiente, ...]:
        """Devuelve todos los trabajos de la cola, en cualquier estado."""
        ...

    def tomar_vencidos(self, ahora: datetime) -> tuple[TrabajoPendiente, ...]:
        """Devuelve los trabajos "pendiente" cuyo próximo intento es menor o igual a ahora.

        No cambia los trabajos: el ProcesadorPendientes los ejecuta y luego los actualiza.
        """
        ...
