from src.app.recomendar_app import RecomendarApp
from src.dominio.servicios.recomendacion import recomendacionPorContenido_srv, obtenerRecomendacion
from src.dominio.servicios.libro import obtenerLibro_srv
from src.infrastuctura.repositorio.recomendacion_rep import RecomendacionRepositorio
from src.infrastuctura.repositorio.recomendacion_rep import RecomendacionRepositorio
from src.infrastuctura.repositorio.libro_rep import LibroRepositorio
from src.helpers.mongoconn_hlp import MongoConnection


mongoConexion = MongoConnection()
libroRepo = LibroRepositorio(mongoConexion)
recomendacionRepo = RecomendacionRepositorio(mongoConexion)
obtenerLibroServicio = obtenerLibro_srv.ObtenerLibroServicio(libroRepo)

recomendarPorContenidoServicio = recomendacionPorContenido_srv.RecomendarPorContenido(obtenerLibroServicio, recomendacionRepo)
obtenerRecomendacionServicio = obtenerRecomendacion.ObtenerRecomendacionServicio(recomendacionRepo)
recomendarApp = RecomendarApp(recomendarPorContenidoServicio, obtenerRecomendacionServicio)
def iniciar_recomendacion():
    return recomendarApp.ejecutarRecomendacion()