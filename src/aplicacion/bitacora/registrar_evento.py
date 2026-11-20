from datetime import datetime

from aplicacion.bitacora.puertos.registro_bitacora import RegistroBitacora
from dominio.evento_bitacora import EventoBitacora


class RegistrarEvento:
    """Arma el EventoBitacora con la fecha actual y lo inserta (plan de specs/001).

    Es lo que usan los demás módulos para escribir en la bitácora (ADR-012).
    Solo recibe identificadores: quién, qué, sobre qué y desde dónde; nunca
    datos personales. El "cuándo" lo pone este caso de uso, no quien llama.
    """

    def __init__(self, registro_bitacora: RegistroBitacora) -> None:
        self._registro_bitacora = registro_bitacora

    def ejecutar(
        self,
        *,
        quien: str,
        que: str,
        desde_donde: str,
        sobre_que: str | None = None,
    ) -> EventoBitacora:
        evento = EventoBitacora(
            quien=quien,
            que=que,
            sobre_que=sobre_que,
            cuando=datetime.now(),
            desde_donde=desde_donde,
        )
        self._registro_bitacora.insertar(evento)
        return evento
