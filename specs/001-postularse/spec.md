# language: es
# Traza: CU-01, EAC-02, EAC-01, RT-03, PA-02, PA-03, PA-04, ADR-004, ADR-005, ADR-008, ADR-009, ADR-012
# Escenario de arquitectura: ESC-01 (docs/diagramas/secuencias/cu01-postularse.puml)
#
# Datos de ejemplo usados en los escenarios (son datos de prueba, no reglas de negocio):
#   - Estudiante "E-1001" del programa "Ingeniería de Sistemas".
#   - Versión de reglas 3 de "Ingeniería de Sistemas", vigente, con dos requisitos:
#       promedio mínimo 3.5 y créditos aprobados mínimos 130.
#   - Tiempos de espera entre intentos de ADR-005: 1, 2, 4, 8 y máximo 15 minutos.

Característica: Postularse a la práctica empresarial
  Como estudiante con la plaza ya conseguida, quiero postularme ante la Facultad
  para que se verifiquen mis requisitos académicos en el SIA y pueda empezar mi práctica.

  Antecedentes:
    Dado que la sesión del usuario llega validada con usuario "E-1001", rol "estudiante" y ámbito "Ingeniería de Sistemas"
    Y que el programa "Ingeniería de Sistemas" tiene vigente la versión de reglas 3
    Y que la versión de reglas 3 exige promedio mínimo 3.5 y créditos aprobados mínimos 130
    Y que el estudiante "E-1001" no tiene ninguna postulación activa

  # --- Flujo básico ---

  Escenario: 1. El estudiante envía su postulación y recibe la confirmación de recepción
    Cuando el estudiante "E-1001" envía su postulación
    Entonces queda guardada una postulación del estudiante "E-1001" en estado "pendiente de verificación"
    Y la postulación queda con la versión de reglas 3 de "Ingeniería de Sistemas"
    Y queda registrado un trabajo pendiente "verificar en SIA" para esa postulación
    Y queda un evento de bitácora con quién ("E-1001"), qué (postulación creada en "pendiente de verificación"), sobre qué (la postulación), cuándo y desde dónde
    Y el evento de bitácora no contiene el nombre, el documento, el promedio ni los créditos del estudiante
    Y el estudiante recibe la confirmación "postulación recibida, te avisamos el resultado"
    Y el sistema no consultó el SIA antes de dar la confirmación

  Escenario: 2. El SIA responde y el estudiante cumple los requisitos
    Dado que la postulación de "E-1001" está en estado "pendiente de verificación" con la versión de reglas 3
    Y que el SIA devuelve para "E-1001" promedio 3.8 y créditos aprobados 140
    Cuando se ejecuta el trabajo pendiente "verificar en SIA" de esa postulación
    Y el SIA responde en menos de 5 segundos
    Entonces la postulación pasa a estado "verificada"
    Y queda un evento de bitácora del cambio de "pendiente de verificación" a "verificada"
    Y queda registrado un trabajo pendiente para avisar el resultado al estudiante "E-1001"
    Y el trabajo "verificar en SIA" queda terminado y no se vuelve a ejecutar

  # --- Flujos alternos y excepciones ---

  Escenario: 3. El SIA responde y el estudiante no cumple los requisitos
    Dado que la postulación de "E-1001" está en estado "pendiente de verificación" con la versión de reglas 3
    Y que el SIA devuelve para "E-1001" promedio 3.2 y créditos aprobados 140
    Cuando se ejecuta el trabajo pendiente "verificar en SIA" de esa postulación
    Y el SIA responde en menos de 5 segundos
    Entonces la postulación pasa a estado "no cumple requisitos"
    Y el resultado indica que no se cumplió el requisito "promedio mínimo" (exigido 3.5)
    Y el resultado no marca como incumplido el requisito "créditos aprobados mínimos"
    Y queda un evento de bitácora del cambio de "pendiente de verificación" a "no cumple requisitos"
    Y queda registrado un trabajo pendiente para avisar el resultado al estudiante "E-1001"

  Escenario: 4. El estudiante ya tiene una postulación activa
    Dado que el estudiante "E-1001" tiene una postulación en estado "pendiente de verificación"
    Cuando el estudiante "E-1001" envía otra postulación
    Entonces el sistema rechaza la postulación con el mensaje "ya tienes una postulación en curso"
    Y el estudiante "E-1001" sigue teniendo exactamente 1 postulación
    Y no queda registrado ningún trabajo pendiente nuevo
    Y no se consultó el SIA

  # --- EAC-02: fiabilidad cuando el SIA falla ---

  Escenario: 5. EAC-02: confirmación en menos de 3 segundos con el SIA caído en el pico de inicio de periodo
    Dado que el SIA no responde
    Y que hay 30 estudiantes distintos, cada uno sin postulación activa
    Cuando los 30 estudiantes envían su postulación al mismo tiempo
    Entonces quedan guardadas 30 postulaciones en estado "pendiente de verificación"
    Y quedan registrados 30 trabajos pendientes "verificar en SIA"
    Y al menos 95% de los estudiantes recibe la confirmación "postulación recibida, te avisamos el resultado" en menos de 3 segundos
    Y 0 postulaciones se pierden

  Escenario: 6. EAC-02: el SIA no responde en 5 segundos durante la verificación
    Dado que la postulación de "E-1001" está en estado "pendiente de verificación"
    Y que el SIA tarda más de 5 segundos en responder
    Cuando se ejecuta el trabajo pendiente "verificar en SIA" de esa postulación
    Entonces la espera por el SIA se corta a los 5 segundos
    Y la postulación sigue en estado "pendiente de verificación"
    Y el trabajo queda reprogramado para dentro de 1 minuto
    Y si los siguientes intentos también fallan, se reprograman para dentro de 2, 4, 8, 15, 15, ... minutos
    Y ninguna espera entre intentos es mayor de 15 minutos

  Escenario: 7. EAC-02: el SIA responde con error y luego se recupera
    Dado que la postulación de "E-1001" está en estado "pendiente de verificación"
    Y que el SIA responde con error en cada intento durante 3 horas
    Cuando el SIA vuelve a responder correctamente con promedio 3.8 y créditos aprobados 140
    Entonces la postulación pasa a estado "verificada" en máximo 30 minutos desde que el SIA se recuperó
    Y durante las 3 horas la postulación nunca dejó de estar guardada en estado "pendiente de verificación"
    Y 0 postulaciones se pierden

  Escenario: 8. EAC-02: la verificación no se logra en 24 horas
    Dado que la postulación de "E-1001" está en estado "pendiente de verificación"
    Y que el trabajo "verificar en SIA" de esa postulación lleva 24 horas fallando
    Cuando se cumple el siguiente ciclo del procesador de pendientes
    Entonces el trabajo "verificar en SIA" queda en estado "fallido" y no se vuelve a intentar
    Y queda registrado un trabajo pendiente para avisar al administrador del sistema
    Y la postulación sigue guardada en estado "pendiente de verificación"

  # --- Seguridad (PA-02, ADR-008, ADR-012) ---

  Escenario: 9. Un usuario sin rol de estudiante intenta postularse
    Dado que la sesión del usuario llega validada con usuario "D-0042" y rol "docente asesor"
    Cuando el usuario "D-0042" intenta enviar una postulación
    Entonces el sistema niega la operación por falta de permiso
    Y no queda guardada ninguna postulación
    Y no queda registrado ningún trabajo pendiente
    Y queda un evento de bitácora de permiso negado con quién ("D-0042"), qué (postularse), cuándo y desde dónde

  # --- EAC-01: la postulación conserva su versión de reglas ---

  Escenario: 10. EAC-01: la postulación se verifica con la versión de reglas con la que se hizo
    Dado que la postulación de "E-1001" está en estado "pendiente de verificación" con la versión de reglas 3
    Y que después de postularse entra en vigencia la versión de reglas 4 de "Ingeniería de Sistemas" con promedio mínimo 4.0
    Y que el SIA devuelve para "E-1001" promedio 3.8 y créditos aprobados 140
    Cuando se ejecuta el trabajo pendiente "verificar en SIA" de esa postulación
    Entonces la postulación se verifica contra la versión de reglas 3
    Y la postulación pasa a estado "verificada"
    Y la postulación sigue con la versión de reglas 3

  Escenario: 11. El estudiante puede volver a postularse si la anterior no cumplió requisitos
    Dado que el estudiante "E-1001" tiene una postulación en estado "no cumple requisitos"
    Y que no tiene ninguna postulación activa
    Cuando el estudiante "E-1001" envía una postulación nueva
    Entonces queda guardada una postulación nueva en estado "pendiente de verificación" con la versión de reglas vigente
    Y la postulación anterior sigue en estado "no cumple requisitos"

# ---------------------------------------------------------------------------
# Decisiones de la revisión (sin marcas pendientes)
# ---------------------------------------------------------------------------
# 1. La postulación registra la empresa de la plaza (S-04). El convenio no se revisa aquí: no está en ESC-01.
# 2. Supuesto: todo programa tiene una versión de reglas vigente (la crea CU-12, ADR-009).
# 3. El programa del estudiante sale del ámbito de la sesión (ADR-008).
# 4. La autorización de tratamiento de datos (RN-01) queda fuera de esta spec; se valida con el área jurídica.
# 5. La alerta de postulaciones pendientes con más de 2 h (R-05) queda fuera de esta spec: es un reporte de operación.
# 6. No se fijan textos exactos de los avisos; el aviso de "no cumple" lista cada requisito incumplido con su valor exigido.
# 7. Si el trabajo queda "fallido", el estudiante no recibe aviso; se acepta como deuda técnica (DT-02).
# 8. Un requisito se cumple con un valor mayor o igual al exigido.