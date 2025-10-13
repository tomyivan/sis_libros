from src.infrastuctura.repositorio.calificacion_rep import CalificacionRepositorio
from src.app.calificacion_app import CalificacionApp
from src.infrastuctura.http.calificacion.calificacion_ctl import CalificacionControlador
from src.helpers.mongoconn_hlp import MongoConnection
from src.dominio.servicios.calificacion.crearCalificacion_srv import CrearCalificacionServicio
from src.dominio.servicios.calificacion.obtenerCalificacion_srv import ObtenerCalificacionServicio
from src.dominio.servicios.calificacion.actualizarCalificacion_srv import ActualizarCalificacionServicio
from src.dominio.servicios.calificacion.eliminarCalificacion_srv import EliminarCalificacionServicio
mongo_connection = MongoConnection()
calificacion_repo = CalificacionRepositorio(mongo_connection)

crear_calificacion_svc = CrearCalificacionServicio(calificacion_repo)
obtener_calificacion_svc = ObtenerCalificacionServicio(calificacion_repo)
actualizar_calificacion_svc = ActualizarCalificacionServicio(calificacion_repo)
eliminar_calificacion_svc = EliminarCalificacionServicio(calificacion_repo)
calificacion_app = CalificacionApp(
    crear_calificacion_svc,
    obtener_calificacion_svc,
    actualizar_calificacion_svc,
    eliminar_calificacion_svc
)
calificacion_controlador = CalificacionControlador(calificacion_app)
