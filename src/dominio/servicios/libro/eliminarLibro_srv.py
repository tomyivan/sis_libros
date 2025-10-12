from src.dominio.modelos import libro_mod
from src.dominio.puertos import libro_prt

class EliminarLibroServicio:
    def __init__(self, repositorio: libro_prt.LibroPuerto):
        self.repositorio = repositorio

    def eliminarLibro(self, libro_id: str) -> bool:
        """Eliminar (desactivar) un libro"""
        
        # Verificar que el libro existe
        libro_existente = self.repositorio.obtenerLibro(
            libro_mod.FiltroLibroModelo(_id=libro_id)
        )
        if not libro_existente:
            raise ValueError("El libro no existe")
        
        # Verificar que el libro esté disponible
        if not libro_existente.disponible:
            raise ValueError("El libro ya está desactivado")
        
        # Realizar soft delete
        return self.repositorio.eliminarLibro(libro_id)