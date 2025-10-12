from src.helpers.mongoconn_hlp import MongoConnection
from src.infrastuctura.repositorio.genero_rep import GeneroRepositorioMongo
from src.dominio.servicios.genero.obtenerGenero_srv import ObtenerGeneroServicio
from src.dominio.servicios.genero.crearGenero_srv import CrearGeneroServicio
from src.dominio.servicios.genero.actualizarGenero_srv import ActualizarGeneroServicio
from src.dominio.servicios.genero.eliminarGenero_srv import EliminarGeneroServicio
from src.app.genero_app import GeneroApp
from src.infrastuctura.http.genero.genero_ctl import GeneroControlador

mongo_connection = MongoConnection()
genero_repo = GeneroRepositorioMongo(mongo_connection)

obtener_genero_svc = ObtenerGeneroServicio(genero_repo)
crear_genero_svc = CrearGeneroServicio(genero_repo)
actualizar_genero_svc = ActualizarGeneroServicio(genero_repo)
eliminar_genero_svc = EliminarGeneroServicio(genero_repo)

genero_app = GeneroApp(
    obtener_genero_svc,
    crear_genero_svc,
    actualizar_genero_svc,
    eliminar_genero_svc
)

genero_controlador = GeneroControlador(genero_app)
