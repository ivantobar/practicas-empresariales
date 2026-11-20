"""Composición del sistema: el único archivo que conoce las tres capas (AGENTS.md, ADR-001).

Arma los adaptadores en memoria (DT-01) y el simulador del SIA, los módulos Bitácora,
Acceso, Pendientes, Reglas y Postulación, y los casos de uso. Registra VerificarPostulacion
en el ProcesadorPendientes para el tipo "verificar en SIA", así Pendientes no conoce a
Postulación (vista de usos).

Tiene dos puntos de entrada, como pide ADR-002 ("misma imagen, otro punto de entrada"),
y la ejecución con datos de ejemplo de los escenarios de specs/001 (DP-03 del plan):

    python src/main.py               -> escenarios con datos de ejemplo (por defecto)
    python src/main.py escenarios    -> escenarios con datos de ejemplo
    python src/main.py aplicacion    -> aplicación
    python src/main.py procesador    -> procesador de pendientes, un ciclo cada minuto

Los 11 escenarios imprimen cada verificación con "[cumple]" o "[NO cumple]"; esa salida
es la evidencia de validacion.md. Si alguna verificación falla, el proceso termina con
código 1. Los del flujo de la petición (1, 4, 9 y 11) llaman a Postularse; los del
procesador (2, 3, 6, 7, 8 y 10) llaman a ejecutar_ciclo(ahora) con hora simulada: "ahora"
es la hora de creación del trabajo más los minutos simulados, así 24 h corren en segundos.
Solo el primer intento del escenario 6 espera de verdad los 5 s del corte del SIA. El
escenario 5 lanza 30 postulaciones al mismo tiempo en hilos y mide cada respuesta.

Como no hay base de datos (DT-01), cada punto de entrada tiene su propia memoria: el
procesador solo ve los trabajos que se registran en su mismo proceso.
"""

import sys
import threading
import time
from collections.abc import Iterable
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, fields
from datetime import date, datetime, timedelta

from aplicacion.acceso.permiso_negado import PermisoNegado
from aplicacion.acceso.sesion import Sesion
from aplicacion.acceso.validar_permiso import ValidarPermiso
from aplicacion.bitacora.registrar_evento import RegistrarEvento
from aplicacion.pendientes.estado_trabajo import EstadoTrabajo
from aplicacion.pendientes.procesador_pendientes import ProcesadorPendientes
from aplicacion.pendientes.registrar_trabajo import RegistrarTrabajo
from aplicacion.pendientes.trabajo_pendiente import TrabajoPendiente
from aplicacion.postulacion.postulacion_activa_existente import PostulacionActivaExistente
from aplicacion.postulacion.postularse import Postularse
from aplicacion.postulacion.postularse_entrada import PostularseEntrada
from aplicacion.postulacion.verificar_postulacion import VerificarPostulacion
from aplicacion.reglas.obtener_version_vigente import ObtenerVersionVigente
from aplicacion.reglas.validadores.validador_creditos_aprobados_minimos import (
    ValidadorCreditosAprobadosMinimos,
)
from aplicacion.reglas.validadores.validador_promedio_minimo import ValidadorPromedioMinimo
from aplicacion.reglas.verificar_requisitos import VerificarRequisitos
from dominio.datos_academicos import DatosAcademicos
from dominio.estado_postulacion import EstadoPostulacion
from dominio.evento_bitacora import EventoBitacora
from dominio.requisito import Requisito
from dominio.tipo_requisito import TipoRequisito
from dominio.version_reglas import VersionReglas
from infraestructura.memoria.cola_pendientes_en_memoria import ColaPendientesEnMemoria
from infraestructura.memoria.registro_bitacora_en_memoria import RegistroBitacoraEnMemoria
from infraestructura.memoria.repositorio_postulaciones_en_memoria import (
    RepositorioPostulacionesEnMemoria,
)
from infraestructura.memoria.repositorio_reglas_en_memoria import RepositorioReglasEnMemoria
from infraestructura.sia.consulta_academica_simulada import ConsultaAcademicaSimulada

INTERVALO_PROCESADOR_SEGUNDOS = 60


@dataclass(frozen=True)
class Composicion:
    """Lo que queda armado: adaptadores, casos de uso y el procesador de pendientes."""

    repositorio_postulaciones: RepositorioPostulacionesEnMemoria
    repositorio_reglas: RepositorioReglasEnMemoria
    cola_pendientes: ColaPendientesEnMemoria
    registro_bitacora: RegistroBitacoraEnMemoria
    consulta_academica: ConsultaAcademicaSimulada
    postularse: Postularse
    verificar_postulacion: VerificarPostulacion
    procesador_pendientes: ProcesadorPendientes


def armar(
    *,
    versiones: Iterable[VersionReglas] = (),
    consulta_academica: ConsultaAcademicaSimulada | None = None,
) -> Composicion:
    """Arma el sistema. Las versiones de reglas y el SIA simulado se pueden pasar desde afuera."""
    # Adaptadores de salida (infraestructura/).
    repositorio_postulaciones = RepositorioPostulacionesEnMemoria()
    repositorio_reglas = RepositorioReglasEnMemoria(versiones)
    cola_pendientes = ColaPendientesEnMemoria()
    registro_bitacora = RegistroBitacoraEnMemoria()
    sia = consulta_academica if consulta_academica is not None else ConsultaAcademicaSimulada()

    # Módulo Bitácora.
    registrar_evento = RegistrarEvento(registro_bitacora)

    # Módulo Acceso.
    validar_permiso = ValidarPermiso(registrar_evento)

    # Módulo Pendientes.
    registrar_trabajo = RegistrarTrabajo(cola_pendientes)
    procesador_pendientes = ProcesadorPendientes(cola_pendientes, registrar_trabajo)

    # Módulo Reglas: un validador por cada tipo de requisito (ADR-009).
    obtener_version_vigente = ObtenerVersionVigente(repositorio_reglas)
    verificar_requisitos = VerificarRequisitos(
        consulta_academica=sia,
        repositorio_reglas=repositorio_reglas,
        validadores={
            TipoRequisito.PROMEDIO_MINIMO: ValidadorPromedioMinimo(),
            TipoRequisito.CREDITOS_APROBADOS_MINIMOS: ValidadorCreditosAprobadosMinimos(),
        },
    )

    # Módulo Postulación.
    postularse = Postularse(
        validar_permiso=validar_permiso,
        repositorio_postulaciones=repositorio_postulaciones,
        obtener_version_vigente=obtener_version_vigente,
        registrar_trabajo=registrar_trabajo,
        registrar_evento=registrar_evento,
    )
    verificar_postulacion = VerificarPostulacion(
        repositorio_postulaciones=repositorio_postulaciones,
        verificar_requisitos=verificar_requisitos,
        registrar_evento=registrar_evento,
        registrar_trabajo=registrar_trabajo,
    )

    # Pendientes no conoce a Postulación: main.py registra el manejador (vista de usos).
    procesador_pendientes.registrar_manejador(
        VerificarPostulacion.TIPO_VERIFICAR_EN_SIA, verificar_postulacion
    )

    return Composicion(
        repositorio_postulaciones=repositorio_postulaciones,
        repositorio_reglas=repositorio_reglas,
        cola_pendientes=cola_pendientes,
        registro_bitacora=registro_bitacora,
        consulta_academica=sia,
        postularse=postularse,
        verificar_postulacion=verificar_postulacion,
        procesador_pendientes=procesador_pendientes,
    )


def ejecutar_aplicacion(composicion: Composicion) -> None:
    """Punto de entrada de la aplicación de prácticas.

    Los controladores web no se construyen en esta etapa (DT-04): el caso de uso Postularse
    queda armado y recibe la Sesion ya validada en su DTO de entrada.
    """
    print("Aplicación de prácticas armada: caso de uso Postularse listo (CU-01).")


def ejecutar_procesador(
    composicion: Composicion,
    *,
    intervalo_segundos: float = INTERVALO_PROCESADOR_SEGUNDOS,
    ciclos: int | None = None,
) -> None:
    """Punto de entrada del procesador de pendientes: un ciclo cada minuto (ADR-005).

    Con ciclos=None corre hasta que se detenga el proceso.
    """
    print("Procesador de pendientes iniciado: un ciclo cada minuto (ADR-005).")
    hechos = 0
    while ciclos is None or hechos < ciclos:
        composicion.procesador_pendientes.ejecutar_ciclo(datetime.now())
        hechos += 1
        if ciclos is None or hechos < ciclos:
            time.sleep(intervalo_segundos)


# ---------------------------------------------------------------------------
# Datos de ejemplo de specs/001 (son datos de prueba, no reglas de negocio)
# ---------------------------------------------------------------------------

PROGRAMA_EJEMPLO = "Ingeniería de Sistemas"
ESTUDIANTE_EJEMPLO = "E-1001"
DOCENTE_EJEMPLO = "D-0042"
EMPRESA_EJEMPLO = "Empresa de ejemplo S.A.S."
ORIGEN_EJEMPLO = "portal del estudiante (ejemplo)"
# La spec no da la fecha de vigencia de la versión 3; basta con que ya esté vigente hoy.
VIGENCIA_VERSION_3 = date(2026, 1, 1)


def version_reglas_3() -> VersionReglas:
    """Versión de reglas 3 de "Ingeniería de Sistemas": promedio 3.5 y créditos 130 (antecedentes)."""
    return VersionReglas(
        programa=PROGRAMA_EJEMPLO,
        numero=3,
        fecha_vigencia=VIGENCIA_VERSION_3,
        requisitos=(
            Requisito(TipoRequisito.PROMEDIO_MINIMO, 3.5),
            Requisito(TipoRequisito.CREDITOS_APROBADOS_MINIMOS, 130),
        ),
    )


def armar_con_antecedentes() -> Composicion:
    """Sistema recién armado con los antecedentes de spec.md.

    Versión de reglas 3 vigente y "E-1001" sin postulación activa. El SIA simulado
    conoce a "E-1001" (promedio 3.8, créditos 140) para poder revisar que la bitácora
    no copie esos valores y que la petición no lo consulta.
    """
    sia = ConsultaAcademicaSimulada(
        datos={ESTUDIANTE_EJEMPLO: DatosAcademicos(promedio=3.8, creditos_aprobados=140)}
    )
    return armar(versiones=[version_reglas_3()], consulta_academica=sia)


def sesion_estudiante() -> Sesion:
    return Sesion(usuario=ESTUDIANTE_EJEMPLO, rol="estudiante", ambito=PROGRAMA_EJEMPLO)


def entrada_postulacion(sesion: Sesion) -> PostularseEntrada:
    return PostularseEntrada(sesion=sesion, empresa=EMPRESA_EJEMPLO, origen=ORIGEN_EJEMPLO)


def verificar(resultados: list[bool], descripcion: str, condicion: bool) -> None:
    """Imprime una verificación del escenario y guarda si se cumplió."""
    resultados.append(condicion)
    marca = "[cumple]" if condicion else "[NO cumple]"
    print(f"  {marca} {descripcion}")


def evento_sin_datos_personales(evento: EventoBitacora, valores_personales: Iterable[str]) -> bool:
    """El evento solo tiene quién, qué, sobre qué, cuándo y desde dónde, y ningún valor personal."""
    campos = {campo.name for campo in fields(evento)}
    if campos != {"quien", "que", "sobre_que", "cuando", "desde_donde"}:
        return False
    textos = [str(getattr(evento, campo)) for campo in campos]
    return not any(valor in texto for valor in valores_personales for texto in textos)


# ---------------------------------------------------------------------------
# Escenarios del flujo de la petición (T-41): 1, 4, 9 y 11
# ---------------------------------------------------------------------------


def escenario_1(resultados: list[bool]) -> None:
    print("Escenario 1. El estudiante envía su postulación y recibe la confirmación de recepción")
    sistema = armar_con_antecedentes()

    salida = sistema.postularse.ejecutar(entrada_postulacion(sesion_estudiante()))

    postulaciones = sistema.repositorio_postulaciones.listar_por_estudiante(ESTUDIANTE_EJEMPLO)
    postulacion = postulaciones[0] if len(postulaciones) == 1 else None
    verificar(
        resultados,
        'queda guardada 1 postulación de "E-1001" en "pendiente de verificación"',
        postulacion is not None
        and postulacion.id == salida.id
        and postulacion.estado is EstadoPostulacion.PENDIENTE_DE_VERIFICACION,
    )
    verificar(
        resultados,
        'la postulación queda con la versión de reglas 3 de "Ingeniería de Sistemas"',
        postulacion is not None
        and postulacion.numero_version_reglas == 3
        and postulacion.programa == PROGRAMA_EJEMPLO,
    )
    trabajos = sistema.cola_pendientes.listar()
    verificar(
        resultados,
        'queda registrado 1 trabajo pendiente "verificar en SIA" para esa postulación',
        len(trabajos) == 1
        and trabajos[0].tipo == VerificarPostulacion.TIPO_VERIFICAR_EN_SIA
        and trabajos[0].referencia == salida.id,
    )
    eventos = sistema.registro_bitacora.listar()
    evento = eventos[0] if len(eventos) == 1 else None
    verificar(
        resultados,
        "queda 1 evento de bitácora con quién, qué, sobre qué, cuándo y desde dónde",
        evento is not None
        and evento.quien == ESTUDIANTE_EJEMPLO
        and evento.que == "postulación creada en 'pendiente de verificación'"
        and evento.sobre_que == salida.id
        and evento.cuando is not None
        and evento.desde_donde == ORIGEN_EJEMPLO,
    )
    verificar(
        resultados,
        "el evento no contiene nombre, documento, promedio ni créditos (solo identificadores)",
        evento is not None and evento_sin_datos_personales(evento, ("3.8", "140")),
    )
    verificar(
        resultados,
        'el estudiante recibe "postulación recibida, te avisamos el resultado"',
        salida.mensaje == "postulación recibida, te avisamos el resultado"
        and salida.estado is EstadoPostulacion.PENDIENTE_DE_VERIFICACION,
    )
    verificar(
        resultados,
        f"el sistema no consultó el SIA antes de confirmar (consultas: {sistema.consulta_academica.consultas})",
        sistema.consulta_academica.consultas == 0,
    )


def escenario_4(resultados: list[bool]) -> None:
    print("Escenario 4. El estudiante ya tiene una postulación activa")
    sistema = armar_con_antecedentes()
    # Dado: "E-1001" tiene una postulación en "pendiente de verificación".
    sistema.postularse.ejecutar(entrada_postulacion(sesion_estudiante()))
    trabajos_antes = len(sistema.cola_pendientes.listar())

    mensaje = None
    try:
        sistema.postularse.ejecutar(entrada_postulacion(sesion_estudiante()))
    except PostulacionActivaExistente as rechazo:
        mensaje = str(rechazo)

    verificar(
        resultados,
        f'el sistema rechaza con "ya tienes una postulación en curso" (mensaje: {mensaje!r})',
        mensaje == "ya tienes una postulación en curso",
    )
    postulaciones = sistema.repositorio_postulaciones.listar_por_estudiante(ESTUDIANTE_EJEMPLO)
    verificar(
        resultados,
        f'"E-1001" sigue teniendo exactamente 1 postulación (tiene {len(postulaciones)})',
        len(postulaciones) == 1,
    )
    trabajos_despues = len(sistema.cola_pendientes.listar())
    verificar(
        resultados,
        f"no queda registrado ningún trabajo pendiente nuevo ({trabajos_antes} antes, {trabajos_despues} después)",
        trabajos_despues == trabajos_antes,
    )
    verificar(
        resultados,
        f"no se consultó el SIA (consultas: {sistema.consulta_academica.consultas})",
        sistema.consulta_academica.consultas == 0,
    )


def escenario_9(resultados: list[bool]) -> None:
    print("Escenario 9. Un usuario sin rol de estudiante intenta postularse")
    sistema = armar_con_antecedentes()
    # La spec no da el ámbito de "D-0042"; se usa el programa de ejemplo.
    sesion_docente = Sesion(usuario=DOCENTE_EJEMPLO, rol="docente asesor", ambito=PROGRAMA_EJEMPLO)

    negado = False
    try:
        sistema.postularse.ejecutar(entrada_postulacion(sesion_docente))
    except PermisoNegado:
        negado = True

    verificar(resultados, "el sistema niega la operación por falta de permiso", negado)
    verificar(
        resultados,
        "no queda guardada ninguna postulación",
        len(sistema.repositorio_postulaciones.listar_por_estudiante(DOCENTE_EJEMPLO)) == 0
        and len(sistema.repositorio_postulaciones.listar_por_estudiante(ESTUDIANTE_EJEMPLO)) == 0,
    )
    verificar(
        resultados,
        "no queda registrado ningún trabajo pendiente",
        len(sistema.cola_pendientes.listar()) == 0,
    )
    eventos = sistema.registro_bitacora.listar()
    evento = eventos[0] if len(eventos) == 1 else None
    verificar(
        resultados,
        'queda 1 evento de permiso negado con quién ("D-0042"), qué (postularse), cuándo y desde dónde',
        evento is not None
        and evento.quien == DOCENTE_EJEMPLO
        and evento.que == "permiso negado: postularse"
        and evento.cuando is not None
        and evento.desde_donde == ORIGEN_EJEMPLO,
    )


def escenario_11(resultados: list[bool]) -> None:
    print("Escenario 11. El estudiante puede volver a postularse si la anterior no cumplió requisitos")
    sistema = armar_con_antecedentes()
    # Dado: "E-1001" tiene una postulación en "no cumple requisitos". Se prepara directo en
    # el repositorio; el paso por el procesador de pendientes es el escenario 3 (T-42).
    anterior_id = sistema.postularse.ejecutar(entrada_postulacion(sesion_estudiante())).id
    anterior = sistema.repositorio_postulaciones.buscar_por_id(anterior_id)
    anterior.marcar_no_cumple_requisitos((Requisito(TipoRequisito.PROMEDIO_MINIMO, 3.5),))
    sistema.repositorio_postulaciones.actualizar(anterior)
    verificar(
        resultados,
        "antes de postularse no tiene ninguna postulación activa",
        not any(
            p.esta_activa()
            for p in sistema.repositorio_postulaciones.listar_por_estudiante(ESTUDIANTE_EJEMPLO)
        ),
    )

    salida = sistema.postularse.ejecutar(entrada_postulacion(sesion_estudiante()))

    nueva = sistema.repositorio_postulaciones.buscar_por_id(salida.id)
    verificar(
        resultados,
        'queda guardada una postulación nueva en "pendiente de verificación" con la versión vigente (3)',
        nueva is not None
        and nueva.id != anterior_id
        and nueva.estado is EstadoPostulacion.PENDIENTE_DE_VERIFICACION
        and nueva.numero_version_reglas == 3,
    )
    anterior = sistema.repositorio_postulaciones.buscar_por_id(anterior_id)
    verificar(
        resultados,
        'la postulación anterior sigue en "no cumple requisitos"',
        anterior is not None and anterior.estado is EstadoPostulacion.NO_CUMPLE_REQUISITOS,
    )


# ---------------------------------------------------------------------------
# Escenarios del procesador con hora simulada (T-42): 2, 3, 6, 7, 8 y 10, y el 5
# ---------------------------------------------------------------------------


def trabajos_de(sistema: Composicion, tipo: str, referencia: str) -> list[TrabajoPendiente]:
    return [t for t in sistema.cola_pendientes.listar() if t.tipo == tipo and t.referencia == referencia]


def postular_ejemplo(sistema: Composicion) -> tuple[str, TrabajoPendiente]:
    """Dado: la postulación de "E-1001" en "pendiente de verificación" y su trabajo "verificar en SIA"."""
    postulacion_id = sistema.postularse.ejecutar(entrada_postulacion(sesion_estudiante())).id
    (trabajo,) = trabajos_de(sistema, VerificarPostulacion.TIPO_VERIFICAR_EN_SIA, postulacion_id)
    return postulacion_id, trabajo


def trabajo_actual(sistema: Composicion, trabajo_id: str) -> TrabajoPendiente:
    (trabajo,) = [t for t in sistema.cola_pendientes.listar() if t.id == trabajo_id]
    return trabajo


def estado_de(sistema: Composicion, postulacion_id: str) -> EstadoPostulacion | None:
    postulacion = sistema.repositorio_postulaciones.buscar_por_id(postulacion_id)
    return postulacion.estado if postulacion is not None else None


def escenario_2(resultados: list[bool]) -> None:
    print("Escenario 2. El SIA responde y el estudiante cumple los requisitos")
    sistema = armar_con_antecedentes()  # El SIA devuelve para "E-1001" promedio 3.8 y créditos 140.
    postulacion_id, trabajo = postular_ejemplo(sistema)

    inicio = time.perf_counter()
    sistema.procesador_pendientes.ejecutar_ciclo(trabajo.creado_en)
    duracion = time.perf_counter() - inicio

    verificar(
        resultados,
        f"el SIA responde en menos de 5 segundos (ciclo de {duracion:.3f} s)",
        sistema.consulta_academica.consultas == 1 and duracion < 5,
    )
    verificar(
        resultados,
        'la postulación pasa a "verificada"',
        estado_de(sistema, postulacion_id) is EstadoPostulacion.VERIFICADA,
    )
    eventos = sistema.registro_bitacora.listar()
    verificar(
        resultados,
        'queda un evento de bitácora del cambio de "pendiente de verificación" a "verificada"',
        any(
            e.sobre_que == postulacion_id
            and e.que == "cambio de 'pendiente de verificación' a 'verificada'"
            for e in eventos
        ),
    )
    verificar(
        resultados,
        'queda registrado un trabajo pendiente para avisar el resultado a "E-1001"',
        len(trabajos_de(sistema, VerificarPostulacion.TIPO_AVISAR_AL_ESTUDIANTE, postulacion_id)) == 1,
    )
    consultas_antes = sistema.consulta_academica.consultas
    sistema.procesador_pendientes.ejecutar_ciclo(trabajo.creado_en + timedelta(minutes=30))
    verificar(
        resultados,
        'el trabajo "verificar en SIA" queda terminado y no se vuelve a ejecutar '
        f"(consultas al SIA: {consultas_antes} antes y {sistema.consulta_academica.consultas} "
        "después de otro ciclo)",
        trabajo_actual(sistema, trabajo.id).estado is EstadoTrabajo.TERMINADO
        and sistema.consulta_academica.consultas == consultas_antes,
    )


def escenario_3(resultados: list[bool]) -> None:
    print("Escenario 3. El SIA responde y el estudiante no cumple los requisitos")
    sistema = armar_con_antecedentes()
    sistema.consulta_academica.configurar_datos(
        ESTUDIANTE_EJEMPLO, DatosAcademicos(promedio=3.2, creditos_aprobados=140)
    )
    postulacion_id, trabajo = postular_ejemplo(sistema)

    inicio = time.perf_counter()
    sistema.procesador_pendientes.ejecutar_ciclo(trabajo.creado_en)
    duracion = time.perf_counter() - inicio

    verificar(
        resultados,
        f"el SIA responde en menos de 5 segundos (ciclo de {duracion:.3f} s)",
        sistema.consulta_academica.consultas == 1 and duracion < 5,
    )
    postulacion = sistema.repositorio_postulaciones.buscar_por_id(postulacion_id)
    verificar(
        resultados,
        'la postulación pasa a "no cumple requisitos"',
        postulacion is not None and postulacion.estado is EstadoPostulacion.NO_CUMPLE_REQUISITOS,
    )
    incumplidos = postulacion.requisitos_incumplidos if postulacion is not None else ()
    verificar(
        resultados,
        'el resultado indica que no se cumplió "promedio mínimo" (exigido 3.5)',
        Requisito(TipoRequisito.PROMEDIO_MINIMO, 3.5) in incumplidos,
    )
    verificar(
        resultados,
        'el resultado no marca como incumplido "créditos aprobados mínimos"',
        all(r.tipo is not TipoRequisito.CREDITOS_APROBADOS_MINIMOS for r in incumplidos),
    )
    verificar(
        resultados,
        'queda un evento de bitácora del cambio de "pendiente de verificación" a "no cumple requisitos"',
        any(
            e.sobre_que == postulacion_id
            and e.que == "cambio de 'pendiente de verificación' a 'no cumple requisitos'"
            for e in sistema.registro_bitacora.listar()
        ),
    )
    verificar(
        resultados,
        'queda registrado un trabajo pendiente para avisar el resultado a "E-1001"',
        len(trabajos_de(sistema, VerificarPostulacion.TIPO_AVISAR_AL_ESTUDIANTE, postulacion_id)) == 1,
    )


ESTUDIANTES_PICO = 30
LIMITE_CONFIRMACION_SEGUNDOS = 3


def escenario_5(resultados: list[bool]) -> None:
    print("Escenario 5. EAC-02: confirmación en menos de 3 segundos con el SIA caído en el pico")
    # El SIA no responde: si alguien lo consultara, esperaría hasta el corte de 5 s.
    sia = ConsultaAcademicaSimulada(demora_segundos=60)
    sistema = armar(versiones=[version_reglas_3()], consulta_academica=sia)
    estudiantes = [f"E-{2001 + i}" for i in range(ESTUDIANTES_PICO)]
    salida_al_mismo_tiempo = threading.Barrier(ESTUDIANTES_PICO)

    def postular(estudiante: str) -> tuple[str, str, float]:
        sesion = Sesion(usuario=estudiante, rol="estudiante", ambito=PROGRAMA_EJEMPLO)
        salida_al_mismo_tiempo.wait()
        inicio = time.perf_counter()
        salida = sistema.postularse.ejecutar(entrada_postulacion(sesion))
        return salida.id, salida.mensaje, time.perf_counter() - inicio

    with ThreadPoolExecutor(max_workers=ESTUDIANTES_PICO) as ejecutor:
        respuestas = list(ejecutor.map(postular, estudiantes))

    guardadas = [
        p
        for estudiante in estudiantes
        for p in sistema.repositorio_postulaciones.listar_por_estudiante(estudiante)
    ]
    verificar(
        resultados,
        f'quedan guardadas 30 postulaciones en "pendiente de verificación" (hay {len(guardadas)})',
        len(guardadas) == ESTUDIANTES_PICO
        and all(p.estado is EstadoPostulacion.PENDIENTE_DE_VERIFICACION for p in guardadas),
    )
    ids = {id for id, _, _ in respuestas}
    trabajos = [
        t for t in sistema.cola_pendientes.listar()
        if t.tipo == VerificarPostulacion.TIPO_VERIFICAR_EN_SIA and t.referencia in ids
    ]
    verificar(
        resultados,
        f'quedan registrados 30 trabajos pendientes "verificar en SIA" (hay {len(trabajos)})',
        len(trabajos) == ESTUDIANTES_PICO,
    )
    a_tiempo = [
        d for _, mensaje, d in respuestas
        if mensaje == "postulación recibida, te avisamos el resultado" and d < LIMITE_CONFIRMACION_SEGUNDOS
    ]
    porcentaje = 100 * len(a_tiempo) / ESTUDIANTES_PICO
    mas_lenta = max(d for _, _, d in respuestas)
    verificar(
        resultados,
        f"al menos 95% recibe la confirmación en menos de 3 s ({porcentaje:.0f}%, "
        f"la más lenta en {mas_lenta:.3f} s; consultas al SIA: {sia.consultas})",
        porcentaje >= 95,
    )
    perdidas = [id for id in ids if sistema.repositorio_postulaciones.buscar_por_id(id) is None]
    verificar(
        resultados,
        f"0 postulaciones se pierden ({len(perdidas)} perdidas, {len(ids)} ids distintos)",
        not perdidas and len(ids) == ESTUDIANTES_PICO,
    )


def escenario_6(resultados: list[bool]) -> None:
    print("Escenario 6. EAC-02: el SIA no responde en 5 segundos durante la verificación")
    sistema = armar_con_antecedentes()
    sistema.consulta_academica.configurar_demora(6)  # Tarda más de 5 s.
    postulacion_id, trabajo = postular_ejemplo(sistema)
    creado_en = trabajo.creado_en

    inicio = time.perf_counter()
    sistema.procesador_pendientes.ejecutar_ciclo(creado_en)
    duracion = time.perf_counter() - inicio

    verificar(
        resultados,
        f"la espera por el SIA se corta a los 5 segundos (el ciclo duró {duracion:.3f} s)",
        # Tolerancia de 0.5 s a cada lado: el reloj del corte y el de la medición no coinciden exacto.
        4.5 <= duracion < 5.5,
    )
    verificar(
        resultados,
        'la postulación sigue en "pendiente de verificación"',
        estado_de(sistema, postulacion_id) is EstadoPostulacion.PENDIENTE_DE_VERIFICACION,
    )
    despues = trabajo_actual(sistema, trabajo.id)
    verificar(
        resultados,
        "el trabajo queda reprogramado para dentro de 1 minuto",
        despues.estado is EstadoTrabajo.PENDIENTE
        and despues.proximo_intento == creado_en + timedelta(minutes=1),
    )

    # Los siguientes intentos también fallan: para no esperar 5 s reales en cada uno,
    # el SIA simulado responde con error, que también es ConsultaAcademicaFallida.
    sistema.consulta_academica.configurar_demora(0)
    sistema.consulta_academica.configurar_error(True)
    minutos_de_intento = [0]
    intentos = despues.intentos_fallidos
    for minuto in range(1, 61):  # Un ciclo por minuto simulado durante 1 h.
        sistema.procesador_pendientes.ejecutar_ciclo(creado_en + timedelta(minutes=minuto))
        actual = trabajo_actual(sistema, trabajo.id)
        if actual.intentos_fallidos > intentos:
            intentos = actual.intentos_fallidos
            minutos_de_intento.append(minuto)
    esperas = [b - a for a, b in zip(minutos_de_intento, minutos_de_intento[1:])]
    verificar(
        resultados,
        f"los siguientes intentos se reprograman a 1, 2, 4, 8, 15, 15, ... minutos (esperas: {esperas})",
        esperas == [1, 2, 4, 8, 15, 15, 15],
    )
    verificar(
        resultados,
        f"ninguna espera entre intentos es mayor de 15 minutos (máxima: {max(esperas)})",
        max(esperas) <= 15,
    )


def escenario_7(resultados: list[bool]) -> None:
    print("Escenario 7. EAC-02: el SIA responde con error y luego se recupera")
    sistema = armar_con_antecedentes()  # Al recuperarse devuelve promedio 3.8 y créditos 140.
    sistema.consulta_academica.configurar_error(True)
    postulacion_id, trabajo = postular_ejemplo(sistema)
    creado_en = trabajo.creado_en

    siempre_guardada = True
    minutos_con_error = 3 * 60
    for minuto in range(0, minutos_con_error + 1):  # 3 h con error, un ciclo por minuto.
        sistema.procesador_pendientes.ejecutar_ciclo(creado_en + timedelta(minutes=minuto))
        siempre_guardada = siempre_guardada and (
            estado_de(sistema, postulacion_id) is EstadoPostulacion.PENDIENTE_DE_VERIFICACION
        )
    intentos_con_error = trabajo_actual(sistema, trabajo.id).intentos_fallidos

    # El SIA se recupera justo después del intento del minuto 180.
    sistema.consulta_academica.configurar_error(False)
    minutos_hasta_verificar = None
    for minuto in range(1, 61):
        sistema.procesador_pendientes.ejecutar_ciclo(
            creado_en + timedelta(minutes=minutos_con_error + minuto)
        )
        if estado_de(sistema, postulacion_id) is EstadoPostulacion.VERIFICADA:
            minutos_hasta_verificar = minuto
            break

    verificar(
        resultados,
        'la postulación pasa a "verificada" en máximo 30 minutos desde que el SIA se recuperó '
        f"(a los {minutos_hasta_verificar} min)",
        minutos_hasta_verificar is not None and minutos_hasta_verificar <= 30,
    )
    verificar(
        resultados,
        'durante las 3 horas la postulación nunca dejó de estar guardada en "pendiente de verificación" '
        f"({intentos_con_error} intentos con error)",
        siempre_guardada and intentos_con_error > 0,
    )
    verificar(
        resultados,
        "0 postulaciones se pierden",
        len(sistema.repositorio_postulaciones.listar_por_estudiante(ESTUDIANTE_EJEMPLO)) == 1,
    )


def escenario_8(resultados: list[bool]) -> None:
    print("Escenario 8. EAC-02: la verificación no se logra en 24 horas")
    sistema = armar_con_antecedentes()
    sistema.consulta_academica.configurar_error(True)
    postulacion_id, trabajo = postular_ejemplo(sistema)
    creado_en = trabajo.creado_en
    minutos_24_horas = 24 * 60

    for minuto in range(0, minutos_24_horas):  # Lleva 24 h fallando, un ciclo por minuto.
        sistema.procesador_pendientes.ejecutar_ciclo(creado_en + timedelta(minutes=minuto))
    antes = trabajo_actual(sistema, trabajo.id)
    verificar(
        resultados,
        f'antes de las 24 h el trabajo sigue "pendiente" ({antes.intentos_fallidos} intentos fallidos)',
        antes.estado is EstadoTrabajo.PENDIENTE,
    )

    # Siguiente ciclo del procesador, a las 24 h.
    sistema.procesador_pendientes.ejecutar_ciclo(creado_en + timedelta(minutes=minutos_24_horas))
    consultas_al_fallar = sistema.consulta_academica.consultas
    for minuto in range(1, 61):  # Una hora más de ciclos.
        sistema.procesador_pendientes.ejecutar_ciclo(
            creado_en + timedelta(minutes=minutos_24_horas + minuto)
        )
    verificar(
        resultados,
        'el trabajo "verificar en SIA" queda "fallido" y no se vuelve a intentar '
        f"(consultas al SIA: {consultas_al_fallar} al fallar y {sistema.consulta_academica.consultas} "
        "una hora después)",
        trabajo_actual(sistema, trabajo.id).estado is EstadoTrabajo.FALLIDO
        and sistema.consulta_academica.consultas == consultas_al_fallar,
    )
    verificar(
        resultados,
        "queda registrado un trabajo pendiente para avisar al administrador del sistema",
        len(trabajos_de(sistema, ProcesadorPendientes.TIPO_AVISAR_AL_ADMINISTRADOR, trabajo.id)) == 1,
    )
    verificar(
        resultados,
        'la postulación sigue guardada en "pendiente de verificación"',
        estado_de(sistema, postulacion_id) is EstadoPostulacion.PENDIENTE_DE_VERIFICACION,
    )


def escenario_10(resultados: list[bool]) -> None:
    print("Escenario 10. EAC-01: la postulación se verifica con la versión de reglas con la que se hizo")
    # La versión 4 (promedio mínimo 4.0) entra en vigencia mañana, después de postularse.
    vigencia_version_4 = date.today() + timedelta(days=1)
    version_4 = VersionReglas(
        programa=PROGRAMA_EJEMPLO,
        numero=4,
        fecha_vigencia=vigencia_version_4,
        requisitos=(Requisito(TipoRequisito.PROMEDIO_MINIMO, 4.0),),
    )
    sia = ConsultaAcademicaSimulada(
        datos={ESTUDIANTE_EJEMPLO: DatosAcademicos(promedio=3.8, creditos_aprobados=140)}
    )
    sistema = armar(versiones=[version_reglas_3(), version_4], consulta_academica=sia)
    postulacion_id, trabajo = postular_ejemplo(sistema)

    # El trabajo se ejecuta con hora simulada del día en que ya rige la versión 4.
    ahora = datetime.combine(vigencia_version_4, trabajo.creado_en.time())
    vigente = ObtenerVersionVigente(sistema.repositorio_reglas).ejecutar(
        programa=PROGRAMA_EJEMPLO, fecha=ahora.date()
    )
    verificar(
        resultados,
        f"al ejecutar el trabajo ya rige la versión 4 (vigente el {ahora.date().isoformat()}: {vigente.numero})",
        vigente.numero == 4,
    )
    sistema.procesador_pendientes.ejecutar_ciclo(ahora)

    postulacion = sistema.repositorio_postulaciones.buscar_por_id(postulacion_id)
    verificar(
        resultados,
        'la postulación se verifica contra la versión 3 y pasa a "verificada" '
        "(con la versión 4 no cumpliría: 3.8 < 4.0)",
        postulacion is not None and postulacion.estado is EstadoPostulacion.VERIFICADA,
    )
    verificar(
        resultados,
        "la postulación sigue con la versión de reglas 3",
        postulacion is not None and postulacion.numero_version_reglas == 3,
    )


def ejecutar_escenarios() -> bool:
    """Ejecuta los 11 escenarios con datos de ejemplo; devuelve True si todos se cumplen."""
    resultados: list[bool] = []
    print("specs/001-postularse: escenarios con datos de ejemplo")
    print("  flujo de la petición: 1, 4, 9 y 11; procesador con hora simulada: 2, 3, 6, 7, 8 y 10;")
    print("  30 estudiantes a la vez: 5")
    escenarios = (
        escenario_1, escenario_2, escenario_3,escenario_4, escenario_5,escenario_6, escenario_7, escenario_8,  escenario_9, escenario_10,
        escenario_11,
    )
    for escenario in escenarios:
        print()
        escenario(resultados)
    cumplidas = sum(resultados)
    print()
    print(f"Verificaciones cumplidas: {cumplidas} de {len(resultados)}")
    return cumplidas == len(resultados)


def main(argumentos: list[str]) -> int:
    punto_de_entrada = argumentos[0] if argumentos else "escenarios"
    if punto_de_entrada == "escenarios":
        return 0 if ejecutar_escenarios() else 1
    if punto_de_entrada == "aplicacion":
        ejecutar_aplicacion(armar())
        return 0
    if punto_de_entrada == "procesador":
        try:
            ejecutar_procesador(armar())
        except KeyboardInterrupt:
            print("Procesador de pendientes detenido.")
        return 0
    print(f"punto de entrada desconocido: {punto_de_entrada!r} (use escenarios, aplicacion o procesador)")
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
