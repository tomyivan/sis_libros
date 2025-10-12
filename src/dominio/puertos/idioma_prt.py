from abc import ABC, abstractmethod
from typing import List
from src.dominio.modelos.idioma_mod import IdiomaModelo, IdiomaModeloDTO


class IdiomaPuerto(ABC):
    @abstractmethod
    def crearIdioma(self, idioma: IdiomaModelo) -> str:
        pass

    @abstractmethod
    def obtenerIdioma(self, idioma_id: str) -> IdiomaModeloDTO:
        pass

    @abstractmethod
    def obtenerIdiomas(self) -> List[IdiomaModeloDTO]:
        pass

    @abstractmethod
    def actualizarIdioma(self, idioma: IdiomaModelo, idioma_id: str) -> int:
        pass

    @abstractmethod
    def eliminarIdioma(self, idioma_id: str) -> bool:
        pass
