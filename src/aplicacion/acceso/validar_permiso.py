from types import MappingProxyType

from aplicacion.acceso.permiso_negado import PermisoNegado
from aplicacion.acceso.sesion import Sesion
from aplicacion.bitacora.registrar_evento import RegistrarEvento


class ValidarPermiso:
    """Valida que el rol de la sesión tenga el permiso que pide el caso de uso (ADR-008).

    Tiene la tabla de permisos por rol; en specs/001 solo existe "postularse",
    que tiene únicamente el rol "estudiante". Si el rol no tiene el permiso,
    registra en la bitácora un evento de permiso negado (ADR-012) y lanza
    PermisoNegado. El evento guarda quién, qué, cuándo y desde dónde, sin
    "sobre qué" porque la operación no llegó a hacerse. Escenario 9 de specs/001.
    """

    _PERMISOS_POR_ROL = MappingProxyType(
        {
            "estudiante": frozenset({"postularse"}),
        }
    )

    def __init__(self, registrar_evento: RegistrarEvento) -> None:
        self._registrar_evento = registrar_evento

    def ejecutar(self, *, sesion: Sesion, permiso: str, origen: str) -> None:
        permisos_del_rol = self._PERMISOS_POR_ROL.get(sesion.rol, frozenset())
        if permiso in permisos_del_rol:
            return
        self._registrar_evento.ejecutar(
            quien=sesion.usuario,
            que=f"permiso negado: {permiso}",
            desde_donde=origen,
        )
        raise PermisoNegado(
            f"el rol {sesion.rol!r} no tiene el permiso {permiso!r}"
        )
