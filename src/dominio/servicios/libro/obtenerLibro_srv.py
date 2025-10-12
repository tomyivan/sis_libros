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
        
    def obtenerLibros(self, filtro: libro_mod.FiltroLibroModelo = None, offset: int = None, limit: int = None) -> List[libro_mod.LibroModeloDTO]:
        """Obtener lista de libros con filtros opcionales y paginación.
        Pasa offset/limit al repositorio cuando estén presentes.
        """
        if filtro is None:
            filtro = libro_mod.FiltroLibroModelo( titulo=filtro)
        libros = self.repositorio.obtenerLibros(filtro, offset=offset, limit=limit)
        nuevoLibro = []
        for libro in libros:
            libro['_id'] = str(libro['_id'])  # Convertir ObjectId a str
            nuevoLibro.append(libro_mod.LibroModeloDTO(**libro))
        return nuevoLibro