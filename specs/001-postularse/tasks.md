# Tareas: 001 Postularse

<!-- Dominio -->

- [x] T-01 Enum EstadoPostulacion
      Archivos: src/dominio/estado_postulacion.py
      Escenarios: 1, 2, 3, 4, 11
      Depende de: ninguna

- [x] T-02 Enum TipoRequisito
      Archivos: src/dominio/tipo_requisito.py
      Escenarios: 3
      Depende de: ninguna

- [x] T-03 Objeto de valor Requisito (tipo y valor exigido)
      Archivos: src/dominio/requisito.py
      Escenarios: 3
      Depende de: T-02

- [x] T-04 Entidad VersionReglas (programa, número, fecha de vigencia y requisitos; no se modifica)
      Archivos: src/dominio/version_reglas.py
      Escenarios: 1, 10, 11
      Depende de: T-03

- [x] T-05 Objeto de valor DatosAcademicos (promedio y créditos aprobados)
      Archivos: src/dominio/datos_academicos.py
      Escenarios: 2, 3, 10
      Depende de: ninguna

- [x] T-06 Entidad Postulacion con esta_activa() y transiciones válidas solo desde "pendiente de verificación"
      Archivos: src/dominio/postulacion.py
      Escenarios: 1, 2, 3, 4, 10, 11
      Depende de: T-01, T-03

- [x] T-07 Entidad EventoBitacora sin campos para datos personales
      Archivos: src/dominio/evento_bitacora.py
      Escenarios: 1, 2, 3, 9
      Depende de: ninguna

<!-- Aplicación: Módulo Bitácora -->

- [x] T-08 Puerto RegistroBitacora (solo insertar y listar)
      Archivos: src/aplicacion/bitacora/puertos/registro_bitacora.py
      Escenarios: 1, 2, 3, 9
      Depende de: T-07

- [x] T-09 RegistrarEvento: arma el evento con la fecha actual y lo inserta
      Archivos: src/aplicacion/bitacora/registrar_evento.py
      Escenarios: 1, 2, 3, 9
      Depende de: T-07, T-08

<!-- Aplicación: Módulo Acceso (seguridad) -->

- [x] T-10 DTO Sesion (usuario, rol y ámbito)
      Archivos: src/aplicacion/acceso/sesion.py
      Escenarios: 1, 9
      Depende de: ninguna

- [x] T-11 Error PermisoNegado
      Archivos: src/aplicacion/acceso/permiso_negado.py
      Escenarios: 9
      Depende de: ninguna

- [x] T-12 ValidarPermiso: tabla de permisos por rol ("postularse" → estudiante), registra el permiso negado en bitácora y lanza PermisoNegado
      Archivos: src/aplicacion/acceso/validar_permiso.py
      Escenarios: 9
      Depende de: T-09, T-10, T-11

<!-- Aplicación: Módulo Pendientes (manejo de errores) -->

- [x] T-13 Enum EstadoTrabajo ("pendiente", "terminado", "fallido")
      Archivos: src/aplicacion/pendientes/estado_trabajo.py
      Escenarios: 2, 8
      Depende de: ninguna

- [x] T-14 TrabajoPendiente: espera creciente 1, 2, 4, 8 y máximo 15 min, y regla de las 24 h
      Archivos: src/aplicacion/pendientes/trabajo_pendiente.py
      Escenarios: 1, 6, 7, 8
      Depende de: T-13

- [x] T-15 Error FallaReintentable
      Archivos: src/aplicacion/pendientes/falla_reintentable.py
      Escenarios: 6, 7
      Depende de: ninguna

- [x] T-16 Interfaz ManejadorTrabajo (ejecutar(trabajo))
      Archivos: src/aplicacion/pendientes/manejador_trabajo.py
      Escenarios: 2, 3, 6
      Depende de: T-14

- [x] T-17 Puerto ColaPendientes (guardar, actualizar, listar y tomar vencidos a una hora dada)
      Archivos: src/aplicacion/pendientes/puertos/cola_pendientes.py
      Escenarios: 1, 5, 6, 8
      Depende de: T-14

- [x] T-18 RegistrarTrabajo: crea un trabajo listo para ejecutarse de inmediato y lo guarda
      Archivos: src/aplicacion/pendientes/registrar_trabajo.py
      Escenarios: 1, 2, 3, 5, 8
      Depende de: T-14, T-17

- [x] T-19 ProcesadorPendientes.ejecutar_ciclo(ahora): ejecuta vencidos, marca terminado, reprograma o marca fallido y registra "avisar al administrador"
      Archivos: src/aplicacion/pendientes/procesador_pendientes.py
      Escenarios: 2, 6, 7, 8
      Depende de: T-15, T-16, T-17, T-18

<!-- Aplicación: Módulo Reglas -->

- [x] T-20 Puerto RepositorioReglas (buscar versiones de reglas de un programa)
      Archivos: src/aplicacion/reglas/puertos/repositorio_reglas.py
      Escenarios: 1, 10, 11
      Depende de: T-04

- [x] T-21 Error ConsultaAcademicaFallida (SIA caído, lento o con error)
      Archivos: src/aplicacion/reglas/consulta_academica_fallida.py
      Escenarios: 6, 7
      Depende de: ninguna

- [x] T-22 Puerto ConsultaAcademica (consultar(estudiante) -> DatosAcademicos, espera máxima de 5 s)
      Archivos: src/aplicacion/reglas/puertos/consulta_academica.py
      Escenarios: 2, 3, 6, 7
      Depende de: T-05, T-21

- [x] T-23 Interfaz ValidadorRequisito
      Archivos: src/aplicacion/reglas/validador_requisito.py
      Escenarios: 2, 3
      Depende de: T-03, T-05

- [x] T-24 ValidadorPromedioMinimo (promedio ≥ exigido)
      Archivos: src/aplicacion/reglas/validadores/validador_promedio_minimo.py
      Escenarios: 2, 3, 10
      Depende de: T-23

- [x] T-25 ValidadorCreditosAprobadosMinimos (créditos aprobados ≥ exigido)
      Archivos: src/aplicacion/reglas/validadores/validador_creditos_aprobados_minimos.py
      Escenarios: 2, 3
      Depende de: T-23

- [x] T-26 ObtenerVersionVigente: versión de mayor fecha de vigencia menor o igual a la fecha dada
      Archivos: src/aplicacion/reglas/obtener_version_vigente.py
      Escenarios: 1, 10, 11
      Depende de: T-20

- [x] T-27 DTO ResultadoVerificacion (si cumple y requisitos incumplidos con su valor exigido)
      Archivos: src/aplicacion/reglas/resultado_verificacion.py
      Escenarios: 2, 3
      Depende de: T-03

- [x] T-28 VerificarRequisitos: consulta el SIA y aplica los validadores de la versión dada; deja pasar ConsultaAcademicaFallida
      Archivos: src/aplicacion/reglas/verificar_requisitos.py
      Escenarios: 2, 3, 6, 7, 10
      Depende de: T-20, T-22, T-24, T-25, T-27

<!-- Aplicación: Módulo Postulación -->

- [x] T-29 Puerto RepositorioPostulaciones (guardar, actualizar, buscar por id y listar por estudiante)
      Archivos: src/aplicacion/postulacion/puertos/repositorio_postulaciones.py
      Escenarios: 1, 4, 5, 11
      Depende de: T-06

- [x] T-30 DTO PostularseEntrada (sesión, empresa y origen)
      Archivos: src/aplicacion/postulacion/postularse_entrada.py
      Escenarios: 1, 9
      Depende de: T-10

- [x] T-31 DTO PostularseSalida (id, estado y mensaje "postulación recibida, te avisamos el resultado")
      Archivos: src/aplicacion/postulacion/postularse_salida.py
      Escenarios: 1, 5
      Depende de: T-01

- [x] T-32 Error PostulacionActivaExistente ("ya tienes una postulación en curso")
      Archivos: src/aplicacion/postulacion/postulacion_activa_existente.py
      Escenarios: 4
      Depende de: ninguna

- [x] T-33 Caso de uso Postularse: permiso, postulación activa, versión vigente, guardar, trabajo "verificar en SIA", bitácora y respuesta; sin consultar el SIA
      Archivos: src/aplicacion/postulacion/postularse.py
      Escenarios: 1, 4, 5, 9, 11
      Depende de: T-06, T-09, T-12, T-18, T-26, T-29, T-30, T-31, T-32

- [x] T-34 VerificarPostulacion (ManejadorTrabajo "verificar en SIA"): verifica con la versión guardada, cambia el estado, registra bitácora y "avisar al estudiante"; convierte ConsultaAcademicaFallida en FallaReintentable
      Archivos: src/aplicacion/postulacion/verificar_postulacion.py
      Escenarios: 2, 3, 6, 7, 10
      Depende de: T-06, T-09, T-15, T-16, T-18, T-21, T-28, T-29

<!-- Infraestructura -->

- [x] T-35 RepositorioPostulacionesEnMemoria con threading.Lock
      Archivos: src/infraestructura/memoria/repositorio_postulaciones_en_memoria.py
      Escenarios: 1, 4, 5, 11
      Depende de: T-29

- [x] T-36 RepositorioReglasEnMemoria
      Archivos: src/infraestructura/memoria/repositorio_reglas_en_memoria.py
      Escenarios: 1, 10, 11
      Depende de: T-20

- [x] T-37 ColaPendientesEnMemoria con threading.Lock
      Archivos: src/infraestructura/memoria/cola_pendientes_en_memoria.py
      Escenarios: 1, 5, 6, 7, 8
      Depende de: T-17

- [x] T-38 RegistroBitacoraEnMemoria, solo inserción, con threading.Lock
      Archivos: src/infraestructura/memoria/registro_bitacora_en_memoria.py
      Escenarios: 1, 2, 3, 9
      Depende de: T-08

- [x] T-39 ConsultaAcademicaSimulada: datos por estudiante, demora y error configurables, contador de consultas, corte a 5 s con concurrent.futures y traducción de fallas a ConsultaAcademicaFallida
      Archivos: src/infraestructura/sia/consulta_academica_simulada.py
      Escenarios: 1, 2, 3, 4, 5, 6, 7, 10
      Depende de: T-21, T-22

<!-- Composición -->

- [ ] T-40 main.py: armar adaptadores, módulos y casos de uso; registrar VerificarPostulacion para "verificar en SIA"; puntos de entrada de la aplicación y del procesador
      Archivos: src/main.py
      Escenarios: 2, 3, 6, 7, 8
      Depende de: T-19, T-33, T-34, T-35, T-36, T-37, T-38, T-39

- [ ] T-41 main.py: ejecución con datos de ejemplo de los escenarios del flujo de la petición (1, 4, 9 y 11)
      Archivos: src/main.py
      Escenarios: 1, 4, 9, 11
      Depende de: T-40

- [ ] T-42 main.py: ejecución con datos de ejemplo y hora simulada de los escenarios del procesador (2, 3, 6, 7, 8 y 10) y de los 30 estudiantes a la vez (5)
      Archivos: src/main.py
      Escenarios: 2, 3, 5, 6, 7, 8, 10
      Depende de: T-41

<!-- Validación -->

- [ ] T-43 Validación escenario por escenario con la evidencia de python src/main.py y revisión de la regla de dependencia (R-07)
      Archivos: specs/001-postularse/validacion.md
      Escenarios: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11
      Depende de: T-42
