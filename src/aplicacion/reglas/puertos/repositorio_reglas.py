from typing import Protocol

from dominio.version_reglas import VersionReglas


class RepositorioReglas(Protocol):
    """Puerto para buscar las versiones de reglas de un programa (plan de specs/001).

    Lo define el Módulo Reglas y lo implementa infraestructura/. Las versiones no se
    modifican (ADR-009), por eso aquí solo hay consulta. En esta etapa el adaptador es en
    memoria y las versiones se cargan como datos de ejemplo (DT-01).
    """

    def buscar_versiones(self, programa: str) -> tuple[VersionReglas, ...]:
        """Devuelve todas las versiones de reglas del programa, en cualquier orden.

        Si el programa no tiene versiones, devuelve una tupla vacía. Elegir la versión
        vigente le toca a ObtenerVersionVigente.
        """
        ...
