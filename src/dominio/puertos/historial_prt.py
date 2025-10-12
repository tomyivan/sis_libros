import src.dominio.modelos.historial_mod as historial_mod
from typing import List
from abc import ABC, abstractmethod

class HistorialPuerto(ABC):
    @abstractmethod
    def registrarHistorial(self, historial: historial_mod.HistorialModelo) -> str:
        pass

    @abstractmethod
    def obtenerHistorial(self, idUsuario: str, libro: str = "") -> List[historial_mod.HistorialModeloDTO]:
        pass