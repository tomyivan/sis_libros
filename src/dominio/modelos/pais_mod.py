from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class PaisModelo:
    nombre: str
    fecha_creacion: Optional[datetime] = None


@dataclass
class PaisModeloDTO:
    _id: str
    nombre: str
    fecha_creacion: Optional[datetime] = None
    fecha_modificacion: Optional[datetime] = None   