# ADR-006: Login con el proveedor de identidad institucional (OpenID Connect o SAML)

## Estado

Aceptado (2026-11-02)

## Contexto

[RT-02](../drivers.md#3-restricciones) obliga a que estudiantes, docentes y personal entren con la cuenta institucional (inicio de sesión único), así que el sistema no debe guardar contraseñas. Usar la cuenta institucional ya está decidido; aquí decidimos cómo nos conectamos.

Esto hace parte de [PA-02](../drivers.md#4-preocupaciones-arquitectónicas) (cómo se autentican los roles internos), y el administrador del SIA, que es el responsable de seguridad, pide autenticación institucional y registro de accesos ([stakeholders](../vision.md#4-stakeholders)).

## Alternativas consideradas

1. **Consultar el directorio (LDAP) con el usuario y la contraseña que se escriben en nuestro formulario.** Es fácil si el directorio está disponible, pero la contraseña institucional pasaría por nuestro sistema, y si tenemos un fallo de seguridad se expone. Tampoco es un inicio de sesión único de verdad.
2. **Federación con el proveedor de identidad institucional usando un estándar (OpenID Connect, o SAML si es lo único que hay).** El usuario se autentica en la página de la Universidad y nosotros solo recibimos una respuesta firmada con su identidad; nunca vemos la contraseña. Se aprovechan las políticas que ya tiene la Universidad (doble factor, bloqueos), y hay librerías libres para ambos. La desventaja es que dependemos de que la Universidad registre el sistema, y si su proveedor se cae nadie interno puede entrar.

(No consideramos cuentas propias con contraseña porque RT-02 las descarta.)

## Decisión

Elegimos la opción 2. El sistema se registra como aplicación cliente del proveedor institucional y valida la respuesta firmada. El protocolo depende de lo que tenga la Universidad, y queda aislado en un adaptador ([ADR-001](ADR-001-monolito-modular.md)). Los roles no vienen del proveedor sino que se manejan dentro del sistema ([ADR-008](ADR-008-autorizacion-por-roles.md)).

## Consecuencias

**Positivas:** no guardamos ni vemos contraseñas; la gente entra con la cuenta que ya usa; cuando alguien se va de la Universidad, su acceso se desactiva solo; si cambia el protocolo o el proveedor, solo se toca el adaptador.

**Negativas:** si el proveedor institucional se cae, nadie interno puede entrar (aunque eso le pasa igual a los demás sistemas de la Universidad). Hay que hacer un trámite con el Área de Sistemas para registrar la aplicación y tener un ambiente de pruebas. Y para desarrollar necesitamos un proveedor de identidad simulado.

**Riesgos:** que la Universidad no tenga ningún protocolo estándar. Lo confirmamos la primera semana (S-09). Si solo hay LDAP, usaríamos la opción 1 con un ADR nuevo que deje escrito el riesgo de seguridad que se acepta.
