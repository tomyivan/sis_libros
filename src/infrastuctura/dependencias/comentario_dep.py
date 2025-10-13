from src.helpers.mongoconn_hlp import MongoConnection
from src.infrastuctura.repositorio.comentario_rep import ComentarioRepositorio
from src.dominio.servicios.comentario.obtenerComentario_srv import ObtenerComentarioServicio
from src.dominio.servicios.comentario.crearComentario_srv import CrearComentarioServicio
from src.dominio.servicios.comentario.actualizarComentario_srv import ActualizarComentarioServicio
from src.dominio.servicios.comentario.eliminarComentario_srv import EliminarComentarioServicio
from src.app.comentario_app import ComentarioApp
from src.infrastuctura.http.comentario.comentario_ctl import ComentarioControlador

mongo_connection = MongoConnection()
comentario_repo = ComentarioRepositorio(mongo_connection)

obtener_comentario_svc = ObtenerComentarioServicio(comentario_repo)
crear_comentario_svc = CrearComentarioServicio(comentario_repo)
actualizar_comentario_svc = ActualizarComentarioServicio(comentario_repo)
eliminar_comentario_svc = EliminarComentarioServicio(comentario_repo)

comentario_app = ComentarioApp(
    obtener_comentario_svc,
    crear_comentario_svc,
    actualizar_comentario_svc,
    eliminar_comentario_svc
)

comentario_controlador = ComentarioControlador(comentario_app)
