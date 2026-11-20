from typing import Protocol

from aplicacion.pendientes.trabajo_pendiente import TrabajoPendiente


class ManejadorTrabajo(Protocol):
    """La interfaz que implementa cada módulo para ejecutar un tipo de trabajo (glosario).

    La define el Módulo Pendientes y la implementan los módulos de negocio, por ejemplo
    VerificarPostulacion para el tipo "verificar en SIA". main.py registra cada manejador
    con su tipo, así Pendientes no conoce a ningún módulo de negocio (vista de desarrollo,
    vista de usos). No es un puerto hacia infraestructura, por eso no va en puertos/.
    """

    def ejecutar(self, trabajo: TrabajoPendiente) -> None:
        """Hace el trabajo. Si termina sin lanzar error, el trabajo se marca "terminado".

        Si la llamada externa falla, lanza FallaReintentable y el ProcesadorPendientes
        reprograma el trabajo, o lo marca "fallido" si ya tiene 24 h (ADR-005).
        """
        ...
