from src.helpers.mongoconn_hlp import MongoConnection
from src.infrastuctura.repositorio.categoria_rep import CategoriaRepositorio
from src.dominio.servicios.categoria.obtenerCategoria_srv import ObtenerCategoriaServicio
from src.dominio.servicios.categoria.crearCategoria_srv import CrearCategoriaServicio
from src.dominio.servicios.categoria.actualizarCategoria_srv import ActualizarCategoriaServicio
from src.dominio.servicios.categoria.eliminarCategoria_srv import EliminarCategoriaServicio
from src.app.categoria_app import CategoriaApp
from src.infrastuctura.http.categoria.categoria_ctl import CategoriaControlador

mongo_connection = MongoConnection()
categoria_repo = CategoriaRepositorio(mongo_connection)

obtener_categoria_svc = ObtenerCategoriaServicio(categoria_repo)
crear_categoria_svc = CrearCategoriaServicio(categoria_repo)
actualizar_categoria_svc = ActualizarCategoriaServicio(categoria_repo)
eliminar_categoria_svc = EliminarCategoriaServicio(categoria_repo)

categoria_app = CategoriaApp(
    obtener_categoria_svc,
    crear_categoria_svc,
    actualizar_categoria_svc,
    eliminar_categoria_svc
)

categoria_controlador = CategoriaControlador(categoria_app)
