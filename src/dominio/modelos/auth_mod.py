
from dataclasses import dataclass


@dataclass
class AuthModelo:
    token: str
    rol: str
    idUsuario: str
    usuario: str
    alias: str


