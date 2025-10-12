from src.helpers.mongoconn_hlp import MongoConnection
from src.infrastuctura.repositorio.idioma_rep import IdiomaRepositorio
from src.dominio.servicios.idioma.obtenerIdioma_srv import ObtenerIdiomaServicio
from src.dominio.servicios.idioma.crearIdioma_srv import CrearIdiomaServicio
from src.dominio.servicios.idioma.actualizarIdioma_srv import ActualizarIdiomaServicio
from src.dominio.servicios.idioma.eliminarIdioma_srv import EliminarIdiomaServicio
from src.app.idioma_app import IdiomaApp
from src.infrastuctura.http.idioma.idioma_ctl import IdiomaControlador

mongo_connection = MongoConnection()
idioma_repo = IdiomaRepositorio(mongo_connection)

obtener_idioma_svc = ObtenerIdiomaServicio(idioma_repo)
crear_idioma_svc = CrearIdiomaServicio(idioma_repo)
actualizar_idioma_svc = ActualizarIdiomaServicio(idioma_repo)
eliminar_idioma_svc = EliminarIdiomaServicio(idioma_repo)

idioma_app = IdiomaApp(
    obtener_idioma_svc,
    crear_idioma_svc,
    actualizar_idioma_svc,
    eliminar_idioma_svc
)

idioma_controlador = IdiomaControlador(idioma_app)
