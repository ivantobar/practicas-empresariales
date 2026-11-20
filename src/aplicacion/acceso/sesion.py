from dataclasses import dataclass


@dataclass(frozen=True, kw_only=True)
class Sesion:
    """Quién es el usuario, qué rol tiene y cuál es su ámbito (programa) (glosario).

    Es un DTO técnico, fuera del modelo de dominio (plan de specs/001). Llega ya
    validada al caso de uso (ADR-006, DT-04): aquí no se hace login. Cada caso de
    uso valida con ella el permiso del rol antes de ejecutar (ADR-008).
    Ejemplo: usuario "E-1001", rol "estudiante", ámbito "Ingeniería de Sistemas".
    """

    usuario: str
    rol: str
    ambito: str
