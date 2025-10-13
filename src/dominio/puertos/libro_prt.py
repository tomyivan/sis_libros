# Se define la interfaz para las operaciones relacionadas con libros.
from abc import ABC, abstractmethod
from src.dominio.modelos.libro_mod import LibroModelo, LibroModeloDTO, FiltroLibroModelo, LibroInformacion
from typing import List

class LibroPuerto(ABC):

    @abstractmethod
    def obtenerLibroInfo(self, idLibro: str) -> LibroInformacion:
        """Obtener información detallada de un libro por su ID, incluyendo estadísticas agregadas."""
        pass

    @abstractmethod
    def obtenerLibro(self, filtro: FiltroLibroModelo) -> LibroModeloDTO:
        """Obtener un libro específico por filtro"""
        pass

    @abstractmethod
    def obtenerLibros(self, filtro: FiltroLibroModelo, offset: int = None, limit: int = None) -> List[LibroModeloDTO]:
        """Obtener lista de libros según filtros con soporte opcional de paginación (offset/limit)."""
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
    
