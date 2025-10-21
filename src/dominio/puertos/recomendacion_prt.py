from abc import ABC, abstractmethod
from typing import List

from src.dominio.modelos import recomendacion_mod
class RecomendacionPuerto(ABC):
   
    # @abstractmethod
    # def obtenerRecomendacionRedis(self, idLibro: str) -> List[str]:
    #     pass

    @abstractmethod
    def guardarRecomendacionRedis(self, idLibro: str, recomendaciones: List[str]) -> None:
        pass

    @abstractmethod
    def obtenerRecomendacionPorLibro(self, idLibro: str) -> List[recomendacion_mod.RecomendacionModeloDTO]:
        pass