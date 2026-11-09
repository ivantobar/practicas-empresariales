# Vista física: despliegue

Diagrama: [../diagramas/04-fisica.puml](../diagramas/04-fisica.puml) (C4, despliegue)

Para: el Área de Sistemas. Responde qué se instala, en qué servidores y por dónde viaja cada conexión. Aquí es donde se verifica RT-01.

## 1. Presentación principal

Todos los nodos están dentro del centro de datos de la Universidad. Desde internet solo entra HTTPS por el proxy institucional.

## 2. Catálogo de elementos

| Nodo | Contenedores que aloja | Características | Conexiones |
|---|---|---|---|
| Dispositivo del usuario | Navegador web | Celular o computador, fuera de la Universidad o dentro | Proxy institucional (HTTPS 443), Proveedor de identidad institucional (HTTPS) |
| Proxy institucional | Terminación HTTPS | Lo administra el Área de Sistemas, con certificado institucional; no deja pasar HTTP plano | Navegadores (HTTPS), Aplicación de prácticas (red interna) |
| Máquina virtual de prácticas | Aplicación de prácticas, Procesador de pendientes, Almacenamiento de documentos | Linux con Docker Compose. Los dos contenedores salen de la misma imagen con versión; el almacenamiento es un volumen con respaldo | Base de datos de prácticas (SQL), SIA (HTTPS), Proveedor de identidad (HTTPS), correo (SMTP), todo por red interna |
| Servidor de base de datos institucional | Base de datos de prácticas | Motor relacional libre del catálogo, respaldado por el Área de Sistemas; solo se llega desde la red interna | Aplicación y Procesador (SQL) |
| Servidores del SIA | SIA | Los administra el administrador del SIA; solo exponemos el uso de sus servicios | Aplicación y Procesador (HTTPS) |
| Servidor de identidad | Proveedor de identidad institucional | Lo administra el Área de Sistemas | Navegadores y Aplicación (HTTPS) |
| Servidor de correo | Servicio de correo institucional | Envía desde el dominio institucional (menos riesgo de spam, ADR-007) | Procesador (SMTP) |

El ambiente de pruebas tiene la misma forma en otra máquina virtual, con un simulador del SIA y del proveedor de identidad.

## 3. Justificación

- RT-01, [ADR-002](../adr/ADR-002-despliegue-institucional.md): todos los nodos están en la infraestructura de la Universidad, no hay nube pública. Docker Compose en una sola máquina virtual, sin Kubernetes (R-04).
- RN-01 (Ley 1581): todo lo que viene de afuera es HTTPS y los datos personales no salen del centro de datos. La base de datos no se ve desde internet.
- RT-04, RN-05, [ADR-003](../adr/ADR-003-persistencia-relacional.md): servidor de base de datos del catálogo, sin licencias.
- RN-02, [ADR-011](../adr/ADR-011-aprobacion-trazable-acta-inmutable.md): el volumen de documentos tiene respaldo y la política de conservación de la tabla de retención.
- EAC-02, [ADR-005](../adr/ADR-005-reintentos-y-estados-pendientes.md): los trabajos pendientes están en la base de datos, no en memoria, así que si se reinicia la máquina virtual no se pierde ninguno.
- RT-02, RT-03: el Proveedor de identidad y el SIA corren en sus propios servidores, nosotros solo los consumimos.
- Lo que aceptamos (ADR-002): hay una sola máquina virtual, si se cae el sistema queda fuera hasta que se recupere. Ningún driver pide alta disponibilidad.

## 4. Comportamiento

La secuencia de [cu01-postularse](../diagramas/secuencias/cu01-postularse.puml) cruza nodos: el estudiante entra por el proxy, la postulación se guarda en el servidor de base de datos y el Procesador consulta al SIA por la red interna. En [cu07-evaluar-practicante](../diagramas/secuencias/cu07-evaluar-practicante.puml) el supervisor entra desde internet por el mismo proxy.

## 5. Vistas relacionadas

- [Procesos](02-procesos.md): cada contenedor de esa vista aparece en un nodo de esta.
- [Contexto](../contexto.md): cada sistema externo aparece con su protocolo.
