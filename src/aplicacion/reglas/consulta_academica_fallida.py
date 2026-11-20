class ConsultaAcademicaFallida(Exception):
    """Error de aplicación para un SIA caído, lento o que responde con error (plan de specs/001).

    Lo lanza el adaptador de ConsultaAcademica cuando el SIA no responde en 5 s o
    responde con error: el adaptador traduce toda falla a este error (ADR-004).
    VerificarRequisitos lo deja pasar y VerificarPostulacion lo convierte en
    FallaReintentable para que el trabajo se reintente (ADR-005).
    Escenarios 6 y 7 de specs/001.
    """
