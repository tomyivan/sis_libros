from src.dominio.modelos import libro_mod
from src.dominio.puertos import libro_prt
from typing import List

class ObtenerLibroServicio:
    def __init__(self, repositorio: libro_prt.LibroPuerto):
        self.repositorio = repositorio

    def obtenerLibro(self, libro_id: str) -> libro_mod.LibroModeloDTO:
        """Obtener un libro por ID"""
        filtro = libro_mod.FiltroLibroModelo(_id=libro_id)
        return self.repositorio.obtenerLibro(filtro)
        
    def obtenerLibros(self, filtro: libro_mod.FiltroLibroModelo = None) -> List[libro_mod.LibroModeloDTO]:
        """Obtener lista de libros con filtros opcionales"""
        if filtro is None:
            filtro = libro_mod.FiltroLibroModelo(disponible=True)
        return self.repositorio.obtenerLibros(filtro)
    
    def obtenerLibrosPorGenero(self, genero: str) -> List[libro_mod.LibroModeloDTO]:
        """Obtener libros por género"""
        return self.repositorio.obtenerLibrosPorGenero(genero)
    
    def obtenerLibrosPorAutor(self, autor: str) -> List[libro_mod.LibroModeloDTO]:
        """Obtener libros por autor"""
        return self.repositorio.obtenerLibrosPorAutor(autor)
    
    def buscarLibros(self, texto_busqueda: str) -> List[libro_mod.LibroModeloDTO]:
        """Buscar libros por texto"""
        return self.repositorio.buscarLibrosPorTexto(texto_busqueda)
    
    def obtenerLibrosPorAño(self, año_min: int = None, año_max: int = None) -> List[libro_mod.LibroModeloDTO]:
        """Obtener libros por rango de años"""
        filtro = libro_mod.FiltroLibroModelo(
            año_min=año_min, 
            año_max=año_max, 
            disponible=True
        )
        return self.repositorio.obtenerLibros(filtro)
    
    def obtenerLibrosMejorCalificados(self, limite: int = 10) -> List[libro_mod.LibroModeloDTO]:
        """Obtener libros mejor calificados"""
        filtro = libro_mod.FiltroLibroModelo(calificacion_min=4.0, disponible=True)
        libros = self.repositorio.obtenerLibros(filtro)
        # Ordenar por calificación y limitar resultados
        return sorted(libros, key=lambda x: x.calificacion_promedio, reverse=True)[:limite]