
from dataclasses import dataclass


@dataclass
class CalificacionModelo:
    idUsuario: str
    idLibro: str
    calificacion: int  # Valor entre 1 y 5
    

@dataclass
class CalificacionModeloDTO:
    calificacion: int

@dataclass
class FiltroCalificacionModelo:
    _id: str = None
    idUsuario: str = None
    idLibro: str = None