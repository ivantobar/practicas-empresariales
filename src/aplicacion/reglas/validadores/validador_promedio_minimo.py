from dominio.datos_academicos import DatosAcademicos
from dominio.requisito import Requisito


class ValidadorPromedioMinimo:
    """ValidadorRequisito para el tipo "promedio mínimo" (ADR-009).

    Se cumple si el promedio del estudiante es mayor o igual al valor exigido
    (plan de specs/001). Cumple el Protocol ValidadorRequisito por su forma, sin
    heredar de él. Escenarios 2, 3 y 10 de specs/001.
    """

    def cumple(self, requisito: Requisito, datos: DatosAcademicos) -> bool:
        return datos.promedio >= requisito.valor_exigido
