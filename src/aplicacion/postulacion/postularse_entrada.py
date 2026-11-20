from dataclasses import dataclass

from aplicacion.acceso.sesion import Sesion


@dataclass(frozen=True, kw_only=True)
class PostularseEntrada:
    """DTO de entrada del caso de uso Postularse: sesión, empresa y origen (plan de specs/001).

    La sesión llega ya validada (ADR-006, DT-04); de ella salen el estudiante
    (usuario) y el programa (ámbito). La empresa es solo el nombre de la empresa
    de la plaza que da el estudiante: el convenio no se revisa (decisión 1 de spec.md).
    El origen es el "desde dónde" que va al evento de bitácora (ADR-012).
    Escenarios 1 y 9 de specs/001.
    """

    sesion: Sesion
    empresa: str
    origen: str
