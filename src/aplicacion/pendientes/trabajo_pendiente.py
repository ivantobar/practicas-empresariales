from dataclasses import dataclass
from datetime import datetime, timedelta

from aplicacion.pendientes.estado_trabajo import EstadoTrabajo


@dataclass(kw_only=True)
class TrabajoPendiente:
    """Una llamada externa que puede fallar, guardada para hacerla y reintentarla en segundo plano (glosario).

    Concepto técnico, fuera del modelo de dominio (ADR-005). La referencia es el
    identificador del objeto sobre el que trabaja (por ejemplo, el id de la postulación).

    Si un intento falla, el trabajo se reprograma con espera creciente de 1, 2, 4 y 8 min
    y luego 15 min como máximo. Si un intento falla cuando el trabajo ya tiene 24 h o más
    desde que se creó, queda "fallido" y no se vuelve a intentar.
    """

    ESPERAS_EN_MINUTOS = (1, 2, 4, 8, 15)
    LIMITE_DE_REINTENTOS = timedelta(hours=24)

    id: str
    tipo: str
    referencia: str
    creado_en: datetime
    proximo_intento: datetime
    estado: EstadoTrabajo = EstadoTrabajo.PENDIENTE
    intentos_fallidos: int = 0

    def siguiente_espera(self) -> timedelta:
        """Espera tras el siguiente intento fallido: 1, 2, 4, 8 y luego 15, 15, ... minutos."""
        posicion = min(self.intentos_fallidos, len(self.ESPERAS_EN_MINUTOS) - 1)
        return timedelta(minutes=self.ESPERAS_EN_MINUTOS[posicion])

    def cumplio_24_horas(self, ahora: datetime) -> bool:
        """Regla de las 24 h: el trabajo tiene 24 h o más desde que se creó."""
        return ahora - self.creado_en >= self.LIMITE_DE_REINTENTOS

    def registrar_intento_fallido(self, ahora: datetime) -> None:
        """Cuenta el intento fallido y reprograma el trabajo, o lo marca "fallido" si ya cumplió 24 h."""
        self._validar_pendiente()
        if self.cumplio_24_horas(ahora):
            self.intentos_fallidos += 1
            self.estado = EstadoTrabajo.FALLIDO
            return
        self.proximo_intento = ahora + self.siguiente_espera()
        self.intentos_fallidos += 1

    def marcar_terminado(self) -> None:
        self._validar_pendiente()
        self.estado = EstadoTrabajo.TERMINADO

    def _validar_pendiente(self) -> None:
        if self.estado is not EstadoTrabajo.PENDIENTE:
            raise ValueError(
                f"El trabajo {self.id} está '{self.estado.value}': "
                f"solo se puede actualizar un trabajo '{EstadoTrabajo.PENDIENTE.value}'."
            )
