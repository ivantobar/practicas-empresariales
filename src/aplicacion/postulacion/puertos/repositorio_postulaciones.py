from typing import Protocol

from dominio.postulacion import Postulacion


class RepositorioPostulaciones(Protocol):
    """Puerto para guardar y consultar las postulaciones (plan de specs/001).

    Lo define el Módulo Postulación y lo implementa infraestructura/. En esta etapa el
    adaptador es en memoria (DT-01).
    """

    def guardar(self, postulacion: Postulacion) -> None:
        """Agrega una postulación nueva."""
        ...

    def actualizar(self, postulacion: Postulacion) -> None:
        """Guarda los cambios de una postulación que ya existe (estado y requisitos incumplidos)."""
        ...

    def buscar_por_id(self, id: str) -> Postulacion | None:
        """Devuelve la postulación con ese id, o None si no existe."""
        ...

    def listar_por_estudiante(self, estudiante: str) -> tuple[Postulacion, ...]:
        """Devuelve todas las postulaciones del estudiante, en cualquier estado.

        Si el estudiante no tiene postulaciones, devuelve una tupla vacía. Saber si tiene
        una activa le toca al caso de uso, con esta_activa().
        """
        ...
