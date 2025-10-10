from abc import ABC, abstractmethod
from typing import List
from src.dominio.modelos.categoria_mod import CategoriaModelo, CategoriaModeloDTO

class CategoriaPuerto(ABC):
    @abstractmethod
    def crearCategoria(self, categoria: CategoriaModelo) -> str:
        pass

    @abstractmethod
    def obtenerCategoria(self, categoria_id: str) -> CategoriaModeloDTO:
        pass

    @abstractmethod
    def obtenerCategorias(self) -> List[CategoriaModeloDTO]:
        pass

    @abstractmethod
    def actualizarCategoria(self, categoria: CategoriaModelo, categoria_id: str) -> int:
        pass

    @abstractmethod
    def eliminarCategoria(self, categoria_id: str) -> bool:
        pass
