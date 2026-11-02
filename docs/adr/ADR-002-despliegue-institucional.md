# ADR-002: Despliegue con contenedores en los servidores de la Universidad

## Estado

Aceptado (2026-11-02)

## Contexto

[RT-01](../drivers.md#3-restricciones) obliga a desplegar en la infraestructura de la Universidad, así que la nube pública queda descartada. El dónde ya está decidido; lo que falta decidir es cómo empaquetamos y desplegamos el sistema.

También hay que tener en cuenta que [RN-01](../drivers.md#3-restricciones) pide cifrar los datos personales en tránsito, que [RN-05](../drivers.md#3-restricciones) no deja usar licencias pagas, y que con [EAC-01](../drivers.md#eac-01-mantenibilidad-modificabilidad) hay que poder desplegar cambios con el sistema funcionando. El Área de Sistemas es quien lo va a operar.

## Alternativas consideradas

1. **Instalar a mano en una máquina virtual.** No hay que aprender nada nuevo, pero cada despliegue depende de pasos manuales, es difícil tener el mismo entorno en pruebas y producción, y devolverse si algo sale mal es lento.
2. **Contenedores con Docker y Docker Compose en máquinas virtuales de la Universidad.** La aplicación queda en una imagen con versión, la misma imagen corre en todos los ambientes, y volver a la versión anterior es cambiar la etiqueta. Es software libre. La desventaja es que el Área de Sistemas tiene que saber manejar contenedores.
3. **Kubernetes.** Da autoescalado y alta disponibilidad, pero la carga de [S-03](../vision.md#6-supuestos-y-riesgos-iniciales) no lo necesita y operar un clúster es caro. Sería sobredimensionar ([R-04](../vision.md#6-supuestos-y-riesgos-iniciales)).

## Decisión

Elegimos la opción 2: imagen de contenedor con Docker Compose en una máquina virtual de la Universidad, detrás del proxy institucional con HTTPS obligatorio (por RN-01). Cumple RT-01 y deja los despliegues repetibles y fáciles de revertir sin meternos en la complejidad de Kubernetes.

## Consecuencias

**Positivas:** la misma imagen pasa de pruebas a producción; devolverse a una versión anterior toma minutos; todo el tráfico va cifrado.

**Negativas:** el Área de Sistemas tiene que aprender a operar contenedores si no lo hace hoy. Hay una sola instancia en una sola máquina, entonces si se cae el servidor el sistema queda fuera hasta que se recupere; lo aceptamos porque ningún driver pide alta disponibilidad. Cada actualización implica un corte corto, que se hace fuera de horas pico.

**Riesgos:** que el Área de Sistemas no tenga experiencia con contenedores. Lo confirmamos la primera semana (S-09); si no la tienen, se hace un manual de operación, y si ni así funciona, se instala directo en la máquina virtual con un ADR nuevo.
