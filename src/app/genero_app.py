from src.dominio.servicios.genero.obtenerGenero_srv import ObtenerGeneroServicio
from src.dominio.servicios.genero.crearGenero_srv import CrearGeneroServicio
from src.dominio.servicios.genero.actualizarGenero_srv import ActualizarGeneroServicio
from src.dominio.servicios.genero.eliminarGenero_srv import EliminarGeneroServicio


class GeneroApp:
    def __init__(self, obtener_svc: ObtenerGeneroServicio, crear_svc: CrearGeneroServicio, actualizar_svc: ActualizarGeneroServicio, eliminar_svc: EliminarGeneroServicio):
        self.obtener_svc = obtener_svc
        self.crear_svc = crear_svc
        self.actualizar_svc = actualizar_svc
        self.eliminar_svc = eliminar_svc

    def obtenerGenero(self, genero_id: str):
        return self.obtener_svc.ejecutar(genero_id)

    def obtenerGeneros(self, offset: int = 0, limit: int = 10, q: str = None):
        if q:
            if hasattr(self.obtener_svc, 'buscarGeneros'):
                return self.obtener_svc.buscarGeneros(q, offset=offset, limit=limit)
            all_items = self.obtener_svc.repo.obtener_generos()
            filtered = [g for g in all_items if q.lower() in (g.nombre or '').lower()]
            return filtered[offset:offset+limit]
        if hasattr(self.obtener_svc.repo, 'obtenerGenerosPaged'):
            return self.obtener_svc.repo.obtenerGenerosPaged(offset=offset, limit=limit)
        return self.obtener_svc.repo.obtener_generos()[offset:offset+limit]

    def crearGenero(self, genero):
        return self.crear_svc.ejecutar(genero) 

    def actualizarGenero(self, genero_id: str, genero):
        return self.actualizar_svc.ejecutar(genero_id, genero)

    def eliminarGenero(self, genero_id: str):
        return self.eliminar_svc.ejecutar(genero_id)
