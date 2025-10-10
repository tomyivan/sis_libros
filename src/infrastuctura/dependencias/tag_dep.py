from src.helpers.mongoconn_hlp import MongoConnection
from src.infrastuctura.repositorio.tag_rep import TagRepositorio
from src.dominio.servicios.tag.obtenerTag_srv import ObtenerTagServicio
from src.dominio.servicios.tag.crearTag_srv import CrearTagServicio
from src.dominio.servicios.tag.actualizarTag_srv import ActualizarTagServicio
from src.dominio.servicios.tag.eliminarTag_srv import EliminarTagServicio
from src.app.tag_app import TagApp
from src.infrastuctura.http.tag.tag_ctl import TagControlador

mongo_connection = MongoConnection()
tag_repo = TagRepositorio(mongo_connection)

obtener_tag_svc = ObtenerTagServicio(tag_repo)
crear_tag_svc = CrearTagServicio(tag_repo)
actualizar_tag_svc = ActualizarTagServicio(tag_repo)
eliminar_tag_svc = EliminarTagServicio(tag_repo)

tag_app = TagApp(
    obtener_tag_svc,
    crear_tag_svc,
    actualizar_tag_svc,
    eliminar_tag_svc
)

tag_controlador = TagControlador(tag_app)
