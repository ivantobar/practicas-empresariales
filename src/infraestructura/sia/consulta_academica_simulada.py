import threading
import time
from collections.abc import Mapping
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import TimeoutError as EsperaAgotada

from aplicacion.reglas.consulta_academica_fallida import ConsultaAcademicaFallida
from dominio.datos_academicos import DatosAcademicos


class ConsultaAcademicaSimulada:
    """Implementa el puerto ConsultaAcademica con un simulador del SIA (ADR-004, plan de specs/001).

    Es el simulador que pide ADR-004 para probar el sistema sin el SIA real (DT-01).
    Se configura con los datos académicos de cada estudiante, una demora en segundos
    y si el SIA responde con error. La demora y el error se pueden cambiar mientras
    corre, para simular un SIA que se cae y luego se recupera (escenario 7).

    Cuenta todas las consultas que recibe, también las que fallan, para mostrar que
    Postularse no consulta el SIA mientras el estudiante espera (escenarios 1 y 4).

    Cada consulta corre en un hilo de concurrent.futures y la espera se corta a los
    espera_maxima_segundos (5 s por defecto, se puede cambiar el valor). El adaptador
    traduce toda falla a ConsultaAcademicaFallida: el corte por tiempo, la respuesta
    con error y un estudiante que el SIA no conoce; ninguna otra falla sale del
    puerto (ADR-004, escenarios 6 y 7). Al cortar no espera a que el hilo termine,
    así que quien llama nunca espera más del máximo.

    El contador y la configuración se protegen con un threading.Lock porque varios
    hilos pueden consultar al mismo tiempo (escenario 5).
    Escenarios 1, 2, 3, 4, 5, 6, 7 y 10 de specs/001.
    """

    def __init__(
        self,
        *,
        datos: Mapping[str, DatosAcademicos] | None = None,
        demora_segundos: float = 0.0,
        responde_con_error: bool = False,
        espera_maxima_segundos: float = 5.0,
    ) -> None:
        if demora_segundos < 0:
            raise ValueError("la demora no puede ser negativa")
        if espera_maxima_segundos <= 0:
            raise ValueError("la espera máxima debe ser mayor que 0")
        self._datos: dict[str, DatosAcademicos] = dict(datos or {})
        self._demora_segundos = demora_segundos
        self._responde_con_error = responde_con_error
        self._espera_maxima_segundos = espera_maxima_segundos
        self._consultas = 0
        self._candado = threading.Lock()

    @property
    def consultas(self) -> int:
        with self._candado:
            return self._consultas

    def configurar_datos(self, estudiante: str, datos: DatosAcademicos) -> None:
        with self._candado:
            self._datos[estudiante] = datos

    def configurar_demora(self, demora_segundos: float) -> None:
        if demora_segundos < 0:
            raise ValueError("la demora no puede ser negativa")
        with self._candado:
            self._demora_segundos = demora_segundos

    def configurar_error(self, responde_con_error: bool) -> None:
        with self._candado:
            self._responde_con_error = responde_con_error

    def consultar(self, estudiante: str) -> DatosAcademicos:
        with self._candado:
            self._consultas += 1
            demora = self._demora_segundos
            responde_con_error = self._responde_con_error
            datos = self._datos.get(estudiante)
            espera_maxima = self._espera_maxima_segundos

        ejecutor = ThreadPoolExecutor(max_workers=1)
        try:
            futuro = ejecutor.submit(self._responder, estudiante, demora, responde_con_error, datos)
            return futuro.result(timeout=espera_maxima)
        except EsperaAgotada:
            raise ConsultaAcademicaFallida(
                f"el SIA no respondió en {espera_maxima} s"
            ) from None
        except ConsultaAcademicaFallida:
            raise
        except Exception as falla:
            raise ConsultaAcademicaFallida(f"el SIA falló: {falla}") from falla
        finally:
            ejecutor.shutdown(wait=False, cancel_futures=True)

    @staticmethod
    def _responder(
        estudiante: str,
        demora: float,
        responde_con_error: bool,
        datos: DatosAcademicos | None,
    ) -> DatosAcademicos:
        if demora:
            time.sleep(demora)
        if responde_con_error:
            raise ConnectionError("el SIA respondió con error")
        if datos is None:
            raise ConsultaAcademicaFallida(f"el SIA no tiene datos del estudiante {estudiante!r}")
        return datos
