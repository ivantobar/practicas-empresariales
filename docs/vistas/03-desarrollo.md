# Vista de desarrollo: componentes de la Aplicación de prácticas

Diagrama: [../diagramas/03-desarrollo.puml](../diagramas/03-desarrollo.puml) (C4, nivel 3)

Para: los desarrolladores. Responde cómo está organizado el código, qué se puede cambiar sin afectar lo demás y quién usa a quién.

## 1. Presentación principal

Abrimos el contenedor principal, la Aplicación de prácticas. Los componentes están en las capas de Clean Architecture: `infraestructura` (adaptadores de entrada y de salida), `aplicacion` (módulos con sus casos de uso y los puertos que necesitan) y `dominio` (las entidades de la vista lógica). Las dependencias solo apuntan hacia adentro: si algo de `dominio/` importa algo de `infraestructura/`, la arquitectura está rota.

En el diagrama no dibujamos todas las flechas para que se pueda leer; las que faltan están en la tabla de usos de abajo.

## 2. Catálogo de elementos

| Componente | Capa | Responsabilidad | Depende de |
|---|---|---|---|
| Controladores web | infraestructura (entrada) | Reciben las peticiones HTTPS y llaman al caso de uso que toca | Módulo Acceso y los 6 módulos de negocio |
| Módulo Postulación | aplicacion | CU-01, CU-02 y CU-03 | Módulo Reglas, transversales, puerto RepositorioPostulaciones |
| Módulo Horas | aplicacion | CU-04, CU-05 y CU-06 | Transversales, puerto RepositorioPracticas |
| Módulo Evaluación | aplicacion | CU-07 y CU-08 | Transversales, puerto RepositorioPracticas |
| Módulo Actas | aplicacion | CU-09, CU-10, CU-11, CU-13 y CU-14 | Módulo Horas, Módulo Evaluación, transversales, puertos ConsultaAcademica, AlmacenDocumentos y RepositorioActas |
| Módulo Reglas | aplicacion | CU-12, versiones de reglas y validadores de requisitos | Módulo Bitácora, puertos ConsultaAcademica y RepositorioReglas |
| Módulo Administración | aplicacion | Roles e importador de la plantilla Excel (CU-15) | Módulo Postulación, Módulo Reglas, transversales |
| Módulo Acceso | aplicacion, transversal | Sesión, roles con ámbito y enlaces de un solo uso | Módulo Bitácora, puertos ProveedorIdentidad y RepositorioAccesos |
| Módulo Pendientes | aplicacion, transversal | Registra trabajos pendientes y los ejecuta con reintentos. Define la interfaz ManejadorTrabajo | Puertos ColaPendientes y Notificador |
| Módulo Bitácora | aplicacion, transversal | Registra los eventos de auditoría | Puerto RegistroBitacora |
| Entidades del dominio | dominio | Las 17 entidades de la vista lógica y sus reglas | Nada |
| Adaptador SIA | infraestructura (salida) | Implementa ConsultaAcademica con los servicios del SIA, espera máximo 5 s | SIA (HTTPS) |
| Adaptador de identidad | infraestructura (salida) | Implementa ProveedorIdentidad con el protocolo de la Universidad | Proveedor de identidad institucional (HTTPS) |
| Adaptador de correo | infraestructura (salida) | Implementa Notificador | Servicio de correo institucional (SMTP) |
| Adaptador de base de datos | infraestructura (salida) | Implementa los repositorios, ColaPendientes y RegistroBitacora | Base de datos de prácticas (SQL) |
| Adaptador de documentos | infraestructura (salida) | Implementa AlmacenDocumentos: llena la plantilla HTML, la pasa a PDF con una librería libre y la guarda | Almacenamiento de documentos |

El Procesador de pendientes no tiene código aparte: es la misma imagen arrancada con otro punto de entrada, que solo usa el Módulo Pendientes y los manejadores que registran los módulos.

### Vista de usos (sin ciclos)

"A usa B" quiere decir que A no funciona bien sin B.

| Módulo | Usa | No puede usar |
|---|---|---|
| Postulación | Reglas, Acceso, Pendientes, Bitácora | Actas, Administración |
| Horas | Acceso, Pendientes, Bitácora | Actas |
| Evaluación | Acceso, Pendientes, Bitácora | Actas |
| Actas | Horas, Evaluación, Acceso, Pendientes, Bitácora | Administración |
| Reglas | Bitácora | Ningún otro módulo de negocio |
| Administración | Postulación, Reglas, Acceso, Bitácora | Actas |
| Acceso | Bitácora | Ningún módulo de negocio |
| Pendientes | (nada, solo sus puertos) | Ningún módulo de negocio |
| Bitácora | (nada, solo su puerto) | Ningún otro módulo |

Había un ciclo escondido: Postulación registra el trabajo "verificar en SIA" en Pendientes, y Pendientes tenía que llamar de vuelta a Postulación para hacer la verificación. Lo rompimos con inversión de dependencias: Pendientes define la interfaz ManejadorTrabajo y Postulación la implementa y la registra al arrancar (en la composición, `main`). Así Pendientes no conoce a nadie de negocio. Lo mismo hacen Evaluación y Actas para sus correos.

Como no hay ciclos, se puede entregar por incrementos: primero Bitácora, Acceso, Pendientes y Reglas; luego Postulación; luego Horas y Evaluación; y al final Actas.

## 3. Justificación

- PA-01, EAC-01, [ADR-001](../adr/ADR-001-monolito-modular.md): un módulo por tema de negocio con puertos y adaptadores. Para EAC-01 (programa nuevo con otras horas y un requisito más) se toca el Módulo Reglas (un validador nuevo) y su configuración: máximo 2 módulos, y nadie más se entera porque Postulación solo usa la interfaz de Reglas.
- [ADR-009](../adr/ADR-009-reglas-configurables-por-programa.md): validadores intercambiables dentro del Módulo Reglas.
- RT-03, EAC-02, [ADR-004](../adr/ADR-004-integracion-sia.md): el SIA queda aislado en un solo adaptador. Si toca el plan B de R-02 (exportación periódica), se cambia ese adaptador y nada más.
- PA-04, [ADR-005](../adr/ADR-005-reintentos-y-estados-pendientes.md): una sola estrategia de fallas, en el Módulo Pendientes.
- RT-02, PA-02, [ADR-006](../adr/ADR-006-autenticacion-institucional.md), [ADR-007](../adr/ADR-007-enlace-unico-supervisores.md), [ADR-008](../adr/ADR-008-autorizacion-por-roles.md): las dos formas de entrar terminan en el Módulo Acceso, y los permisos se validan en los casos de uso, no en los controladores.
- PA-03, RN-01, [ADR-012](../adr/ADR-012-bitacora-auditoria.md): Módulo Bitácora transversal.
- RN-03, RN-05, [ADR-010](../adr/ADR-010-acta-desde-plantilla.md): la conversión a PDF queda en un adaptador con librería libre.
- PA-05, [ADR-013](../adr/ADR-013-migracion-desde-excel.md): el importador vive en Administración y se puede retirar sin tocar los demás módulos.
- RT-04, [ADR-003](../adr/ADR-003-persistencia-relacional.md): la base de datos queda detrás de un solo adaptador.

## 4. Comportamiento

- [cu01-postularse](../diagramas/secuencias/cu01-postularse.puml) dentro de la aplicación: Controladores web, Módulo Postulación, Módulo Reglas, Módulo Pendientes y Adaptador SIA.
- [cu12-configurar-reglas](../diagramas/secuencias/cu12-configurar-reglas.puml): todo pasa dentro del Módulo Reglas.

## 5. Vistas relacionadas

- [Procesos](02-procesos.md): esto es el interior del contenedor Aplicación de prácticas.
- [Lógica](01-logica.md): las Entidades del dominio son las de esa vista.
- [Física](04-fisica.md): la imagen que sale de este código es la que corre en la máquina virtual.
