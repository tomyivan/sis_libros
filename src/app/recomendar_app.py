from src.dominio.servicios.recomendacion import recomendacionPorContenido_srv
from src.dominio.servicios.recomendacion import obtenerRecomendacion
from src.dominio.modelos.libro_mod import LibroModelo
class RecomendarApp:
    def __init__(self, recomendarPorContenidoServicio: recomendacionPorContenido_srv.RecomendarPorContenido,
                    obtenerRecomendacionServicio: obtenerRecomendacion.ObtenerRecomendacionServicio
                 ):
        self.recomendarPorContenidoServicio = recomendarPorContenidoServicio
        self.obtenerRecomendacionServicio = obtenerRecomendacionServicio

    def ejecutarRecomendacion(self) -> bool:
        return self.recomendarPorContenidoServicio.recomendarPorContenido()

    def agregarNuevaRecomendacion(self, data: LibroModelo) -> bool:
        return self.recomendarPorContenidoServicio.agregarNuevaRecomendacion(data)

    def obtenerRecomendacionPorLibro(self, idLibro: str):
        return self.obtenerRecomendacionServicio.obtenerPorLibro(idLibro)