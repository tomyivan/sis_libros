from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class CategoriaModelo:
    nombre: str
    descripcion: Optional[str] = None
    activo: bool = True
    fecha_creacion: datetime = None
    fecha_modificacion: Optional[datetime] = None


@dataclass
class CategoriaModeloDTO:
    _id: str
    nombre: str
    descripcion: Optional[str]
    activo: bool
    fecha_creacion: datetime
    fecha_modificacion: Optional[datetime] = None
