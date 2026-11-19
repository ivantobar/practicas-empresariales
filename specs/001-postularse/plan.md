# Plan: 001 Postularse

Traza: CU-01, EAC-02, EAC-01, RT-03, PA-02, PA-03, PA-04. Escenario de arquitectura: ESC-01.

## Decisiones que aplican

| ADR | Qué implica para esta funcionalidad |
|---|---|
| [ADR-001](../../docs/adr/ADR-001-monolito-modular.md) | El código va en `dominio/`, `aplicacion/` e `infraestructura/`. Intervienen los módulos Postulación, Reglas, Acceso, Pendientes y Bitácora, y cada uno usa solo lo que permite la vista de usos (Postulación usa Reglas, Acceso, Pendientes y Bitácora; Reglas usa Bitácora; Acceso usa Bitácora; Pendientes y Bitácora no usan ningún módulo). Pendientes no conoce a Postulación: Postulación implementa `ManejadorTrabajo` y `main.py` la registra. |
| [ADR-003](../../docs/adr/ADR-003-persistencia-relacional.md) | En esta etapa no hay base de datos: los repositorios, la cola y la bitácora son adaptadores en memoria detrás de sus puertos (AGENTS.md, DT-01). El adaptador de base de datos no se hace aquí. |
| [ADR-004](../../docs/adr/ADR-004-integracion-sia.md) | `Postularse` guarda la postulación en "pendiente de verificación" y responde sin llamar al SIA. La verificación la hace después el trabajo "verificar en SIA". El SIA solo se consulta por el puerto `ConsultaAcademica`, y el adaptador corta la espera a los 5 s y convierte cualquier falla en un error de aplicación. |
| [ADR-005](../../docs/adr/ADR-005-reintentos-y-estados-pendientes.md) | La verificación y los avisos son `TrabajoPendiente` en la `ColaPendientes`. El `ProcesadorPendientes` toma cada minuto los trabajos vencidos. Si un intento falla, reprograma con espera de 1, 2, 4, 8 y luego 15 min como máximo. Si un intento falla cuando el trabajo ya tiene 24 h o más desde que se creó, el trabajo queda "fallido" y se registra un trabajo para avisar al administrador del sistema. Como no hay base de datos, no existe la transacción única de postulación, trabajo y bitácora (DT-01): se guardan en ese orden. |
| [ADR-006](../../docs/adr/ADR-006-autenticacion-institucional.md) | La `Sesion` llega ya armada al caso de uso (DT-04). Aquí no se hace login ni se usa el `ProveedorIdentidad`. |
| [ADR-008](../../docs/adr/ADR-008-autorizacion-por-roles.md) | `Postularse` declara que necesita el permiso "postularse", que solo tiene el rol `estudiante`, y lo valida con el Módulo Acceso antes de hacer cualquier otra cosa. El programa de la postulación sale del ámbito de la sesión. |
| [ADR-009](../../docs/adr/ADR-009-reglas-configurables-por-programa.md) | Al postularse se consulta en el Módulo Reglas la `VersionReglas` vigente del programa y la postulación guarda su número. La verificación usa esa versión, aunque después entre en vigencia otra. Cada tipo de `Requisito` tiene su `ValidadorRequisito`. Un requisito se cumple si el valor es mayor o igual al exigido. |
| [ADR-012](../../docs/adr/ADR-012-bitacora-auditoria.md) | Se registra un `EventoBitacora` cuando se crea la postulación, cuando cambia de estado y cuando se niega un permiso. Cada evento guarda solo quién, qué, sobre qué, cuándo y desde dónde, sin nombre, documento, promedio ni créditos. El puerto `RegistroBitacora` solo inserta. |

## Componentes

Según [vistas/03-desarrollo.md](../../docs/vistas/03-desarrollo.md). Hay una clase por archivo y ningún `__init__.py`. Los nombres de archivo van en minúsculas con guion bajo.

### dominio/ (Entidades del dominio)

| Archivo | Clase | Responsabilidad |
|---|---|---|
| `src/dominio/estado_postulacion.py` | `EstadoPostulacion` | Enum con "pendiente de verificación", "verificada" y "no cumple requisitos". |
| `src/dominio/postulacion.py` | `Postulacion` | Guarda id, estudiante, programa, empresa (nombre de la empresa de la plaza), número de versión de reglas, fecha, estado y requisitos incumplidos. Tiene `esta_activa()`. Al marcarse "verificada" o "no cumple requisitos" solo acepta pasar desde "pendiente de verificación". |
| `src/dominio/tipo_requisito.py` | `TipoRequisito` | Enum con "promedio mínimo" y "créditos aprobados mínimos". |
| `src/dominio/requisito.py` | `Requisito` | Un tipo y su valor exigido. |
| `src/dominio/version_reglas.py` | `VersionReglas` | Guarda programa, número, fecha de vigencia y requisitos. No se modifica. |
| `src/dominio/datos_academicos.py` | `DatosAcademicos` | Promedio y créditos aprobados de un estudiante, como los devuelve el SIA. |
| `src/dominio/evento_bitacora.py` | `EventoBitacora` | Quién, qué, sobre qué (opcional), cuándo y desde dónde. No tiene ningún campo para datos personales. |

### aplicacion/acceso/ (Módulo Acceso)

| Archivo | Clase | Responsabilidad |
|---|---|---|
| `src/aplicacion/acceso/sesion.py` | `Sesion` | Usuario, rol y ámbito (programa). Llega validada. |
| `src/aplicacion/acceso/permiso_negado.py` | `PermisoNegado` | Error que se lanza cuando la sesión no tiene el permiso. |
| `src/aplicacion/acceso/validar_permiso.py` | `ValidarPermiso` | Tabla de permisos por rol (aquí solo "postularse" → `estudiante`). Si el rol no tiene el permiso, registra en Bitácora un evento de permiso negado y lanza `PermisoNegado`. |

### aplicacion/bitacora/ (Módulo Bitácora)

| Archivo | Clase | Responsabilidad |
|---|---|---|
| `src/aplicacion/bitacora/puertos/registro_bitacora.py` | `RegistroBitacora` | Puerto (`Protocol`) que solo tiene `insertar(evento)` y `listar()`. |
| `src/aplicacion/bitacora/registrar_evento.py` | `RegistrarEvento` | Arma el `EventoBitacora` con la fecha actual y lo inserta. Es lo que usan los demás módulos. |

### aplicacion/pendientes/ (Módulo Pendientes)

| Archivo | Clase | Responsabilidad |
|---|---|---|
| `src/aplicacion/pendientes/estado_trabajo.py` | `EstadoTrabajo` | Enum con "pendiente", "terminado" y "fallido". |
| `src/aplicacion/pendientes/trabajo_pendiente.py` | `TrabajoPendiente` | Guarda id, tipo, referencia (por ejemplo, el id de la postulación), estado, intentos fallidos, creado en y próximo intento. Calcula la siguiente espera (1, 2, 4, 8 y 15 min como máximo) y la regla de las 24 h. |
| `src/aplicacion/pendientes/falla_reintentable.py` | `FallaReintentable` | Error con el que un manejador indica que el intento falló y se debe reintentar. |
| `src/aplicacion/pendientes/manejador_trabajo.py` | `ManejadorTrabajo` | Interfaz (`Protocol`) que implementa cada módulo: `ejecutar(trabajo)`. No es un puerto hacia infraestructura, por eso no va en `puertos/`. |
| `src/aplicacion/pendientes/puertos/cola_pendientes.py` | `ColaPendientes` | Puerto (`Protocol`) para guardar, actualizar y listar trabajos, y para tomar los vencidos a una hora dada. |
| `src/aplicacion/pendientes/registrar_trabajo.py` | `RegistrarTrabajo` | Crea un `TrabajoPendiente` listo para ejecutarse de inmediato y lo guarda en la cola. |
| `src/aplicacion/pendientes/procesador_pendientes.py` | `ProcesadorPendientes` | `ejecutar_ciclo(ahora)`: toma los trabajos vencidos y busca el manejador de cada tipo. Si el manejador termina, marca el trabajo "terminado". Si lanza `FallaReintentable`, reprograma el trabajo, o lo marca "fallido" si ya tiene 24 h, y en ese caso registra el trabajo "avisar al administrador". |

### aplicacion/reglas/ (Módulo Reglas)

| Archivo | Clase | Responsabilidad |
|---|---|---|
| `src/aplicacion/reglas/puertos/repositorio_reglas.py` | `RepositorioReglas` | Puerto (`Protocol`) para buscar las versiones de reglas de un programa. |
| `src/aplicacion/reglas/puertos/consulta_academica.py` | `ConsultaAcademica` | Puerto (`Protocol`): `consultar(estudiante) -> DatosAcademicos`, con espera máxima de 5 s. Si falla, lanza `ConsultaAcademicaFallida`. |
| `src/aplicacion/reglas/consulta_academica_fallida.py` | `ConsultaAcademicaFallida` | Error de aplicación para un SIA caído, lento o que responde con error. |
| `src/aplicacion/reglas/validador_requisito.py` | `ValidadorRequisito` | Interfaz (`Protocol`): dice si un `Requisito` se cumple con unos `DatosAcademicos`. |
| `src/aplicacion/reglas/validadores/validador_promedio_minimo.py` | `ValidadorPromedioMinimo` | Se cumple si promedio ≥ exigido. |
| `src/aplicacion/reglas/validadores/validador_creditos_aprobados_minimos.py` | `ValidadorCreditosAprobadosMinimos` | Se cumple si créditos aprobados ≥ exigido. |
| `src/aplicacion/reglas/obtener_version_vigente.py` | `ObtenerVersionVigente` | Devuelve la versión de mayor fecha de vigencia que sea menor o igual a la fecha dada. |
| `src/aplicacion/reglas/resultado_verificacion.py` | `ResultadoVerificacion` | DTO de salida: si cumple y la lista de requisitos incumplidos con su valor exigido. |
| `src/aplicacion/reglas/verificar_requisitos.py` | `VerificarRequisitos` | Con un estudiante, un programa y un número de versión, consulta `ConsultaAcademica` y aplica el validador de cada requisito de esa versión. Deja pasar `ConsultaAcademicaFallida`. |

### aplicacion/postulacion/ (Módulo Postulación)

| Archivo | Clase | Responsabilidad |
|---|---|---|
| `src/aplicacion/postulacion/puertos/repositorio_postulaciones.py` | `RepositorioPostulaciones` | Puerto (`Protocol`) para guardar, actualizar, buscar por id y listar las postulaciones de un estudiante. |
| `src/aplicacion/postulacion/postularse_entrada.py` | `PostularseEntrada` | DTO de entrada: sesión, empresa y desde dónde (origen). |
| `src/aplicacion/postulacion/postularse_salida.py` | `PostularseSalida` | DTO de salida: id de la postulación, estado y el mensaje "postulación recibida, te avisamos el resultado". |
| `src/aplicacion/postulacion/postulacion_activa_existente.py` | `PostulacionActivaExistente` | Error con el mensaje "ya tienes una postulación en curso". |
| `src/aplicacion/postulacion/postularse.py` | `Postularse` | Caso de uso CU-01. En orden: valida el permiso, revisa que no haya postulación activa, obtiene la versión vigente del programa del ámbito, guarda la postulación, registra el trabajo "verificar en SIA" y el evento de bitácora, y responde. No usa `ConsultaAcademica`. |
| `src/aplicacion/postulacion/verificar_postulacion.py` | `VerificarPostulacion` | `ManejadorTrabajo` del tipo "verificar en SIA". Llama a `VerificarRequisitos` con la versión guardada en la postulación y cambia el estado. Registra el evento de bitácora del cambio y el trabajo "avisar al estudiante". Si recibe `ConsultaAcademicaFallida`, lanza `FallaReintentable` y la postulación no cambia. |

### infraestructura/ (adaptadores de salida)

| Archivo | Clase | Implementa |
|---|---|---|
| `src/infraestructura/memoria/repositorio_postulaciones_en_memoria.py` | `RepositorioPostulacionesEnMemoria` | `RepositorioPostulaciones`, protegido con `threading.Lock` para el escenario 5. |
| `src/infraestructura/memoria/repositorio_reglas_en_memoria.py` | `RepositorioReglasEnMemoria` | `RepositorioReglas`. |
| `src/infraestructura/memoria/cola_pendientes_en_memoria.py` | `ColaPendientesEnMemoria` | `ColaPendientes`, con `threading.Lock`. |
| `src/infraestructura/memoria/registro_bitacora_en_memoria.py` | `RegistroBitacoraEnMemoria` | `RegistroBitacora`, solo inserción y con `threading.Lock`. |
| `src/infraestructura/sia/consulta_academica_simulada.py` | `ConsultaAcademicaSimulada` | `ConsultaAcademica`. Es el simulador del SIA que pide ADR-004: se configura con datos por estudiante, demora y error, y cuenta las consultas. Corta la espera con `concurrent.futures` a los 5 s (se puede cambiar el valor) y traduce toda falla a `ConsultaAcademicaFallida`. |

### Composición

| Archivo | Responsabilidad |
|---|---|
| `src/main.py` | Arma los adaptadores, los módulos y los casos de uso. Registra `VerificarPostulacion` en el `ProcesadorPendientes` para el tipo "verificar en SIA". Tiene dos puntos de entrada, la aplicación y el procesador (`ejecutar_ciclo` cada minuto), como pide ADR-002 ("misma imagen, otro punto de entrada"). |

## Decisiones pendientes

Ninguna. Las tres que dejó el plan se resolvieron en la revisión:

- DP-01: en esta funcionalidad solo se registran los trabajos "avisar al estudiante" y "avisar al administrador"; quién los envía (Notificador) se decide en otra funcionalidad.
- DP-02: en los eventos de bitácora que genera el procesador, quién = "procesador de pendientes" y desde dónde = "procesador de pendientes".
- DP-03: no hay pruebas automatizadas (lámina 51 del curso). La validación se hace escenario por escenario en validacion.md, con la evidencia que da `python src/main.py`, que ejecuta los 11 escenarios con datos de ejemplo y hora simulada (`ahora`).

### Cobertura de los escenarios de spec.md

| Escenario | Componentes que lo cubren |
|---|---|
| 1. Envía y recibe confirmación | `Postularse`, `PostularseSalida`, `ObtenerVersionVigente`, `RegistrarTrabajo`, `RegistrarEvento`, `EventoBitacora`, `ConsultaAcademicaSimulada` (cuenta 0 consultas) |
| 2. SIA responde y cumple | `ProcesadorPendientes`, `VerificarPostulacion`, `VerificarRequisitos`, validadores, `Postulacion`, `RegistrarEvento`, `RegistrarTrabajo` |
| 3. SIA responde y no cumple | Los mismos del 2, más `ResultadoVerificacion` y `Postulacion.requisitos_incumplidos` |
| 4. Ya tiene postulación activa | `Postularse`, `Postulacion.esta_activa()`, `PostulacionActivaExistente` |
| 5. 30 a la vez con el SIA caído | `Postularse` (no llama al SIA), adaptadores en memoria con `threading.Lock` |
| 6. SIA no responde en 5 s | `ConsultaAcademicaSimulada` (corte a 5 s), `VerificarPostulacion` (`FallaReintentable`), `TrabajoPendiente` (1, 2, 4, 8, 15), `ProcesadorPendientes` |
| 7. SIA con error 3 h y luego se recupera | `TrabajoPendiente` (espera máxima de 15 min) y `ProcesadorPendientes`: se verifica en máximo 15 min más un ciclo de 1 min, menos que los 30 min |
| 8. 24 h sin verificar | `TrabajoPendiente` (regla de 24 h), `ProcesadorPendientes` (estado "fallido" y trabajo "avisar al administrador") |
| 9. Rol sin permiso | `ValidarPermiso`, `PermisoNegado`, `RegistrarEvento` |
| 10. Conserva su versión de reglas | `Postulacion` (número de versión), `VerificarPostulacion`, `VerificarRequisitos` (usa la versión dada, no la vigente) |
| 11. Puede volver a postularse | `Postulacion.esta_activa()`, `Postularse`, `ObtenerVersionVigente` |

## Flujo

Se sigue [diagramas/secuencias/cu01-postularse.puml](../../docs/diagramas/secuencias/cu01-postularse.puml) (ESC-01).

1. Petición del estudiante: `Postularse` → `ValidarPermiso` → `RepositorioPostulaciones` (¿tiene una activa?) → `ObtenerVersionVigente` → guarda `Postulacion` → `RegistrarTrabajo` ("verificar en SIA") → `RegistrarEvento` → `PostularseSalida`. El SIA no se consulta.
2. En segundo plano: `ProcesadorPendientes.ejecutar_ciclo(ahora)` → `VerificarPostulacion` → `VerificarRequisitos` → `ConsultaAcademica` (máximo 5 s) → validadores → cambio de estado, evento de bitácora y trabajo "avisar al estudiante". Si falla, se reprograma, o queda "fallido" con el trabajo "avisar al administrador".

Los dos pasos del diagrama de secuencia que envían correo (SMTP) dependen de DP-01.

## Datos

- Del modelo de dominio ([vistas/01-logica.md](../../docs/vistas/01-logica.md)): `Postulacion`, `VersionReglas`, `Requisito`, `EventoBitacora`. Para `Estudiante` y `Programa` solo se usan sus identificadores, que salen de la sesión: el usuario y el ámbito. Para `Empresa` solo se guarda el nombre que da el estudiante, porque el convenio no se revisa (decisión 1 de spec.md).
- Objetos de valor y estados: `DatosAcademicos`, `EstadoPostulacion`, `TipoRequisito`.
- Técnicos, fuera del modelo de dominio: `TrabajoPendiente`, `EstadoTrabajo` y `Sesion`.
- Datos de ejemplo de la spec, para las pruebas y para `main.py`: "Ingeniería de Sistemas" con la versión de reglas 3 (promedio 3.5, créditos 130) y la versión 4 (promedio 4.0) para el escenario 10.

## Fuera de alcance

- Controladores web, códigos HTTP (202/409) y login real (DT-04). El caso de uso devuelve DTO y lanza errores, y el controlador los traducirá después.
- Adaptador real del SIA por HTTPS y adaptador de base de datos con transacción única (DT-01).
- Revisar si el convenio de la empresa está vigente (decisión 1 de spec.md).
- Autorización de tratamiento de datos, RN-01 (decisión 4).
- Alerta de postulaciones pendientes con más de 2 h, R-05 (decisión 5).
- Textos exactos de los avisos (decisión 6) y aviso al estudiante cuando el trabajo queda "fallido" (decisión 7, DT-02).
- CU-02 (aprobar o rechazar) y CU-12 (crear versiones de reglas). Aquí las versiones se cargan como datos de ejemplo.
- Limpieza de la tabla de trabajos (ADR-005).

## Decisiones pendientes

- **DP-01. ¿Quién ejecuta los trabajos de aviso ("avisar al estudiante" y "avisar al administrador")?** La spec solo pide que queden registrados (escenarios 2, 3 y 8), pero el diagrama de secuencia muestra el envío por SMTP. Según la vista de desarrollo, el puerto `Notificador` es del Módulo Pendientes, aunque dice también que "Evaluación y Actas hacen lo mismo para sus correos", es decir, cada módulo registra su propio manejador. Hay dos opciones:
  - (a) Un manejador genérico `EnviarAviso` en Pendientes que usa `Notificador`, con un `NotificadorEnMemoria`.
  - (b) En esta funcionalidad solo se registran los trabajos, y quién los envía se decide en otra funcionalidad.

  Recomendación: (b), porque cumple la spec sin crear componentes que la vista no aclara.
- **DP-02. ¿Qué "quién" y qué "desde dónde" llevan los eventos de bitácora que genera el procesador?** Por ejemplo, el cambio a "verificada", que no tiene sesión de usuario. Ningún ADR lo dice. Propuesta: quién = "procesador de pendientes" y desde dónde = "procesador de pendientes".
- **DP-03. ¿Dónde van las pruebas y cómo se corren?** Ni AGENTS.md ni ningún ADR lo dice. Como no hay `__init__.py`, `unittest discover` no entra en subcarpetas. Propuesta: carpeta plana `pruebas/` en la raíz, y se corren desde la raíz con `PYTHONPATH=src` y `python -m unittest discover -s pruebas`.
