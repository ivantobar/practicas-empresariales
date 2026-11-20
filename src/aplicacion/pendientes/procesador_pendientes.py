from datetime import datetime

from aplicacion.pendientes.estado_trabajo import EstadoTrabajo
from aplicacion.pendientes.falla_reintentable import FallaReintentable
from aplicacion.pendientes.manejador_trabajo import ManejadorTrabajo
from aplicacion.pendientes.puertos.cola_pendientes import ColaPendientes
from aplicacion.pendientes.registrar_trabajo import RegistrarTrabajo
from aplicacion.pendientes.trabajo_pendiente import TrabajoPendiente


class ProcesadorPendientes:
    """El proceso que cada minuto toma los trabajos vencidos y los ejecuta (glosario, ADR-005).

    En cada ciclo toma de la ColaPendientes los trabajos vencidos a la hora dada y busca
    el ManejadorTrabajo registrado para su tipo:

    - Si el manejador termina sin error, el trabajo queda "terminado" (escenario 2).
    - Si lanza FallaReintentable, el trabajo se reprograma con espera de 1, 2, 4, 8 y
      máximo 15 min (escenarios 6 y 7). Si ya tiene 24 h, queda "fallido" y se registra
      el trabajo "avisar al administrador" con el id del trabajo fallido como referencia
      (escenario 8).

    Los manejadores los registra main.py con registrar_manejador(tipo, manejador), así el
    Módulo Pendientes no conoce a ningún módulo de negocio (vista de usos). Un trabajo
    cuyo tipo no tiene manejador registrado no se toca y sigue "pendiente": en specs/001
    los avisos solo se registran y quién los envía se decide en otra funcionalidad (DP-01).

    La hora "ahora" la da quien llama (real o simulada) y se usa también para el trabajo
    "avisar al administrador".
    """

    TIPO_AVISAR_AL_ADMINISTRADOR = "avisar al administrador"

    def __init__(
        self,
        cola_pendientes: ColaPendientes,
        registrar_trabajo: RegistrarTrabajo,
    ) -> None:
        self._cola_pendientes = cola_pendientes
        self._registrar_trabajo = registrar_trabajo
        self._manejadores: dict[str, ManejadorTrabajo] = {}

    def registrar_manejador(self, tipo: str, manejador: ManejadorTrabajo) -> None:
        """Asocia un tipo de trabajo con el manejador que lo ejecuta."""
        self._manejadores[tipo] = manejador

    def ejecutar_ciclo(self, ahora: datetime) -> None:
        for trabajo in self._cola_pendientes.tomar_vencidos(ahora):
            manejador = self._manejadores.get(trabajo.tipo)
            if manejador is None:
                continue
            self._ejecutar_trabajo(trabajo, manejador, ahora)

    def _ejecutar_trabajo(
        self,
        trabajo: TrabajoPendiente,
        manejador: ManejadorTrabajo,
        ahora: datetime,
    ) -> None:
        try:
            manejador.ejecutar(trabajo)
        except FallaReintentable:
            trabajo.registrar_intento_fallido(ahora)
            self._cola_pendientes.actualizar(trabajo)
            if trabajo.estado is EstadoTrabajo.FALLIDO:
                self._registrar_trabajo.ejecutar(
                    tipo=self.TIPO_AVISAR_AL_ADMINISTRADOR,
                    referencia=trabajo.id,
                    ahora=ahora,
                )
            return
        trabajo.marcar_terminado()
        self._cola_pendientes.actualizar(trabajo)
