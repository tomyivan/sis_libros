from abc import ABC, abstractmethod
from typing import List, Optional
from src.dominio.modelos.genero_mod import GeneroModelo, GeneroModeloDTO


class GeneroRepositorio(ABC):
    @abstractmethod
    def obtener_generos(self) -> List[GeneroModeloDTO]:
        pass

    @abstractmethod
    def obtener_genero(self, id: str) -> Optional[GeneroModeloDTO]:
        pass

    @abstractmethod
    def crear_genero(self, genero: GeneroModelo) -> str:
        pass

    @abstractmethod
    def actualizar_genero(self, id: str, datos: dict) -> bool:
        pass

    @abstractmethod
    def eliminar_genero(self, id: str) -> bool:
        pass
