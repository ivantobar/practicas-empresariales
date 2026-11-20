from typing import Protocol

from dominio.datos_academicos import DatosAcademicos


class ConsultaAcademica(Protocol):
    """Puerto para consultar los datos académicos de un estudiante en el SIA (glosario, RT-03).

    Lo define el Módulo Reglas y lo implementa infraestructura/ (Adaptador SIA). Es la
    única forma de llegar al SIA (ADR-004) y nunca se usa mientras el estudiante espera:
    solo lo llama VerificarRequisitos desde el trabajo "verificar en SIA" (ADR-005).
    En esta etapa el adaptador es el simulador ConsultaAcademicaSimulada (DT-01).
    Escenarios 2, 3, 6 y 7 de specs/001.
    """

    def consultar(self, estudiante: str) -> DatosAcademicos:
        """Devuelve el promedio y los créditos aprobados del estudiante según el SIA.

        La espera máxima es de 5 s. Si el SIA no responde en ese tiempo, está caído o
        responde con error, el adaptador lanza ConsultaAcademicaFallida: ninguna otra
        falla del SIA sale de este puerto (ADR-004).
        """
        ...
