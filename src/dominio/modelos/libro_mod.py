# Aquí se define la entidad Libro
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

@dataclass
class LibroModelo:
    titulo: str
    autor: str
    genero: List[str]
    año_publicacion: int
    editorial: str
    isbn: str
    paginas: int
    idioma: str
    descripcion: str
    origen_pais: str
    disponible: bool = True
    fecha_creacion: datetime = None
    fecha_modificacion: Optional[datetime] = None
    portada_url: Optional[str] = None
    tags: Optional[List[str]] = None

@dataclass
class LibroModeloDTO:
    _id: str
    titulo: str
    autor: str
    genero: List[str]
    año_publicacion: int
    editorial: str
    isbn: str
    paginas: int
    idioma: str
    descripcion: str
    origen_pais: str
    disponible: bool
    fecha_creacion: datetime
    fecha_modificacion: Optional[datetime] = None
    portada_url: Optional[str] = None
    tags: Optional[List[str]] = None

@dataclass
class FiltroLibroModelo:
    _id: str = None
    titulo: str = None
    autor: str = None
    genero: str = None
    año_min: int = None
    año_max: int = None
    editorial: str = None
    isbn: str = None
    idioma: str = None
    origen_pais: str = None
    disponible: bool = None
    tags: List[str] = None