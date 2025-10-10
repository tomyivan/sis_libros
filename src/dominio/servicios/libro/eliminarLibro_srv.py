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

    def reactivarLibro(self, libro_id: str) -> bool:
        """Reactivar un libro previamente eliminado"""
        
        # Verificar que el libro existe
        libro_existente = self.repositorio.obtenerLibro(
            libro_mod.FiltroLibroModelo(_id=libro_id)
        )
        if not libro_existente:
            raise ValueError("El libro no existe")
        
        # Verificar que el libro esté desactivado
        if libro_existente.disponible:
            raise ValueError("El libro ya está activo")
        
        # Crear libro reactivado
        from datetime import datetime
        libro_reactivado = libro_mod.LibroModelo(
            titulo=libro_existente.titulo,
            autor=libro_existente.autor,
            genero=libro_existente.genero,
            año_publicacion=libro_existente.año_publicacion,
            editorial=libro_existente.editorial,
            isbn=libro_existente.isbn,
            paginas=libro_existente.paginas,
            idioma=libro_existente.idioma,
            descripcion=libro_existente.descripcion,
            origen_pais=libro_existente.origen_pais,
            disponible=True,  # Reactivar
            fecha_creacion=libro_existente.fecha_creacion,
            fecha_modificacion=datetime.now(),
            calificacion_promedio=libro_existente.calificacion_promedio,
            numero_calificaciones=libro_existente.numero_calificaciones,
            portada_url=libro_existente.portada_url,
            tags=libro_existente.tags
        )
        
        result = self.repositorio.actualizarLibro(libro_reactivado, libro_id)
        return result > 0