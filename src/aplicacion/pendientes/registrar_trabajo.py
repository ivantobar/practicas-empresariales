from datetime import datetime
from uuid import uuid4

from aplicacion.pendientes.puertos.cola_pendientes import ColaPendientes
from aplicacion.pendientes.trabajo_pendiente import TrabajoPendiente


class RegistrarTrabajo:
    """Crea un TrabajoPendiente listo para ejecutarse de inmediato y lo guarda en la cola (plan de specs/001).

    Es lo que usan los demás módulos para dejar una llamada externa que puede fallar
    (verificar en SIA, avisar al estudiante, avisar al administrador) como trabajo
    pendiente (ADR-005). El trabajo queda "pendiente", sin intentos fallidos y con el
    próximo intento igual a la hora de creación, así que el ProcesadorPendientes lo
    toma en su siguiente ciclo.

    Si no se da "ahora" se usa la hora actual; el ProcesadorPendientes pasa su propia
    hora para que los trabajos que registra queden en la misma hora (simulada o real).
    """

    def __init__(self, cola_pendientes: ColaPendientes) -> None:
        self._cola_pendientes = cola_pendientes

    def ejecutar(
        self,
        *,
        tipo: str,
        referencia: str,
        ahora: datetime | None = None,
    ) -> TrabajoPendiente:
        momento = ahora if ahora is not None else datetime.now()
        trabajo = TrabajoPendiente(
            id=str(uuid4()),
            tipo=tipo,
            referencia=referencia,
            creado_en=momento,
            proximo_intento=momento,
        )
        self._cola_pendientes.guardar(trabajo)
        return trabajo
