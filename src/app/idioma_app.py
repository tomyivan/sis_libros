from src.dominio.servicios.idioma.obtenerIdioma_srv import ObtenerIdiomaServicio
from src.dominio.servicios.idioma.crearIdioma_srv import CrearIdiomaServicio
from src.dominio.servicios.idioma.actualizarIdioma_srv import ActualizarIdiomaServicio
from src.dominio.servicios.idioma.eliminarIdioma_srv import EliminarIdiomaServicio


class IdiomaApp:
    def __init__(self, obtener_svc: ObtenerIdiomaServicio, crear_svc: CrearIdiomaServicio, actualizar_svc: ActualizarIdiomaServicio, eliminar_svc: EliminarIdiomaServicio):
        self.obtener_svc = obtener_svc
        self.crear_svc = crear_svc
        self.actualizar_svc = actualizar_svc
        self.eliminar_svc = eliminar_svc

    def obtenerIdioma(self, idioma_id: str):
        return self.obtener_svc.ejecutar(idioma_id)

    def obtenerIdiomas(self, offset: int = 0, limit: int = 10, q: str = None):
        if q:
            if hasattr(self.obtener_svc, 'buscarIdiomas'):
                return self.obtener_svc.buscarIdiomas(q, offset=offset, limit=limit)
            all_items = self.obtener_svc.repo.obtenerIdiomas()
            filtered = [p for p in all_items if q.lower() in (p.nombre or '').lower()]
            return filtered[offset:offset+limit]
        if hasattr(self.obtener_svc.repo, 'obtenerIdiomasPaged'):
            return self.obtener_svc.repo.obtenerIdiomasPaged(offset=offset, limit=limit)
        return self.obtener_svc.repo.obtenerIdiomas()[offset:offset+limit]

    def crearIdioma(self, idioma):
        return self.crear_svc.ejecutar(idioma)

    def actualizarIdioma(self, idioma_id: str, idioma):
        return self.actualizar_svc.ejecutar(idioma_id, idioma)

    def eliminarIdioma(self, idioma_id: str):
        return self.eliminar_svc.ejecutar(idioma_id)
