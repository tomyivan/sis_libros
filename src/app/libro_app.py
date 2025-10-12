from src.dominio.servicios.libro.obtenerLibro_srv import ObtenerLibroServicio
from src.dominio.servicios.libro.crearLibro_srv import CrearLibroServicio
from src.dominio.servicios.libro.actualizarLibro_srv import ActualizarLibroServicio
from src.dominio.servicios.libro.eliminarLibro_srv import EliminarLibroServicio
from src.dominio.modelos import libro_mod
from typing import List

class LibroApp:
    def __init__(self, 
                 obtener_libro_srv: ObtenerLibroServicio,
                 crear_libro_srv: CrearLibroServicio,
                 actualizar_libro_srv: ActualizarLibroServicio,
                 eliminar_libro_srv: EliminarLibroServicio):
        self.obtener_libro_srv = obtener_libro_srv
        self.crear_libro_srv = crear_libro_srv
        self.actualizar_libro_srv = actualizar_libro_srv
        self.eliminar_libro_srv = eliminar_libro_srv

    # Operaciones de consulta
    def obtenerLibro(self, libro_id: str) -> libro_mod.LibroModeloDTO:
        """Obtener un libro por ID"""
        return self.obtener_libro_srv.obtenerLibro(libro_id)

    def obtenerLibros(self, filtros: dict = None, offset: int = 0, limit: int = 10, q: str = None) -> List[libro_mod.LibroModeloDTO]:
        """Obtener lista de libros con filtros opcionales, paginación y búsqueda.
        Preferimos pasar offset/limit al servicio/repo para que use skip/limit en la BD.
        Si la búsqueda (q) se realiza por un método que no soporta paginación, se hace
        slicing en esta capa como fallback.
        """
        if filtros:
            filtro = libro_mod.FiltroLibroModelo(**filtros)
        else:
            filtro = None

        # Si hay término de búsqueda, delegar a buscarLibros (repo puede o no soportar paginación)
        if q:
            resultados = self.obtener_libro_srv.buscarLibros(q)
            # fallback: si buscarLibros devuelve lista completa, aplicar slicing aquí
            try:
                start = max(0, int(offset))
            except Exception:
                start = 0
            try:
                lim = max(1, int(limit))
            except Exception:
                lim = 10
            end = start + lim
            return resultados[start:end]

        # No búsqueda textual: pasar offset/limit al servicio para que lo propague al repositorio
        return self.obtener_libro_srv.obtenerLibros(filtro, offset=offset, limit=limit)



    # Operaciones de modificación
    def crearLibro(self, libro_data: dict) -> str:
        """Crear un nuevo libro"""
        return self.crear_libro_srv.crearLibro(libro_data)

    def actualizarLibro(self, libro_id: str, libro_data: dict) -> int:
        """Actualizar un libro existente"""
        return self.actualizar_libro_srv.actualizarLibro(libro_id, libro_data)


    def eliminarLibro(self, libro_id: str) -> bool:
        """Eliminar (desactivar) un libro"""
        return self.eliminar_libro_srv.eliminarLibro(libro_id)

