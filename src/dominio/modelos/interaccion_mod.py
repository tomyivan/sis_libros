from dataclasses import dataclass
from datetime import datetime


@dataclass
class ComentarioModelo:
    id_usuario: str
    id_libro: str
    texto: str
    fecha: datetime


@dataclass
class CalificacionModelo:
    id_usuario: str
    id_libro: str
    calificacion: float
    fecha: datetime


@dataclass
class VisualizacionModelo:
    id_usuario: str
    id_libro: str
    fecha: datetime
