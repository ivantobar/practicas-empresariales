class PostulacionActivaExistente(Exception):
    """Error con el mensaje "ya tienes una postulación en curso" (plan de specs/001).

    Lo lanza Postularse cuando el estudiante ya tiene una postulación activa
    (Postulacion.esta_activa()): pendiente de verificación o verificada. El caso de
    uso no lo atrapa: el controlador web lo traducirá después (DT-04).
    Escenario 4 de specs/001.
    """

    MENSAJE = "ya tienes una postulación en curso"

    def __init__(self) -> None:
        super().__init__(self.MENSAJE)
