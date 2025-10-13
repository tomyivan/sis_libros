from src.dominio.modelos import libro_mod
from src.dominio.puertos import libro_prt
from datetime import datetime

class ActualizarLibroServicio:
    def __init__(self, repositorio: libro_prt.LibroPuerto):
        self.repositorio = repositorio

    def actualizarLibro(self, libro_id: str, libro_data: dict) -> int:
        """Actualizar un libro existente"""
        
        # Verificar que el libro existe
        libro_existente = self.repositorio.obtenerLibro(
            libro_mod.FiltroLibroModelo(_id=libro_id)
        )
        if not libro_existente:
            raise ValueError("El libro no existe")
        
        
        # Crear el modelo actualizado
        libro_actualizado = libro_mod.LibroModelo(
            titulo=libro_data["titulo"],
            autor=libro_data["autor"],
            genero=libro_data["genero"],
            año_publicacion=libro_data["año_publicacion"],
            editorial=libro_data["editorial"],
            isbn=libro_data["isbn"],
            paginas=libro_data["paginas"],
            idioma=libro_data["idioma"],
            descripcion=libro_data["descripcion"],
            origen_pais=libro_data["origen_pais"],
            disponible=libro_data.get("disponible", True),
            fecha_creacion=libro_existente.get('fecha_creacion') if isinstance(libro_existente, dict) else getattr(libro_existente, 'fecha_creacion', None),  # Mantener fecha original
            fecha_modificacion=datetime.now(),
            portada_url=libro_data.get("portada_url", libro_existente.get('portada_url') if isinstance(libro_existente, dict) else getattr(libro_existente, 'portada_url', None)),
            tags=libro_data.get("tags", libro_existente.get('tags', []) if isinstance(libro_existente, dict) else getattr(libro_existente, 'tags', []) )
        )
        
        return self.repositorio.actualizarLibro(libro_actualizado, libro_id)
