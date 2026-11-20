class FallaReintentable(Exception):
    """Error con el que un manejador indica que el intento falló y se debe reintentar (plan de specs/001).

    Lo lanza un ManejadorTrabajo cuando la llamada externa falla, por ejemplo
    VerificarPostulacion cuando el SIA no responde en 5 s o responde con error.
    El ProcesadorPendientes lo atrapa y reprograma el trabajo, o lo marca "fallido"
    si ya tiene 24 h (ADR-005). Escenarios 6 y 7 de specs/001.
    """
