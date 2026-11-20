import copy
import threading

from dominio.postulacion import Postulacion


class RepositorioPostulacionesEnMemoria:
    """Implementa el puerto RepositorioPostulaciones en memoria (plan de specs/001, DT-01).

    Todas las operaciones se protegen con un threading.Lock para que varios estudiantes
    puedan postularse al mismo tiempo sin perder postulaciones (escenario 5).

    Guarda y devuelve copias de las postulaciones, como lo haría una base de datos: un
    cambio de estado solo queda guardado cuando se llama a actualizar().
    """

    def __init__(self) -> None:
        self._postulaciones: dict[str, Postulacion] = {}
        self._candado = threading.Lock()

    def guardar(self, postulacion: Postulacion) -> None:
        with self._candado:
            if postulacion.id in self._postulaciones:
                raise ValueError(f"ya existe la postulación {postulacion.id!r}")
            self._postulaciones[postulacion.id] = copy.copy(postulacion)

    def actualizar(self, postulacion: Postulacion) -> None:
        with self._candado:
            if postulacion.id not in self._postulaciones:
                raise LookupError(f"no existe la postulación {postulacion.id!r}")
            self._postulaciones[postulacion.id] = copy.copy(postulacion)

    def buscar_por_id(self, id: str) -> Postulacion | None:
        with self._candado:
            postulacion = self._postulaciones.get(id)
            return copy.copy(postulacion) if postulacion is not None else None

    def listar_por_estudiante(self, estudiante: str) -> tuple[Postulacion, ...]:
        with self._candado:
            return tuple(
                copy.copy(postulacion)
                for postulacion in self._postulaciones.values()
                if postulacion.estudiante == estudiante
            )
