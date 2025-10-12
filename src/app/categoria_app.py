from src.dominio.servicios.categoria.obtenerCategoria_srv import ObtenerCategoriaServicio
from src.dominio.servicios.categoria.crearCategoria_srv import CrearCategoriaServicio
from src.dominio.servicios.categoria.actualizarCategoria_srv import ActualizarCategoriaServicio
from src.dominio.servicios.categoria.eliminarCategoria_srv import EliminarCategoriaServicio

class CategoriaApp:
    def __init__(self, obtener_svc: ObtenerCategoriaServicio, crear_svc: CrearCategoriaServicio, actualizar_svc: ActualizarCategoriaServicio, eliminar_svc: EliminarCategoriaServicio):
        self.obtener_svc = obtener_svc
        self.crear_svc = crear_svc
        self.actualizar_svc = actualizar_svc
        self.eliminar_svc = eliminar_svc

    def obtenerCategoria(self, categoria_id: str):
        return self.obtener_svc.ejecutar(categoria_id)

    def obtenerCategorias(self, offset: int = 0, limit: int = 10, q: str = None):
        if q:
            if hasattr(self.obtener_svc, 'buscarCategorias'):
                return self.obtener_svc.buscarCategorias(q, offset=offset, limit=limit)
            all_items = self.obtener_svc.repo.obtenerCategorias()
            filtered = [c for c in all_items if q.lower() in (c.nombre or '').lower()]
            return filtered[offset:offset+limit]
        if hasattr(self.obtener_svc.repo, 'obtenerCategoriasPaged'):
            return self.obtener_svc.repo.obtenerCategoriasPaged(offset=offset, limit=limit)
        return self.obtener_svc.repo.obtenerCategorias()[offset:offset+limit]

    def crearCategoria(self, categoria):
        return self.crear_svc.ejecutar(categoria)

    def actualizarCategoria(self, categoria_id: str, categoria):
        return self.actualizar_svc.ejecutar(categoria_id, categoria)

    def eliminarCategoria(self, categoria_id: str):
        return self.eliminar_svc.ejecutar(categoria_id)
