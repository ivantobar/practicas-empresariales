from aplicacion.bitacora.registrar_evento import RegistrarEvento
from aplicacion.pendientes.falla_reintentable import FallaReintentable
from aplicacion.pendientes.registrar_trabajo import RegistrarTrabajo
from aplicacion.pendientes.trabajo_pendiente import TrabajoPendiente
from aplicacion.postulacion.puertos.repositorio_postulaciones import RepositorioPostulaciones
from aplicacion.reglas.consulta_academica_fallida import ConsultaAcademicaFallida
from aplicacion.reglas.verificar_requisitos import VerificarRequisitos
from dominio.estado_postulacion import EstadoPostulacion
from dominio.postulacion import Postulacion


class VerificarPostulacion:
    """ManejadorTrabajo del tipo "verificar en SIA" (plan de specs/001, ESC-01).

    Lo ejecuta el ProcesadorPendientes en segundo plano, nunca mientras el estudiante
    espera (ADR-004). main.py lo registra para el tipo "verificar en SIA"; así el Módulo
    Pendientes no conoce al Módulo Postulación (vista de usos). La referencia del trabajo
    es el id de la postulación.

    En orden:
    1. Busca la postulación de la referencia del trabajo.
    2. Llama a VerificarRequisitos con la versión de reglas guardada en la postulación,
       no con la vigente (ADR-009, escenario 10).
    3. Cambia el estado a "verificada" o a "no cumple requisitos" con los requisitos
       incumplidos y su valor exigido (escenarios 2 y 3), y actualiza la postulación.
    4. Registra el evento de bitácora del cambio de estado, solo con identificadores
       (ADR-012). Quién y desde dónde son "procesador de pendientes" (DP-02).
    5. Registra el trabajo "avisar al estudiante" con el id de la postulación (DP-01).

    Si recibe ConsultaAcademicaFallida (SIA caído, lento o con error), lanza
    FallaReintentable y la postulación no cambia: sigue guardada en "pendiente de
    verificación" y el ProcesadorPendientes reprograma el trabajo (ADR-005, escenarios 6 y 7).
    Si la postulación no existe se lanza LookupError, en vez de inventar un resultado.
    """

    TIPO_VERIFICAR_EN_SIA = "verificar en SIA"
    TIPO_AVISAR_AL_ESTUDIANTE = "avisar al estudiante"
    PROCESADOR_DE_PENDIENTES = "procesador de pendientes"

    def __init__(
        self,
        *,
        repositorio_postulaciones: RepositorioPostulaciones,
        verificar_requisitos: VerificarRequisitos,
        registrar_evento: RegistrarEvento,
        registrar_trabajo: RegistrarTrabajo,
    ) -> None:
        self._repositorio_postulaciones = repositorio_postulaciones
        self._verificar_requisitos = verificar_requisitos
        self._registrar_evento = registrar_evento
        self._registrar_trabajo = registrar_trabajo

    def ejecutar(self, trabajo: TrabajoPendiente) -> None:
        postulacion = self._buscar_postulacion(trabajo.referencia)

        try:
            resultado = self._verificar_requisitos.ejecutar(
                estudiante=postulacion.estudiante,
                programa=postulacion.programa,
                numero_version=postulacion.numero_version_reglas,
            )
        except ConsultaAcademicaFallida as error:
            raise FallaReintentable(str(error)) from error

        estado_anterior = postulacion.estado
        if resultado.cumple:
            postulacion.marcar_verificada()
        else:
            postulacion.marcar_no_cumple_requisitos(resultado.requisitos_incumplidos)
        self._repositorio_postulaciones.actualizar(postulacion)

        self._registrar_evento.ejecutar(
            quien=self.PROCESADOR_DE_PENDIENTES,
            que=self._describir_cambio(estado_anterior, postulacion.estado),
            sobre_que=postulacion.id,
            desde_donde=self.PROCESADOR_DE_PENDIENTES,
        )

        self._registrar_trabajo.ejecutar(
            tipo=self.TIPO_AVISAR_AL_ESTUDIANTE,
            referencia=postulacion.id,
        )

    def _buscar_postulacion(self, id: str) -> Postulacion:
        postulacion = self._repositorio_postulaciones.buscar_por_id(id)
        if postulacion is None:
            raise LookupError(f"no existe la postulación {id!r}")
        return postulacion

    @staticmethod
    def _describir_cambio(anterior: EstadoPostulacion, nuevo: EstadoPostulacion) -> str:
        return f"cambio de '{anterior.value}' a '{nuevo.value}'"
