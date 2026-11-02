# Drivers arquitectónicos: Sistema de Gestión de Prácticas Empresariales

> **Enunciado.** *Partiendo del documento de visión del taller anterior, produzcan: lista de casos de uso (mínimo 12) marcando los primarios (máximo 6), justificando cada elección con uno de los cinco criterios; tres escenarios de atributos de calidad completos, con las seis partes, sobre atributos distintos (al menos uno de mantenibilidad); tabla de restricciones con ID, tipo, origen e impacto arquitectónico esperado; cinco preocupaciones arquitectónicas; matriz de priorización con los drivers ubicados en los cuatro cuadrantes.*

Los drivers son el subconjunto de requisitos que, si cambiaran radicalmente, obligarían a rediseñar la estructura del sistema. Aquí se identifican 22 drivers: 5 casos de uso primarios, 3 escenarios de atributos de calidad, 9 restricciones y 5 preocupaciones arquitectónicas.

## 1. Casos de uso y casos de uso primarios

Criterios para que un caso de uso sea primario: **(1)** importancia para el negocio, **(2)** complejidad técnica, **(3)** alta frecuencia de uso, **(4)** riesgo, **(5)** atado a un atributo de calidad crítico.

| ID | Caso de uso | Actor | ¿Primario? | Justificación |
|---|---|---|---|---|
| **CU-01** | Postularse a la práctica empresarial | Estudiante | **Sí** | **(2) Complejidad técnica:** verifica los requisitos académicos contra los servicios del SIA (RT-03), única integración con otro sistema |
| **CU-02** | Aprobar o rechazar la postulación | Director de programa | No | Decisión sobre datos ya verificados en CU-01; no ejercita nada nuevo |
| **CU-03** | Asignar el docente asesor de práctica | Director de programa | No | Registro simple con consulta de la carga de cada docente asesor |
| **CU-04** | Registrar las horas semanales | Estudiante | No | Es el más frecuente, pero son a lo sumo 250 registros por semana (S-03): no es carga alta y es un formulario simple |
| **CU-05** | Validar las horas registradas | Supervisor de empresa | No | Usa el mismo acceso por enlace sin cuenta que CU-07; no ejercita nada nuevo |
| **CU-06** | Revisar horas y avance del practicante | Docente asesor | No | Consulta de datos existentes |
| **CU-07** | Evaluar el desempeño del practicante | Supervisor de empresa | **Sí** | **(4) Riesgo:** si el supervisor no responde no hay acta (R-01, OB-02), y es un usuario externo sin cuenta institucional (RN-04) |
| **CU-08** | Enviar recordatorios de plazos | Sistema (tarea programada) | No | Envío periódico de bajo volumen por el correo institucional; no cambia la estructura |
| **CU-09** | Generar el acta final de la práctica | Sistema, a solicitud del docente asesor | **Sí** | **(1) Importancia para el negocio:** es la razón de ser del sistema y de ella dependen OB-01 y OB-04 |
| **CU-10** | Aprobar el acta electrónicamente | Docente asesor y director de programa | **Sí** | **(5) Atado a un atributo crítico:** seguridad (trazabilidad de quién aprobó el acta y cuándo, OB-06, S-06) |
| **CU-11** | Consultar el estado del trámite | Estudiante | No | Consulta simple, no ejercita nada nuevo |
| **CU-12** | Configurar las reglas de práctica de un programa | Director de programa | **Sí** | **(5) Atado a un atributo crítico:** mantenibilidad (OB-05), porque requisitos y horas varían por programa (S-07) |
| **CU-13** | Monitorear el estado de las prácticas | Director de programa | No | Consulta de datos que ya registraron los demás casos de uso |
| **CU-14** | Generar el consolidado para auditoría o acreditación | Director de programa | No | Importante para el negocio (OB-06), pero es un reporte sobre datos existentes: no estructura nada |
| **CU-15** | Migrar las prácticas en curso desde Excel | Administrador del sistema | No | Se ejecuta una sola vez, al lanzamiento |

## 2. Escenarios de atributos de calidad

Tres escenarios sobre atributos distintos de ISO/IEC 25010:2023. Cada medida de respuesta tiene un número que se puede verificar con una prueba o con el registro de operación.

### EAC-01: Mantenibilidad (modificabilidad)

| Parte | Pregunta | Contenido |
|---|---|---|
| **1. Fuente del estímulo** | ¿Quién o qué lo provoca? | Un desarrollador con un mes en el proyecto |
| **2. Estímulo** | ¿Qué ocurre? | Debe incorporar las reglas de práctica de un programa nuevo aprobadas por el Consejo de Facultad: horas mínimas diferentes y un requisito académico adicional |
| **3. Artefacto** | ¿Sobre qué parte? | El módulo de reglas de práctica y su configuración |
| **4. Entorno** | ¿En qué condiciones? | Tiempo de desarrollo, con el sistema en operación y prácticas de otros programas en curso |
| **5. Respuesta** | ¿Qué debe hacer el sistema? | Hace el cambio y lo despliega sin afectar las prácticas en curso de los demás programas |
| **6. Medida de respuesta** | ¿Cómo se verifica? | **En máximo 16 horas de trabajo, modificando como máximo 2 módulos, y con 0 prácticas en curso de otros programas que cambien de estado o de reglas** |

**Escenario redactado.** *Un desarrollador con un mes en el proyecto debe incorporar las reglas de práctica de un programa nuevo (horas mínimas diferentes y un requisito académico adicional) en el módulo de reglas, con el sistema en operación. Hace el cambio y lo despliega en máximo 16 horas de trabajo, modificando como máximo 2 módulos y sin que ninguna práctica en curso de otro programa cambie de estado o de reglas.*

**Traza:** OB-05, S-07, CU-12

### EAC-02: Fiabilidad (tolerancia a fallos)

| Parte | Pregunta | Contenido |
|---|---|---|
| **1. Fuente del estímulo** | ¿Quién o qué lo provoca? | El servicio de consulta del SIA |
| **2. Estímulo** | ¿Qué ocurre? | No responde en 5 segundos, o responde con error, cuando un estudiante envía su postulación |
| **3. Artefacto** | ¿Sobre qué parte? | El componente de integración con el SIA usado por CU-01 |
| **4. Entorno** | ¿En qué condiciones? | Operación normal en el pico de inicio de periodo, con hasta 30 usuarios concurrentes (S-03) |
| **5. Respuesta** | ¿Qué debe hacer el sistema? | Guarda la postulación como "pendiente de verificación", confirma al estudiante que fue recibida y reintenta la verificación automáticamente |
| **6. Medida de respuesta** | ¿Cómo se verifica? | **0 postulaciones perdidas; confirmación al estudiante en menos de 3 segundos en el 95% de los casos; verificación completada en máximo 30 minutos después de que el SIA se recupera, en el 100% de los casos** |

**Escenario redactado.** *Cuando el servicio de consulta del SIA no responde en 5 segundos durante una postulación, en el pico de inicio de periodo con hasta 30 usuarios concurrentes, el sistema guarda la postulación como pendiente, confirma su recepción al estudiante en menos de 3 segundos (95% de los casos) y completa la verificación en máximo 30 minutos después de que el SIA se recupera, sin perder ninguna postulación.*

**Traza:** OB-01, RT-03, R-02, CU-01

### EAC-03: Seguridad (confidencialidad y responsabilidad)

| Parte | Pregunta | Contenido |
|---|---|---|
| **1. Fuente del estímulo** | ¿Quién o qué lo provoca? | Una persona distinta del supervisor de empresa al que se envió el enlace |
| **2. Estímulo** | ¿Qué ocurre? | Intenta abrir un enlace de evaluación o de validación de horas que ya fue usado, que tiene más de 15 días de emitido o cuyo identificador fue alterado |
| **3. Artefacto** | ¿Sobre qué parte? | El mecanismo de acceso por enlace sin cuenta de CU-05 y CU-07 |
| **4. Entorno** | ¿En qué condiciones? | Operación normal |
| **5. Respuesta** | ¿Qué debe hacer el sistema? | Niega el acceso sin mostrar datos del practicante, registra el intento en la bitácora y avisa al docente asesor |
| **6. Medida de respuesta** | ¿Cómo se verifica? | **100% de los intentos rechazados; 0 datos personales mostrados; intento registrado en la bitácora con fecha, hora y dirección de origen en menos de 1 minuto** |

**Escenario redactado.** *Una persona distinta del supervisor intenta abrir, en operación normal, un enlace de evaluación ya usado, con más de 15 días de emitido o alterado. El sistema rechaza el 100% de estos intentos sin mostrar ningún dato personal, y registra cada intento en la bitácora con fecha, hora y dirección de origen en menos de 1 minuto.*

**Traza:** RN-01, RN-04, OB-06, CU-05, CU-07

## 3. Restricciones

Las restricciones del documento de visión entran como drivers sin transformación. Cada una elimina alternativas de diseño.

| ID | Restricción | Tipo | Origen | Impacto arquitectónico esperado |
|---|---|---|---|---|
| **RT-01** | Desplegar en la infraestructura que administra la Universidad | Técnica | Área de Sistemas | Descarta servicios gestionados de nube pública (funciones sin servidor, bases de datos como servicio) |
| **RT-02** | Autenticar con la cuenta institucional (inicio de sesión único) | Técnica | Administrador del SIA (seguridad de la información) | El sistema no guarda contraseñas; obliga a un adaptador hacia el proveedor de identidad institucional |
| **RT-03** | Consultar los datos académicos solo por los servicios del SIA, sin conexión directa a su base de datos | Técnica | Administrador del SIA | Obliga a un componente de integración aislado (puerto y adaptador) y a manejar sus fallas (EAC-02) |
| **RT-04** | Usar el motor de base de datos y las tecnologías del catálogo institucional | Técnica | Área de Sistemas | Limita lenguaje, framework y persistencia a lo que el Área de Sistemas soporta |
| **RN-01** | Tratar los datos personales conforme a la Ley 1581 de 2012 | Negocio | Legislación colombiana, área jurídica | Autorización por rol sobre datos personales, registro de la autorización de tratamiento y cifrado en tránsito |
| **RN-02** | Conservar actas y evidencias según la tabla de retención documental | Negocio | Gestión documental (Ley 594 de 2000) | Las actas aprobadas no se modifican ni se borran; almacenamiento de documentos con política de conservación |
| **RN-03** | El acta debe seguir el formato del reglamento de prácticas | Negocio | Consejo de Facultad | El formato del acta vive en una plantilla separada del código, para cambiarlo sin reprogramar |
| **RN-04** | No exigir a los supervisores cuenta institucional ni registro con contraseña | Negocio | Director de programa | Un segundo mecanismo de acceso: enlace de un solo uso con vencimiento (EAC-03) |
| **RN-05** | No requerir licencias comerciales de pago recurrente | Negocio | Decanatura | Descarta plataformas comerciales de flujos de trabajo o de firma por suscripción |

## 4. Preocupaciones arquitectónicas

Aspectos transversales que ningún requisito pide de forma explícita, pero que el arquitecto debe decidir para que no los resuelva cada desarrollador a su manera.

| ID | Preocupación | Qué hay que decidir | Por qué importa en este sistema |
|---|---|---|---|
| **PA-01** | Estructura general | En qué grandes bloques se divide el sistema y hacia dónde apuntan sus dependencias | La carga es baja (S-03) pero las reglas cambian (OB-05): pide modularidad, no distribución |
| **PA-02** | Autenticación y autorización | Cómo conviven dos formas de acceso y cómo se controlan los permisos de cinco roles | Inicio de sesión institucional (RT-02) y enlace sin cuenta (RN-04); roles: estudiante, docente asesor, director de programa, supervisor y administrador |
| **PA-03** | Registro y trazabilidad | Qué eventos se registran, dónde y por cuánto tiempo | Auditoría y acreditación (OB-06), datos personales (RN-01) y diagnóstico de la mesa de ayuda |
| **PA-04** | Manejo de errores y fallas de integración | Una estrategia única para fallas del SIA y del correo: reintentos, estados pendientes y mensajes al usuario | Sin ella, cada caso de uso trata distinto la caída del SIA (R-02, EAC-02) |
| **PA-05** | Migración inicial de datos | Cómo cargar las prácticas en curso desde archivos Excel con formatos distintos por docente asesor | Está en el alcance de la visión y define el primer despliegue |

## 5. Matriz de priorización

La importancia para el negocio la asigna el cliente (director de programa) y la dificultad técnica el arquitecto. Los drivers del cuadrante **alta importancia y alta dificultad** dirigen el diseño y se atienden en las primeras iteraciones.

### Alta importancia, alta dificultad: atender primero (aquí está el riesgo)

CU-01, CU-12, EAC-01, EAC-02, RT-02, RT-03, PA-02

### Alta importancia, baja dificultad: hacer ya (rápido)

CU-07, CU-09, CU-10, EAC-03, RT-01, RN-01, RN-03, RN-04, PA-01, PA-03, PA-04

### Baja importancia, baja dificultad: hacer si sobra tiempo

RT-04, RN-02, RN-05

### Baja importancia, alta dificultad: cuestionar (¿de verdad se necesita?)

PA-05
