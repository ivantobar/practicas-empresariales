from collections.abc import Iterable

from dominio.version_reglas import VersionReglas


class RepositorioReglasEnMemoria:
    """Implementa el puerto RepositorioReglas en memoria (plan de specs/001, DT-01).

    Las versiones se cargan al crearlo, como datos de ejemplo, porque crearlas le toca a
    CU-12. Después solo se consultan: VersionReglas no se modifica (ADR-009) y el
    repositorio no cambia, por eso no necesita threading.Lock.
    Escenarios 1, 10 y 11 de specs/001.
    """

    def __init__(self, versiones: Iterable[VersionReglas] = ()) -> None:
        self._versiones: dict[str, list[VersionReglas]] = {}
        for version in versiones:
            del_programa = self._versiones.setdefault(version.programa, [])
            if any(existente.numero == version.numero for existente in del_programa):
                raise ValueError(
                    f"ya existe la versión {version.numero} de reglas del programa {version.programa!r}"
                )
            del_programa.append(version)

    def buscar_versiones(self, programa: str) -> tuple[VersionReglas, ...]:
        return tuple(self._versiones.get(programa, ()))
