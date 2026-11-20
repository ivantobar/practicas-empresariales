class PermisoNegado(Exception):
    """Error que se lanza cuando la sesión no tiene el permiso (plan de specs/001).

    Lo lanza ValidarPermiso después de registrar en la bitácora el evento de permiso
    negado (ADR-008, ADR-012). El caso de uso no lo atrapa: el controlador web lo
    traducirá después (DT-04). Escenario 9 de specs/001.
    """
