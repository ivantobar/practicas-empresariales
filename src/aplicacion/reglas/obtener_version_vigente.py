from datetime import date

from aplicacion.reglas.puertos.repositorio_reglas import RepositorioReglas
from dominio.version_reglas import VersionReglas


class ObtenerVersionVigente:
    """Devuelve la VersionReglas vigente de un programa en una fecha (plan de specs/001).

    La vigente es la de mayor fecha de vigencia que sea menor o igual a la fecha dada;
    las versiones que entran en vigencia después no cuentan (ADR-009). La usa Postularse
    para guardar en la postulación el número de la versión con la que se hizo.
    Escenarios 1, 10 y 11 de specs/001.

    La spec supone que todo programa tiene una versión vigente (decisión 2 de spec.md,
    la crea CU-12). Si el supuesto no se cumple, se lanza LookupError en vez de elegir
    una versión cualquiera.
    """

    def __init__(self, repositorio_reglas: RepositorioReglas) -> None:
        self._repositorio_reglas = repositorio_reglas

    def ejecutar(self, *, programa: str, fecha: date) -> VersionReglas:
        candidatas = [
            version
            for version in self._repositorio_reglas.buscar_versiones(programa)
            if version.fecha_vigencia <= fecha
        ]
        if not candidatas:
            raise LookupError(
                f"el programa {programa!r} no tiene versión de reglas vigente el {fecha.isoformat()}"
            )
        return max(candidatas, key=lambda version: version.fecha_vigencia)
