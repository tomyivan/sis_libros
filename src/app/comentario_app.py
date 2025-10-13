from src.dominio.servicios.comentario.obtenerComentario_srv import ObtenerComentarioServicio
from src.dominio.servicios.comentario.crearComentario_srv import CrearComentarioServicio
from src.dominio.servicios.comentario.actualizarComentario_srv import ActualizarComentarioServicio
from src.dominio.servicios.comentario.eliminarComentario_srv import EliminarComentarioServicio

class ComentarioApp:
    def __init__(self, obtener_svc: ObtenerComentarioServicio, crear_svc: CrearComentarioServicio, actualizar_svc: ActualizarComentarioServicio, eliminar_svc: EliminarComentarioServicio):
        self.obtener_svc = obtener_svc
        self.crear_svc = crear_svc
        self.actualizar_svc = actualizar_svc
        self.eliminar_svc = eliminar_svc

    def crearComentario(self, comentario):
        return self.crear_svc.crearComentario(comentario)

    def obtenerComentario(self, filtro):
        return self.obtener_svc.obtenerComentario(filtro)

    def actualizarComentario(self, comentario, comentarioId):
        return self.actualizar_svc.actualizarComentario(comentario, comentarioId)

    def eliminarComentario(self, comentarioId):
        return self.eliminar_svc.eliminarComentario(comentarioId)
