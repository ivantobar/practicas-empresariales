# Contexto del sistema

Diagrama: [diagramas/contexto.puml](diagramas/contexto.puml) (C4, nivel 1)

El contexto no es una de las vistas de 4+1, es el marco de todas. Aquí el sistema es una caja negra: solo mostramos quién lo usa y con qué sistemas habla, nada de lo que tiene adentro.

## 1. Presentación principal

El diagrama tiene 5 tipos de persona, el sistema en el centro y 3 sistemas externos. Toda flecha dice qué se hace y por qué protocolo. Para verlo en VS Code se usa la extensión PlantUML (Alt+D).

## 2. Catálogo de elementos

| Elemento | Tipo | Rol o responsabilidad | Interacción con el sistema |
|---|---|---|---|
| Estudiante | Persona | Se postula, registra sus horas cada semana y consulta su trámite | Navegador (HTTPS), con cuenta institucional |
| Docente asesor | Persona | Revisa horas y avance, genera y aprueba el acta | Navegador (HTTPS), con cuenta institucional |
| Director de programa | Persona | Aprueba postulaciones, asigna docentes, configura las reglas de su programa y aprueba el acta | Navegador (HTTPS), con cuenta institucional |
| Supervisor de empresa | Persona externa | Valida las horas y evalúa al practicante | Navegador (HTTPS), con enlace de un solo uso, sin cuenta (RN-04) |
| Administrador del sistema | Persona | Administra roles y carga la migración desde Excel | Navegador (HTTPS), con cuenta institucional |
| Sistema de Gestión de Prácticas Empresariales | Sistema en alcance | Gestiona la práctica desde la postulación hasta el acta final | Con todos los demás elementos |
| SIA | Sistema externo | Fuente de los datos académicos del estudiante, lo administra el administrador del SIA | Sus servicios de consulta (HTTPS), nunca su base de datos (RT-03) |
| Proveedor de identidad institucional | Sistema externo | Autentica con la cuenta institucional (inicio de sesión único) | Protocolo estándar sobre HTTPS (RT-02) |
| Servicio de correo institucional | Sistema externo | Entrega los enlaces a supervisores, los recordatorios y los avisos | SMTP |

## 3. Justificación

- Los 5 casos de uso primarios ([drivers.md](drivers.md#1-casos-de-uso-y-casos-de-uso-primarios)) definen los actores: CU-01 el estudiante, CU-07 el supervisor, CU-09 y CU-10 el docente y el director, CU-12 el director. El administrador sale de CU-15 y de [ADR-013](adr/ADR-013-migracion-desde-excel.md).
- RT-03: el SIA aparece como sistema aparte porque no lo controlamos y solo lo usamos por sus servicios ([ADR-004](adr/ADR-004-integracion-sia.md)).
- RT-02: la autenticación la hace un sistema externo; nosotros no guardamos contraseñas ([ADR-006](adr/ADR-006-autenticacion-institucional.md)).
- RN-04: el supervisor está marcado como externo y llega por un enlace que le llega al correo ([ADR-007](adr/ADR-007-enlace-unico-supervisores.md)).
- Stakeholder: el administrador del SIA necesita ver qué consultamos y por qué canal; el Área de Sistemas necesita saber con qué servicios institucionales nos conectamos.

## 4. Comportamiento

Aquí empiezan los escenarios del +1 ([drivers.md, sección 6](drivers.md#6-escenarios-1)): el estudiante inicia CU-01 y el SIA es el que puede fallar (EAC-02); el supervisor entra por el enlace en CU-07 (EAC-03).

## 5. Vistas relacionadas

- [Procesos](vistas/02-procesos.md): qué contenedor habla con cada sistema externo.
- [Física](vistas/04-fisica.md): por qué red sale cada conexión.
- [Lógica](vistas/01-logica.md): los actores aparecen como entidades (Estudiante, DocenteAsesor, DirectorPrograma, SupervisorEmpresa).
