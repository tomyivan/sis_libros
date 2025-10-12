from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class IdiomaModelo:
    nombre: str
    fecha_creacion: Optional[datetime] = None


@dataclass
class IdiomaModeloDTO:
    _id: str
    nombre: str
    fecha_creacion: Optional[datetime] = None
