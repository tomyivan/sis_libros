from abc import ABC, abstractmethod
from typing import List
from src.dominio.modelos.pais_mod import PaisModelo, PaisModeloDTO


class PaisPuerto(ABC):
    @abstractmethod
    def crearPais(self, pais: PaisModelo) -> str:
        pass

    @abstractmethod
    def obtenerPais(self, pais_id: str) -> PaisModeloDTO:
        pass

    @abstractmethod
    def obtenerPaises(self) -> List[PaisModeloDTO]:
        pass

    @abstractmethod
    def actualizarPais(self, pais: PaisModelo, pais_id: str) -> int:
        pass

    @abstractmethod
    def eliminarPais(self, pais_id: str) -> bool:
        pass
