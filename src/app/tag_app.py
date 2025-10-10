from src.dominio.servicios.tag.obtenerTag_srv import ObtenerTagServicio
from src.dominio.servicios.tag.crearTag_srv import CrearTagServicio
from src.dominio.servicios.tag.actualizarTag_srv import ActualizarTagServicio
from src.dominio.servicios.tag.eliminarTag_srv import EliminarTagServicio

class TagApp:
    def __init__(self, obtener_svc: ObtenerTagServicio, crear_svc: CrearTagServicio, actualizar_svc: ActualizarTagServicio, eliminar_svc: EliminarTagServicio):
        self.obtener_svc = obtener_svc
        self.crear_svc = crear_svc
        self.actualizar_svc = actualizar_svc
        self.eliminar_svc = eliminar_svc

    def obtenerTag(self, tag_id: str):
        return self.obtener_svc.ejecutar(tag_id)

    def obtenerTags(self):
        return self.obtener_svc.repo.obtenerTags()

    def crearTag(self, tag):
        return self.crear_svc.ejecutar(tag)

    def actualizarTag(self, tag_id: str, tag):
        return self.actualizar_svc.ejecutar(tag_id, tag)

    def eliminarTag(self, tag_id: str):
        return self.eliminar_svc.ejecutar(tag_id)
