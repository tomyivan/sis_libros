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

    def obtenerTags(self, offset: int = 0, limit: int = 10, q: str = None):
        # Si hay búsqueda, delegar a método de búsqueda del servicio/repo si existe
        if q:
            # intentar método de búsqueda en el servicio
            if hasattr(self.obtener_svc, 'buscarTags'):
                return self.obtener_svc.buscarTags(q, offset=offset, limit=limit)
            # fallback: traer todos y filtrar en memoria (no ideal)
            all_tags = self.obtener_svc.repo.obtenerTags()
            print(all_tags)
            filtered = [t for t in all_tags if q.lower() in (t.nombre or '').lower()]
            return filtered[offset:offset+limit]
        # paginación directa si el repo lo soporta
        if hasattr(self.obtener_svc.repo, 'obtenerTagsPaged'):
            return self.obtener_svc.repo.obtenerTagsPaged(offset=offset, limit=limit)
        return self.obtener_svc.repo.obtenerTags()[offset:offset+limit]

    def crearTag(self, tag):
        return self.crear_svc.ejecutar(tag)

    def actualizarTag(self, tag_id: str, tag):
        return self.actualizar_svc.ejecutar(tag_id, tag)

    def eliminarTag(self, tag_id: str):
        return self.eliminar_svc.ejecutar(tag_id)
