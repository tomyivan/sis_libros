from src.app.recomendar_app import RecomendarApp
from src.dominio.servicios.recomendacion import recomendacionPorContenido_srv, obtenerRecomendacion
from src.infrastuctura.repositorio.interaccion_rep import InteraccionRepositorio
from src.dominio.servicios.libro import obtenerLibro_srv
from src.infrastuctura.repositorio.recomendacion_rep import RecomendacionRepositorio
from src.infrastuctura.repositorio.recomendacion_rep import RecomendacionRepositorio
from src.infrastuctura.repositorio.libro_rep import LibroRepositorio
from src.helpers.mongoconn_hlp import MongoConnection
from src.dominio.servicios.interaccion.interaccion_srv import InteraccionServicio

mongoConexion = MongoConnection()
libroRepo = LibroRepositorio(mongoConexion)
recomendacionRepo = RecomendacionRepositorio(mongoConexion)
interaccionRepo  = InteraccionRepositorio()
interacconServicio = InteraccionServicio(interaccionRepo)
obtenerLibroServicio = obtenerLibro_srv.ObtenerLibroServicio(libroRepo, interacconServicio)

recomendarPorContenidoServicio = recomendacionPorContenido_srv.RecomendarPorContenido(obtenerLibroServicio, recomendacionRepo)
obtenerRecomendacionServicio = obtenerRecomendacion.ObtenerRecomendacionServicio(recomendacionRepo)
recomendarApp = RecomendarApp(recomendarPorContenidoServicio, obtenerRecomendacionServicio)
def iniciar_recomendacion():
    return recomendarApp.ejecutarRecomendacion()