from dataclasses import dataclass

@dataclass
class HistorialModelo:
    idUsuario: str
    textoBusqueda: str

@dataclass
class HistorialModeloDTO:
    idUsuario: str
    textoBusqueda: str