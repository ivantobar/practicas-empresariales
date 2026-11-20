import threading

from dominio.evento_bitacora import EventoBitacora


class RegistroBitacoraEnMemoria:
    """Implementa el puerto RegistroBitacora en memoria (plan de specs/001, DT-01).

    Es de solo inserción (ADR-012): no tiene operaciones para modificar ni borrar
    eventos, y listar() devuelve una tupla para que nadie cambie la lista guardada.
    Los EventoBitacora son inmutables, así que no hace falta copiarlos.

    Todas las operaciones se protegen con un threading.Lock para que varios estudiantes
    y el ProcesadorPendientes puedan registrar eventos al mismo tiempo sin perder
    ninguno. Los eventos se devuelven en el orden en que se insertaron.
    """

    def __init__(self) -> None:
        self._eventos: list[EventoBitacora] = []
        self._candado = threading.Lock()

    def insertar(self, evento: EventoBitacora) -> None:
        with self._candado:
            self._eventos.append(evento)

    def listar(self) -> tuple[EventoBitacora, ...]:
        with self._candado:
            return tuple(self._eventos)
