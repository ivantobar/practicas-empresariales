from collections.abc import Mapping

from aplicacion.reglas.puertos.consulta_academica import ConsultaAcademica
from aplicacion.reglas.puertos.repositorio_reglas import RepositorioReglas
from aplicacion.reglas.resultado_verificacion import ResultadoVerificacion
from aplicacion.reglas.validador_requisito import ValidadorRequisito
from dominio.tipo_requisito import TipoRequisito
from dominio.version_reglas import VersionReglas


class VerificarRequisitos:
    """Verifica los requisitos de una versión de reglas contra los datos del SIA (plan de specs/001).

    Con un estudiante, un programa y un número de versión, consulta ConsultaAcademica y
    aplica el ValidadorRequisito de cada requisito de esa versión. Usa la versión dada,
    no la vigente: la postulación conserva la versión con la que se hizo (ADR-009,
    escenario 10). Los validadores llegan por constructor, uno por TipoRequisito, y
    los arma main.py: un tipo nuevo es un validador nuevo, sin tocar esta clase (EAC-01).

    No atrapa ConsultaAcademicaFallida: la deja pasar para que VerificarPostulacion la
    convierta en FallaReintentable (ADR-005, escenarios 6 y 7). Solo la llama el trabajo
    "verificar en SIA", nunca mientras el estudiante espera (ADR-004).
    Escenarios 2, 3, 6, 7 y 10 de specs/001.

    Si la versión no existe o un tipo de requisito no tiene validador, se lanza
    LookupError antes de consultar el SIA, en vez de dar un resultado inventado.
    """

    def __init__(
        self,
        *,
        consulta_academica: ConsultaAcademica,
        repositorio_reglas: RepositorioReglas,
        validadores: Mapping[TipoRequisito, ValidadorRequisito],
    ) -> None:
        self._consulta_academica = consulta_academica
        self._repositorio_reglas = repositorio_reglas
        self._validadores = dict(validadores)

    def ejecutar(self, *, estudiante: str, programa: str, numero_version: int) -> ResultadoVerificacion:
        version = self._buscar_version(programa, numero_version)
        validadores = [(requisito, self._validador_de(requisito.tipo)) for requisito in version.requisitos]

        datos = self._consulta_academica.consultar(estudiante)

        incumplidos = tuple(
            requisito for requisito, validador in validadores if not validador.cumple(requisito, datos)
        )
        return ResultadoVerificacion(cumple=not incumplidos, requisitos_incumplidos=incumplidos)

    def _buscar_version(self, programa: str, numero_version: int) -> VersionReglas:
        for version in self._repositorio_reglas.buscar_versiones(programa):
            if version.numero == numero_version:
                return version
        raise LookupError(f"el programa {programa!r} no tiene la versión de reglas {numero_version}")

    def _validador_de(self, tipo: TipoRequisito) -> ValidadorRequisito:
        try:
            return self._validadores[tipo]
        except KeyError:
            raise LookupError(f"no hay ValidadorRequisito para el tipo {tipo.value!r}") from None
