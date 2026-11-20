# Validación: 001 Postularse

Evidencia: salida de `python src/main.py` (punto de entrada por defecto, "escenarios"), ejecutado el 2026-11-20 desde la raíz del repositorio. Terminó con código 0 y la última línea fue `Verificaciones cumplidas: 48 de 48`. Cada escenario de `spec.md` es una función `escenario_N` de [src/main.py](../../src/main.py), que arma el sistema desde cero con `armar_con_antecedentes()` o `armar()` y revisa el estado real de los adaptadores en memoria: repositorio, cola, bitácora y contador de consultas del SIA simulado. No revisa valores fijos.

## Validación funcional

| Escenario | Resultado | Evidencia |
|-----------|-----------|-----------|
| 1. El estudiante envía su postulación y recibe la confirmación de recepción | Cumple | `escenario_1` (main.py:247), 7 de 7 verificaciones. `Postularse.ejecutar` guarda la `Postulacion` en "pendiente de verificación" con `numero_version_reglas == 3`, registra 1 `TrabajoPendiente` "verificar en SIA" con la referencia al id y 1 `EventoBitacora` con quién, qué, sobre qué, cuándo y desde dónde. `evento_sin_datos_personales` revisa que el evento tenga solo esos 5 campos y que no contenga "3.8" ni "140". El mensaje de `PostularseSalida` es "postulación recibida, te avisamos el resultado" y la salida muestra "consultas: 0" en `ConsultaAcademicaSimulada.consultas`. |
| 2. El SIA responde y el estudiante cumple los requisitos | Cumple | `escenario_2` (main.py:444), 5 de 5 verificaciones. `ProcesadorPendientes.ejecutar_ciclo` → `VerificarPostulacion` → `VerificarRequisitos`. El ciclo dura 0.001 s con 1 consulta, el estado pasa a "verificada", queda el evento "cambio de 'pendiente de verificación' a 'verificada'" y 1 trabajo "avisar al estudiante". En otro ciclo, 30 min después, el trabajo sigue `TERMINADO` y las consultas siguen en 1. |
| 3. El SIA responde y el estudiante no cumple los requisitos | Cumple | `escenario_3` (main.py:490), 6 de 6 verificaciones. Con promedio 3.2, la postulación pasa a "no cumple requisitos" y `requisitos_incumplidos` contiene `Requisito(PROMEDIO_MINIMO, 3.5)` sin ningún requisito de créditos. Queda el evento del cambio y 1 trabajo "avisar al estudiante". |
| 4. El estudiante ya tiene una postulación activa | Cumple | `escenario_4` (main.py:307), 4 de 4 verificaciones. La segunda llamada lanza `PostulacionActivaExistente` con el mensaje "ya tienes una postulación en curso". Sigue habiendo 1 postulación, los trabajos quedan en 1 antes y 1 después, y hay 0 consultas al SIA. El control lo hace `Postulacion.esta_activa()` en `Postularse.ejecutar`. |
| 5. EAC-02: confirmación en menos de 3 segundos con el SIA caído en el pico de inicio de periodo | Cumple | `escenario_5` (main.py:544), 4 de 4 verificaciones. Se lanzan 30 hilos sincronizados con `threading.Barrier` y el SIA tiene una demora de 60 s. Quedan 30 postulaciones "pendiente de verificación" y 30 trabajos "verificar en SIA". El 100 % recibe la confirmación en menos de 3 s (la más lenta tarda 0.000 s) y el SIA recibe 0 consultas. Hay 30 ids distintos y 0 perdidos. La concurrencia es segura por el `threading.Lock` de los adaptadores en memoria. |
| 6. EAC-02: el SIA no responde en 5 segundos durante la verificación | Cumple | `escenario_6` (main.py:603), 5 de 5 verificaciones. Con el SIA a 6 s, el ciclo dura 5.003 s porque `ConsultaAcademicaSimulada` corta con `future.result(timeout=5)` y lanza `ConsultaAcademicaFallida`, que `VerificarPostulacion` convierte en `FallaReintentable`. La postulación sigue "pendiente de verificación" y `proximo_intento` queda en `creado_en + 1 min`. En 60 minutos simulados las esperas medidas son `[1, 2, 4, 8, 15, 15, 15]`, con un máximo de 15 (`TrabajoPendiente.siguiente_espera`). |
| 7. EAC-02: el SIA responde con error y luego se recupera | Cumple | `escenario_7` (main.py:658), 3 de 3 verificaciones. Se simulan 180 min de error con un ciclo por minuto: hay 16 intentos fallidos y la postulación sigue siempre en "pendiente de verificación". Después de la recuperación pasa a "verificada" a los 15 min, por debajo del máximo de 30, y el estudiante sigue teniendo 1 postulación. |
| 8. EAC-02: la verificación no se logra en 24 horas | Cumple | `escenario_8` (main.py:704), 4 de 4 verificaciones. Antes de las 24 h el trabajo sigue "pendiente" con 99 intentos fallidos. En el ciclo de las 24 h, `TrabajoPendiente.cumplio_24_horas` marca el trabajo `FALLIDO` y `ProcesadorPendientes` registra 1 trabajo "avisar al administrador" con el id del trabajo. Una hora después las consultas siguen en 100, o sea que no se reintenta, y la postulación sigue "pendiente de verificación". |
| 9. Un usuario sin rol de estudiante intenta postularse | Cumple | `escenario_9` (main.py:344), 4 de 4 verificaciones. `ValidarPermiso` lanza `PermisoNegado` para el rol "docente asesor" antes de cualquier otra cosa. Quedan 0 postulaciones y 0 trabajos, y 1 `EventoBitacora` con quién "D-0042", qué "permiso negado: postularse", cuándo y desde dónde. Observación: la spec no da el ámbito de "D-0042" y `main.py` usa el programa de ejemplo. El resultado no depende de eso, porque el permiso se valida por rol. |
| 10. EAC-01: la postulación se verifica con la versión de reglas con la que se hizo | Cumple | `escenario_10` (main.py:748), 3 de 3 verificaciones. La versión 4 (promedio 4.0) entra en vigencia al día siguiente y el ciclo se ejecuta con esa fecha simulada; `ObtenerVersionVigente` confirma que la vigente es la 4. Aun así, la postulación pasa a "verificada" con promedio 3.8, que no alcanzaría el 4.0 de la versión 4, porque `VerificarPostulacion` pasa `postulacion.numero_version_reglas` (3) a `VerificarRequisitos`. La postulación sigue con la versión 3. |
| 11. El estudiante puede volver a postularse si la anterior no cumplió requisitos | Cumple | `escenario_11` (main.py:381), 3 de 3 verificaciones. La postulación anterior se pasa a "no cumple requisitos" con `marcar_no_cumple_requisitos` y `esta_activa()` devuelve False. La postulación nueva tiene otro id, está en "pendiente de verificación" con la versión 3 y la anterior sigue en "no cumple requisitos". |

Resultado: 11 de 11 escenarios cumplen (48 de 48 verificaciones). No hay ningún "No cumple".

## Validación arquitectónica

- **Regla de dependencia (R-07): cumple.** Revisé todos los imports de `src/`:
  - `dominio/` solo importa `dominio.*` y la librería estándar (`dataclasses`, `datetime` y `enum`).
  - `aplicacion/` no importa nada de `infraestructura/`.
  - `infraestructura/` importa solo `dominio.*` y `aplicacion.*` (puertos, errores y `TrabajoPendiente` y `EstadoTrabajo`, que usa la cola en memoria).
  - `main.py` es el único archivo que importa las tres capas.
  - Vista de usos entre módulos:
    - Postulación usa Acceso (`ValidarPermiso`), Bitácora (`RegistrarEvento`), Pendientes (`RegistrarTrabajo`, `FallaReintentable` y `TrabajoPendiente`) y Reglas (`ObtenerVersionVigente`, `VerificarRequisitos` y `ConsultaAcademicaFallida`). Todo está permitido.
    - Acceso usa solo Bitácora, que está permitido.
    - Reglas no usa ningún otro módulo. Está permitido, porque la vista le permite Bitácora y no la necesita en esta funcionalidad.
    - Pendientes y Bitácora no importan ningún otro módulo.
    - Pendientes no conoce a Postulación: `main.py:135` registra `VerificarPostulacion` con `registrar_manejador`.
- **ADR citados en plan.md:**
  - ADR-001: el código está en las capas `dominio/`, `aplicacion/` e `infraestructura/`, y `aplicacion/` está dividida en `acceso/`, `bitacora/`, `pendientes/`, `postulacion/` y `reglas/`. Los puertos están en `aplicacion/<modulo>/puertos/`. La composición está en `main.py:85` (`armar`).
  - ADR-003: no hay base de datos. Hay 4 adaptadores en `infraestructura/memoria/` detrás de los puertos `RepositorioPostulaciones`, `RepositorioReglas`, `ColaPendientes` y `RegistroBitacora` (DT-01).
  - ADR-004: `Postularse` no recibe `ConsultaAcademica` en su constructor (`postularse.py`), así que no puede consultar el SIA mientras el estudiante espera (escenarios 1, 4 y 5: 0 consultas). `ConsultaAcademicaSimulada` corta a los 5 s con `concurrent.futures` y traduce cualquier falla a `ConsultaAcademicaFallida`.
  - ADR-005: `TrabajoPendiente` tiene `ESPERAS_EN_MINUTOS = (1, 2, 4, 8, 15)`, `LIMITE_DE_REINTENTOS = 24 h` y `registrar_intento_fallido`. `ProcesadorPendientes.ejecutar_ciclo(ahora)` marca el trabajo "terminado", lo reprograma o lo marca "fallido" con el trabajo "avisar al administrador". Sin transacción única, `Postularse` guarda en el orden postulación, trabajo y bitácora.
  - ADR-006: la `Sesion` llega armada en `PostularseEntrada` (DT-04). No hay login ni `ProveedorIdentidad`.
  - ADR-008: `Postularse.ejecutar` llama primero a `ValidarPermiso` con el permiso "postularse", que solo tiene el rol "estudiante". El programa sale de `sesion.ambito`.
  - ADR-009: la postulación guarda `numero_version_reglas` y `VerificarRequisitos` busca esa versión y no la vigente. Hay un `ValidadorRequisito` por `TipoRequisito`, inyectado desde `main.py:113`, con comparación ≥.
  - ADR-012: `EventoBitacora` es `frozen` y tiene solo `quien`, `que`, `sobre_que`, `cuando` y `desde_donde`. El puerto y el adaptador solo tienen `insertar` y `listar`. Hay eventos de creación (`Postularse`), de cambio de estado (`VerificarPostulacion`, con quién y desde dónde = "procesador de pendientes", DP-02) y de permiso negado (`ValidarPermiso`).
  - ADR-002: aunque no está en la tabla del plan, el plan lo cita en la composición. `main.py` tiene los puntos de entrada `aplicacion` y `procesador` (`ejecutar_aplicacion` y `ejecutar_procesador`) en el mismo archivo.
- **Convenciones de AGENTS.md:**
  - Cumplen:
    - Solo se usa la librería estándar: `dataclasses`, `enum`, `typing.Protocol`, `threading`, `concurrent.futures` y `uuid`.
    - Los imports son absolutos desde `src/`, por ejemplo `from aplicacion.reglas.verificar_requisitos import VerificarRequisitos`.
    - Hay una clase por archivo: los 39 `.py` de `src/` sin contar `main.py` tienen exactamente una clase cada uno.
    - No hay ningún `__init__.py`.
    - Los casos de uso tienen DTO en la entrada y en la salida: `PostularseEntrada` y `PostularseSalida` en Postularse, y `ResultadoVerificacion` en VerificarRequisitos.
    - Los nombres son los del glosario: `Postulacion`, `EstadoPostulacion`, `esta_activa()`, `VersionReglas`, `Requisito`, `ValidadorRequisito`, `DatosAcademicos`, `ConsultaAcademica`, `EventoBitacora`, `RegistroBitacora`, `Sesion`, `TrabajoPendiente`, `ColaPendientes`, `ProcesadorPendientes` y `ManejadorTrabajo`.
  - Observaciones (no cambian el resultado):
    1. **Versión de Python.** La evidencia se produjo con Python 3.13.1, que es el instalado en la máquina, y AGENTS.md pide 3.12. El código no usa nada propio de 3.13 (lo más reciente es `dataclass(kw_only=True)`, de 3.10), pero falta correrlo con 3.12 para que la evidencia corresponda a la versión acordada. Se relaciona con DT-03.
    2. **Consola de Windows.** En la consola de Windows, con la codificación por defecto, las tildes se ven mal en la salida. Con `PYTHONIOENCODING=utf-8` se ven bien y el resultado es el mismo (48 de 48). No es un problema de la spec ni de la lógica.
    3. **Estilo.** En `main.py:797` la tupla de escenarios tiene un espaciado irregular. Es solo estilo.
    4. **Escenario 9 en la spec.** El "Dado" de la spec no fija el ámbito del docente. No afecta el resultado, pero se podría completar en la spec.
