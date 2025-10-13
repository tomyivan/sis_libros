
from dataclasses import dataclass


@dataclass
class ComentarioModelo:
    idUsuario: str
    idLibro: str
    comentario: str
    

@dataclass
class ComentarioModeloDTO:
    comentario: str

@dataclass
class FiltroComentarioModelo:
    _id: str = None
    idUsuario: str = None
    idLibro: str = None