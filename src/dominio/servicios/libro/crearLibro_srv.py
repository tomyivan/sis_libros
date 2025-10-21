from src.dominio.modelos import libro_mod
from src.dominio.puertos import libro_prt
from datetime import datetime
from src.dominio.servicios.recomendacion import recomendacionPorContenido_srv
class CrearLibroServicio:
    def __init__(self, repositorio: libro_prt.LibroPuerto,
                 recomendacion_servicio: recomendacionPorContenido_srv.RecomendarPorContenido
                 ):
        self.repositorio = repositorio
        self.recomendacion_servicio = recomendacion_servicio

    def crearLibro(self, libro_data: dict) -> str:
        """Crear un nuevo libro con validaciones de negocio"""
        # Validaciones de negocio
        # Crear el modelo del libro
        libro = libro_mod.LibroModelo(
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
            fecha_creacion=datetime.now(),
            portada_url=libro_data.get("portada_url"),
            tags=libro_data.get("tags", [])
        )
        idLibro =  self.repositorio.crearLibro(libro)
        self.recomendacion_servicio.agregarNuevaRecomendacion(libro, idLibro)
        return idLibro
