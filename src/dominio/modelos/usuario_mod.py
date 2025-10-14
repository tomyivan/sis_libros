# Aqui se define la entidad Usuario
from dataclasses import dataclass
from datetime import datetime

@dataclass  
class UsuarioModelo:
    nombre: str
    apellido: str
    alias: str
    email: str
    pais: str
    edad: int
    password_hash: str
    fecha_creacion: datetime
    activo: bool = True
    fecha_modificacion: datetime = None
    rol: str = "usuario"  # rol por defecto

@dataclass
class UsuarioModeloDTO:
    _id: str
    nombre: str
    apellido: str
    alias: str
    email: str
    pais: str
    edad: int
    fecha_creacion: datetime
    fecha_modificacion: datetime = None
    password_hash: str = None
    rol: str = "usuario"

@dataclass
class FiltroUsuarioModelo:
    _id: str = None
    alias: str = None
    pais: str = None
    edad_minima: int = None
    edad_maxima: int = None
    activo: bool = None