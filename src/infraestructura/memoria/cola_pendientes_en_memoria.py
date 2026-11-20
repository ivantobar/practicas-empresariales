import copy
import threading
from datetime import datetime

from aplicacion.pendientes.estado_trabajo import EstadoTrabajo
from aplicacion.pendientes.trabajo_pendiente import TrabajoPendiente


class ColaPendientesEnMemoria:
    """Implementa el puerto ColaPendientes en memoria (plan de specs/001, DT-01).

    Todas las operaciones se protegen con un threading.Lock para que varios estudiantes
    puedan registrar su trabajo "verificar en SIA" al mismo tiempo sin perder ninguno
    (escenario 5), mientras el ProcesadorPendientes toma y actualiza trabajos.

    Guarda y devuelve copias de los trabajos, como lo haría una base de datos: un cambio
    de estado, de intentos o de próximo intento solo queda guardado cuando se llama a
    actualizar(). Los trabajos se devuelven en el orden en que se guardaron.
    """

    def __init__(self) -> None:
        self._trabajos: dict[str, TrabajoPendiente] = {}
        self._candado = threading.Lock()

    def guardar(self, trabajo: TrabajoPendiente) -> None:
        with self._candado:
            if trabajo.id in self._trabajos:
                raise ValueError(f"ya existe el trabajo {trabajo.id!r}")
            self._trabajos[trabajo.id] = copy.copy(trabajo)

    def actualizar(self, trabajo: TrabajoPendiente) -> None:
        with self._candado:
            if trabajo.id not in self._trabajos:
                raise LookupError(f"no existe el trabajo {trabajo.id!r}")
            self._trabajos[trabajo.id] = copy.copy(trabajo)

    def listar(self) -> tuple[TrabajoPendiente, ...]:
        with self._candado:
            return tuple(copy.copy(trabajo) for trabajo in self._trabajos.values())

    def tomar_vencidos(self, ahora: datetime) -> tuple[TrabajoPendiente, ...]:
        with self._candado:
            return tuple(
                copy.copy(trabajo)
                for trabajo in self._trabajos.values()
                if trabajo.estado is EstadoTrabajo.PENDIENTE
                and trabajo.proximo_intento <= ahora
            )
