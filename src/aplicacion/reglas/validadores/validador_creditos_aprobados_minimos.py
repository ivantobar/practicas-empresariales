from dominio.datos_academicos import DatosAcademicos
from dominio.requisito import Requisito


class ValidadorCreditosAprobadosMinimos:
    """ValidadorRequisito para el tipo "créditos aprobados mínimos" (ADR-009).

    Se cumple si los créditos aprobados del estudiante son mayores o iguales al
    valor exigido (plan de specs/001). Cumple el Protocol ValidadorRequisito por su
    forma, sin heredar de él. Escenarios 2 y 3 de specs/001.
    """

    def cumple(self, requisito: Requisito, datos: DatosAcademicos) -> bool:
        return datos.creditos_aprobados >= requisito.valor_exigido
