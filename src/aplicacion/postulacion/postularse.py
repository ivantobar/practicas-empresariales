from datetime import datetime
from uuid import uuid4

from aplicacion.acceso.validar_permiso import ValidarPermiso
from aplicacion.bitacora.registrar_evento import RegistrarEvento
from aplicacion.pendientes.registrar_trabajo import RegistrarTrabajo
from aplicacion.postulacion.postulacion_activa_existente import PostulacionActivaExistente
from aplicacion.postulacion.postularse_entrada import PostularseEntrada
from aplicacion.postulacion.postularse_salida import PostularseSalida
from aplicacion.postulacion.puertos.repositorio_postulaciones import RepositorioPostulaciones
from aplicacion.reglas.obtener_version_vigente import ObtenerVersionVigente
from dominio.estado_postulacion import EstadoPostulacion
from dominio.postulacion import Postulacion


class Postularse:
    """Caso de uso CU-01: el estudiante se postula a la práctica (plan de specs/001).

    En orden (ESC-01):
    1. Valida el permiso "postularse" con el Módulo Acceso antes de cualquier otra cosa
       (ADR-008). Si se niega, ValidarPermiso registra la bitácora y lanza PermisoNegado
       (escenario 9).
    2. Revisa que el estudiante no tenga una postulación activa; si la tiene, lanza
       PostulacionActivaExistente sin guardar nada (escenario 4). Una postulación en
       "no cumple requisitos" no es activa (escenario 11).
    3. Obtiene la versión de reglas vigente del programa del ámbito de la sesión
       (ADR-008, ADR-009) y guarda su número en la postulación.
    4. Guarda la postulación en "pendiente de verificación".
    5. Registra el trabajo "verificar en SIA" con el id de la postulación (ADR-005).
    6. Registra el evento de bitácora de la creación, solo con identificadores (ADR-012).
    7. Responde con PostularseSalida.

    No usa ConsultaAcademica: el SIA se consulta después, en el trabajo pendiente, nunca
    mientras el estudiante espera (ADR-004, escenarios 1 y 5). Sin base de datos no hay
    transacción única, así que postulación, trabajo y bitácora se guardan en ese orden (DT-01).
    """

    PERMISO = "postularse"
    TIPO_VERIFICAR_EN_SIA = "verificar en SIA"

    def __init__(
        self,
        *,
        validar_permiso: ValidarPermiso,
        repositorio_postulaciones: RepositorioPostulaciones,
        obtener_version_vigente: ObtenerVersionVigente,
        registrar_trabajo: RegistrarTrabajo,
        registrar_evento: RegistrarEvento,
    ) -> None:
        self._validar_permiso = validar_permiso
        self._repositorio_postulaciones = repositorio_postulaciones
        self._obtener_version_vigente = obtener_version_vigente
        self._registrar_trabajo = registrar_trabajo
        self._registrar_evento = registrar_evento

    def ejecutar(self, entrada: PostularseEntrada) -> PostularseSalida:
        sesion = entrada.sesion
        self._validar_permiso.ejecutar(sesion=sesion, permiso=self.PERMISO, origen=entrada.origen)

        estudiante = sesion.usuario
        programa = sesion.ambito
        if any(p.esta_activa() for p in self._repositorio_postulaciones.listar_por_estudiante(estudiante)):
            raise PostulacionActivaExistente()

        ahora = datetime.now()
        version = self._obtener_version_vigente.ejecutar(programa=programa, fecha=ahora.date())

        postulacion = Postulacion(
            id=str(uuid4()),
            estudiante=estudiante,
            programa=programa,
            empresa=entrada.empresa,
            numero_version_reglas=version.numero,
            fecha=ahora,
        )
        self._repositorio_postulaciones.guardar(postulacion)

        self._registrar_trabajo.ejecutar(
            tipo=self.TIPO_VERIFICAR_EN_SIA,
            referencia=postulacion.id,
            ahora=ahora,
        )

        self._registrar_evento.ejecutar(
            quien=estudiante,
            que=f"postulación creada en '{EstadoPostulacion.PENDIENTE_DE_VERIFICACION.value}'",
            sobre_que=postulacion.id,
            desde_donde=entrada.origen,
        )

        return PostularseSalida(id=postulacion.id, estado=postulacion.estado)
