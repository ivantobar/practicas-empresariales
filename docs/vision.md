# Documento de visión: Sistema de Gestión de Prácticas Empresariales

> **Enunciado.** *La Facultad de Ingenierías quiere un sistema para gestionar las prácticas empresariales de los estudiantes: postulación, asignación de tutor, seguimiento de horas, evaluación de la empresa y generación del acta final. Hoy todo se maneja en Excel y correo electrónico. Hay 500 estudiantes en práctica al año y 50 tutores.*

## 1. Problema u oportunidad

Hoy la Facultad gestiona las prácticas empresariales de 500 estudiantes al año y 50 docentes asesores de práctica con hojas de Excel y correo electrónico, sin una fuente única de información: cada docente asesor lleva sus archivos a su manera, las horas se consolidan a mano, las evaluaciones de las empresas llegan sin control de plazos y el acta final se arma reuniendo datos dispersos. La situación es insatisfactoria porque el director de programa no sabe en tiempo real qué estudiantes van atrasados, el cierre de las prácticas se demora (y con él el grado), las actas salen con errores de transcripción y atender una auditoría o un proceso de acreditación exige reconstruir la información a mano.

## 2. Objetivos de negocio

| ID | Objetivo de negocio (qué gana la Facultad, medible) | Atributo de calidad que implica |
|---|---|---|
| **OB-01** | Reducir a máximo 5 días hábiles el tiempo entre el cumplimiento de las horas del estudiante y la entrega de su acta final, en el 90% de las prácticas del primer periodo de operación. | Interoperabilidad (datos académicos sin retranscribir) |
| **OB-02** | Recibir dentro del plazo reglamentario al menos el 90% de las evaluaciones que las empresas hacen de sus practicantes, durante el primer año de operación. | Capacidad de interacción para usuarios externos |
| **OB-03** | Reducir en 50% las horas semanales que cada docente asesor de práctica dedica a consolidar información, medidas por encuesta antes y después del primer periodo de operación. | Capacidad de interacción, eficiencia |
| **OB-04** | Bajar a menos del 1% las actas que se deben reemitir por errores en los datos, durante el primer año de operación. | Seguridad (integridad de los datos) |
| **OB-05** | Aplicar un cambio del reglamento o las reglas de un programa nuevo desde el periodo académico siguiente a su aprobación, sin suspender la gestión de las prácticas en curso. | Mantenibilidad (modificabilidad) |
| **OB-06** | Entregar a auditoría o acreditación el consolidado de prácticas de cualquier periodo en máximo 1 día hábil. | Seguridad (trazabilidad) |

## 3. Alcance

### Qué SÍ incluye

- Postulación del estudiante a la práctica empresarial ante la Facultad, con verificación de sus requisitos académicos
- Asignación del docente asesor de práctica por parte del director de programa, según la carga de cada docente asesor
- Registro y validación de las horas de práctica empresarial
- Evaluación del practicante por parte de la empresa, con plazos y recordatorios
- Acta final de la práctica en el formato oficial, seguimiento del estado de cada práctica y migración de las prácticas empresariales en curso

### Qué NO incluye

- Bolsa de empleo o búsqueda de la plaza de práctica en la empresa
- Gestión y firma de los convenios de práctica con las empresas (solo se consulta si están vigentes)
- Afiliación a ARL, pagos o apoyos de sostenimiento del practicante
- Evaluación de la empresa por parte del estudiante practicante
- Firma digital certificada del acta, carga automática de la nota de práctica en el SIA e histórico de prácticas de años anteriores

## 4. Stakeholders

| Nombre / rol | Tipo | Preocupaciones (y atributo de calidad que implican) | Poder / interés |
|---|---|---|---|
| **Decanatura y Consejo de Facultad (patrocinador)** | Negocio | Costo, plazo de puesta en marcha e indicadores para acreditación (costo, tiempo de entrega) | Alto / alto: gestionar de cerca |
| **Director de programa (coordinador de práctica, cliente)** | Negocio | Conocer el estado de todas las prácticas y cerrarlas a tiempo (adecuación funcional) | Alto / alto: gestionar de cerca |
| **Docentes asesores de práctica (50)** | Negocio | Revisar horas y avances sin trabajo adicional (capacidad de interacción, eficiencia) | Bajo / alto: mantener informado |
| **Estudiantes en práctica (500 al año)** | Negocio | Saber en qué va su trámite y registrar horas desde el celular (capacidad de interacción) | Bajo / alto: mantener informado |
| **Supervisores de empresa** | Negocio (externo) | Evaluar y validar horas en pocos minutos, sin crear cuentas (capacidad de interacción) | Alto / bajo: mantener satisfecho |
| **Área jurídica y gestión documental** | Negocio | Protección de datos personales, validez y conservación del acta (seguridad, auditabilidad) | Alto / bajo: mantener satisfecho |
| **Área de Sistemas (infraestructura)** | Técnico | Desplegar, monitorear y respaldar el sistema con su personal (operabilidad, recuperabilidad) | Alto / alto: gestionar de cerca |
| **Administrador del Sistema de Información Académica (SIA), responsable también de la seguridad de la información** | Técnico | Integración por los servicios del SIA, sin conexión directa a su base de datos (interoperabilidad); autenticación institucional, permisos por rol y registro de accesos (seguridad) | Alto / bajo: mantener satisfecho |
| **Desarrolladores que mantendrán el sistema** | Técnico | Cambiar reglas del reglamento sin romper lo existente (mantenibilidad, testabilidad) | Bajo / alto: mantener informado |
| **Mesa de ayuda (soporte)** | Técnico | Diagnosticar por qué un usuario no puede postularse o registrar horas (facilidad de análisis) | Bajo / bajo: monitorear |

## 5. Restricciones

| ID | Restricción (decisión ya tomada) | Quién la impone | Por qué |
|---|---|---|---|
| **RT-01** | Debe desplegarse en la infraestructura que administra la Universidad | Área de Sistemas | Política de control, respaldo y soporte de los sistemas institucionales |
| **RT-02** | Debe autenticar a estudiantes, docentes asesores y personal con la cuenta institucional (inicio de sesión único) | Administrador del SIA (responsable de la seguridad de la información) | Política institucional de gestión de identidades |
| **RT-03** | Debe consultar los datos académicos solo a través de los servicios que el SIA expone para otros sistemas, sin conectarse directamente a su base de datos | Administrador del SIA | Una conexión directa ata el sistema a la estructura interna del SIA, puede afectar su rendimiento y evade sus controles de seguridad |
| **RT-04** | Debe usar el motor de base de datos y las tecnologías del catálogo institucional | Área de Sistemas | Su personal solo da soporte a ese catálogo |
| **RN-01** | Debe tratar los datos personales conforme a la Ley 1581 de 2012 y el Decreto 1377 de 2013 | Legislación colombiana, aplicada por el área jurídica | Obligación legal sobre autorización, finalidad y acceso a datos personales |
| **RN-02** | Debe conservar actas y evidencias según la tabla de retención documental | Gestión documental (Ley 594 de 2000) | Obligación legal archivística |
| **RN-03** | El acta final debe seguir el formato y contenido del reglamento de prácticas | Consejo de Facultad | El acta es un documento académico oficial |
| **RN-04** | No puede exigir a los supervisores de empresa una cuenta institucional ni un registro con contraseña | Director de programa | Las empresas participan de forma voluntaria; un trámite pesado pone en riesgo OB-02 |
| **RN-05** | No puede requerir licencias comerciales de pago recurrente | Decanatura | Presupuesto de funcionamiento disponible |

## 6. Supuestos y riesgos iniciales

| ID | Lo que el enunciado no dice | Supuesto adoptado | Validar con |
|---|---|---|---|
| **S-01** | Qué es "evaluación de la empresa" | La empresa evalúa el desempeño del practicante y esa nota alimenta el acta | Director de programa |
| **S-02** | Contra qué se verifican los requisitos académicos del estudiante | Contra el SIA, sistema que administra el administrador del SIA y que ofrece servicios para que otros sistemas consulten sus datos (RT-03) | Administrador del SIA |
| **S-03** | Cuál es la carga real | Cada práctica dura de 4 a 6 meses: de las 500 anuales hay entre 170 y 250 activas a la vez, con decenas de usuarios concurrentes; no justifica una arquitectura distribuida | Director de programa |
| **S-04** | Ante quién se postula el estudiante | Ante la Facultad, con la plaza ya conseguida | Director de programa |
| **S-05** | Quién valida las horas | El estudiante las registra cada semana, el supervisor las valida y el docente asesor las revisa | Director de programa |
| **S-06** | Qué firmas exige el acta | Basta la aprobación electrónica trazable del docente asesor y del director de programa | Área jurídica |
| **S-07** | Si todos los programas usan las mismas reglas | Requisitos y horas mínimas varían entre los programas de la Facultad | Directores de programa |
| **S-08** | Cómo está hoy el proceso en cifras | No hay indicadores; las líneas base se reconstruyen con correos y archivos del último año | Director de programa |
| **S-09** | Políticas institucionales vigentes | RT-01 a RT-04 y RN-05 están vigentes; se confirman con su dueño en la primera semana | Área de Sistemas, Decanatura |

| ID | Riesgo inicial | Objetivo afectado | Mitigación |
|---|---|---|---|
| **R-01** | Los supervisores no responden a tiempo | OB-02, OB-01 | Acceso por enlace sin cuenta (RN-04), formulario corto y recordatorios con copia al docente asesor |
| **R-02** | El SIA no ofrece servicios de consulta, o fallan con frecuencia, y no se pueden verificar a tiempo los requisitos del estudiante | OB-01 | Confirmar con el administrador del SIA en la primera semana qué servicios existen; si no hay, acordar una exportación periódica de datos |
| **R-03** | Se exige firma digital certificada del acta (S-06) | OB-01 | Validar S-06 con el área jurídica antes de diseñar |
| **R-04** | Sobredimensionar la solución para una carga que no existe | Costo | Justificar cada decisión con S-03 y RT-04 |
