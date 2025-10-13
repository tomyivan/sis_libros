from abc import ABC, abstractmethod
from typing import List
class RecomendacionPuerto(ABC):
   
    @abstractmethod
    def obtenerRecomendacionRedis(self, idLibro: str) -> List[str]:
        pass

    @abstractmethod
    def guardarRecomendacionRedis(self, idLibro: str, recomendaciones: List[str]) -> None:
        pass