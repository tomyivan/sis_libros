# Se define la interfaz para las operaciones relacionadas con libros.
from abc import ABC, abstractmethod
from src.dominio.modelos.libro_mod import LibroModelo, LibroModeloDTO, FiltroLibroModelo
from typing import List

class LibroPuerto(ABC):
    @abstractmethod
    def obtenerLibro(self, filtro: FiltroLibroModelo) -> LibroModeloDTO:
        """Obtener un libro específico por filtro"""
        pass

    @abstractmethod
    def obtenerLibros(self, filtro: FiltroLibroModelo) -> List[LibroModeloDTO]:
        """Obtener lista de libros según filtros"""
        pass

    @abstractmethod
    def crearLibro(self, libro: LibroModelo) -> str:
        """Crear un nuevo libro"""
        pass

    @abstractmethod
    def actualizarLibro(self, libro: LibroModelo) -> int:
        """Actualizar un libro existente"""
        pass

    @abstractmethod
    def eliminarLibro(self, libroId: str) -> bool:
        """Eliminar/desactivar un libro"""
        pass
    
    @abstractmethod
    def buscarLibrosPorTexto(self, texto: str) -> List[LibroModeloDTO]:
        """Buscar libros por texto en título, autor o descripción"""
        pass
    
    @abstractmethod
    def obtenerLibrosPorGenero(self, genero: str) -> List[LibroModeloDTO]:
        """Obtener libros por género específico"""
        pass
    
    @abstractmethod
    def obtenerLibrosPorAutor(self, autor: str) -> List[LibroModeloDTO]:
        """Obtener libros por autor específico"""
        pass