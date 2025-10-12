from src.dominio.servicios.pais.obtenerPais_srv import ObtenerPaisServicio
from src.dominio.servicios.pais.crearPais_srv import CrearPaisServicio
from src.dominio.servicios.pais.actualizarPais_srv import ActualizarPaisServicio
from src.dominio.servicios.pais.eliminarPais_srv import EliminarPaisServicio


class PaisApp:
    def __init__(self, obtener_svc: ObtenerPaisServicio, crear_svc: CrearPaisServicio, actualizar_svc: ActualizarPaisServicio, eliminar_svc: EliminarPaisServicio):
        self.obtener_svc = obtener_svc
        self.crear_svc = crear_svc
        self.actualizar_svc = actualizar_svc
        self.eliminar_svc = eliminar_svc

    def obtenerPais(self, pais_id: str):
        return self.obtener_svc.ejecutar(pais_id)

    def obtenerPaises(self, offset: int = 0, limit: int = 10, q: str = None):
        if q:
            if hasattr(self.obtener_svc, 'buscarPaises'):
                return self.obtener_svc.buscarPaises(q, offset=offset, limit=limit)
            all_items = self.obtener_svc.repo.obtenerPaises()
            filtered = [p for p in all_items if q.lower() in (p.nombre or '').lower()]
            return filtered[offset:offset+limit]
        if hasattr(self.obtener_svc.repo, 'obtenerPaisesPaged'):
            return self.obtener_svc.repo.obtenerPaisesPaged(offset=offset, limit=limit)
        return self.obtener_svc.repo.obtenerPaises()[offset:offset+limit]

    def crearPais(self, pais):
        return self.crear_svc.ejecutar(pais)

    def actualizarPais(self, pais_id: str, pais):
        return self.actualizar_svc.ejecutar(pais_id, pais)

    def eliminarPais(self, pais_id: str):
        return self.eliminar_svc.ejecutar(pais_id)
