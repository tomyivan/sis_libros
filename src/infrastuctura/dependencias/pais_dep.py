from src.helpers.mongoconn_hlp import MongoConnection
from src.infrastuctura.repositorio.pais_rep import PaisRepositorio
from src.dominio.servicios.pais.obtenerPais_srv import ObtenerPaisServicio
from src.dominio.servicios.pais.crearPais_srv import CrearPaisServicio
from src.dominio.servicios.pais.actualizarPais_srv import ActualizarPaisServicio
from src.dominio.servicios.pais.eliminarPais_srv import EliminarPaisServicio
from src.app.pais_app import PaisApp
from src.infrastuctura.http.pais.pais_ctl import PaisControlador

mongo_connection = MongoConnection()
pais_repo = PaisRepositorio(mongo_connection)

obtener_pais_svc = ObtenerPaisServicio(pais_repo)
crear_pais_svc = CrearPaisServicio(pais_repo)
actualizar_pais_svc = ActualizarPaisServicio(pais_repo)
eliminar_pais_svc = EliminarPaisServicio(pais_repo)

pais_app = PaisApp(
    obtener_pais_svc,
    crear_pais_svc,
    actualizar_pais_svc,
    eliminar_pais_svc
)

pais_controlador = PaisControlador(pais_app)
