from abc import ABC, abstractmethod
from typing import List
from src.dominio.modelos.calificacion_mod import CalificacionModelo, CalificacionModeloDTO, FiltroCalificacionModelo

class CalificacionPuerto(ABC):
    @abstractmethod
    def crearCalificacion(self, calificacion: CalificacionModelo) -> str:
        pass

    @abstractmethod
    def obtenerCalificacion(self, filtro: FiltroCalificacionModelo) -> CalificacionModeloDTO:
        pass

    @abstractmethod
    def actualizarCalificacion(self, calificacion: CalificacionModelo, calificacionId: str) -> int:
        pass

    @abstractmethod
    def eliminarCalificacion(self, calificacionId: str) -> bool:
        pass
