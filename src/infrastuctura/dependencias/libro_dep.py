# Dependencias para el módulo de libros
from src.helpers.mongoconn_hlp import MongoConnection
from src.infrastuctura.repositorio.libro_rep import LibroRepositorio
from src.dominio.servicios.libro.obtenerLibro_srv import ObtenerLibroServicio
from src.dominio.servicios.libro.crearLibro_srv import CrearLibroServicio
from src.dominio.servicios.libro.actualizarLibro_srv import ActualizarLibroServicio
from src.dominio.servicios.libro.eliminarLibro_srv import EliminarLibroServicio
from src.app.libro_app import LibroApp
from src.infrastuctura.http.libro.libro_ctl import LibroControlador

# Configuración de dependencias
mongo_connection = MongoConnection()
libro_repositorio = LibroRepositorio(mongo_connection)

# Servicios de dominio
obtener_libro_servicio = ObtenerLibroServicio(libro_repositorio)
crear_libro_servicio = CrearLibroServicio(libro_repositorio)
actualizar_libro_servicio = ActualizarLibroServicio(libro_repositorio)
eliminar_libro_servicio = EliminarLibroServicio(libro_repositorio)

# Servicio de aplicación
libro_app = LibroApp(
    obtener_libro_servicio,
    crear_libro_servicio,
    actualizar_libro_servicio,
    eliminar_libro_servicio
)

# Controlador HTTP
libro_controlador = LibroControlador(libro_app)