from typing import Protocol

from dominio.datos_academicos import DatosAcademicos
from dominio.requisito import Requisito


class ValidadorRequisito(Protocol):
    """La pieza del Módulo Reglas que revisa un tipo de requisito contra los datos académicos (glosario).

    Hay un validador por cada TipoRequisito y son intercambiables (patrón estrategia,
    ADR-009): un tipo de requisito nuevo es un validador nuevo dentro del Módulo Reglas,
    sin tocar a Postulación (EAC-01). Lo usa VerificarRequisitos con los DatosAcademicos
    que devuelve ConsultaAcademica. No es un puerto hacia infraestructura, por eso no va
    en puertos/. Escenarios 2 y 3 de specs/001.
    """

    def cumple(self, requisito: Requisito, datos: DatosAcademicos) -> bool:
        """Dice si el requisito se cumple con los datos académicos del estudiante.

        Un requisito se cumple si el valor del estudiante es mayor o igual al
        valor exigido (plan de specs/001, ADR-009).
        """
        ...
