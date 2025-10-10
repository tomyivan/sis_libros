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

    def obtenerLibros(self, filtros: dict = None) -> List[libro_mod.LibroModeloDTO]:
        """Obtener lista de libros con filtros opcionales"""
        if filtros:
            filtro = libro_mod.FiltroLibroModelo(**filtros)
        else:
            filtro = None
        return self.obtener_libro_srv.obtenerLibros(filtro)

    def buscarLibros(self, texto_busqueda: str) -> List[libro_mod.LibroModeloDTO]:
        """Buscar libros por texto"""
        return self.obtener_libro_srv.buscarLibros(texto_busqueda)

    def obtenerLibrosPorGenero(self, genero: str) -> List[libro_mod.LibroModeloDTO]:
        """Obtener libros por género"""
        return self.obtener_libro_srv.obtenerLibrosPorGenero(genero)

    def obtenerLibrosPorAutor(self, autor: str) -> List[libro_mod.LibroModeloDTO]:
        """Obtener libros por autor"""
        return self.obtener_libro_srv.obtenerLibrosPorAutor(autor)

    def obtenerLibrosPorAño(self, año_min: int = None, año_max: int = None) -> List[libro_mod.LibroModeloDTO]:
        """Obtener libros por rango de años"""
        return self.obtener_libro_srv.obtenerLibrosPorAño(año_min, año_max)

    def obtenerLibrosMejorCalificados(self, limite: int = 10) -> List[libro_mod.LibroModeloDTO]:
        """Obtener libros mejor calificados"""
        return self.obtener_libro_srv.obtenerLibrosMejorCalificados(limite)

    # Operaciones de modificación
    def crearLibro(self, libro_data: dict) -> str:
        """Crear un nuevo libro"""
        return self.crear_libro_srv.crearLibro(libro_data)

    def actualizarLibro(self, libro_id: str, libro_data: dict) -> int:
        """Actualizar un libro existente"""
        return self.actualizar_libro_srv.actualizarLibro(libro_id, libro_data)

    def calificarLibro(self, libro_id: str, calificacion: float) -> int:
        """Agregar una calificación a un libro"""
        return self.actualizar_libro_srv.actualizarCalificacion(libro_id, calificacion)

    def eliminarLibro(self, libro_id: str) -> bool:
        """Eliminar (desactivar) un libro"""
        return self.eliminar_libro_srv.eliminarLibro(libro_id)

    def reactivarLibro(self, libro_id: str) -> bool:
        """Reactivar un libro previamente eliminado"""
        return self.eliminar_libro_srv.reactivarLibro(libro_id)

    # Operaciones estadísticas
    def obtenerEstadisticasLibros(self) -> dict:
        """Obtener estadísticas generales de libros"""
        todos_libros = self.obtener_libro_srv.obtenerLibros()
        libros_activos = [l for l in todos_libros if l.disponible]
        
        if not todos_libros:
            return {
                "total_libros": 0,
                "libros_activos": 0,
                "libros_inactivos": 0,
                "generos_unicos": 0,
                "autores_unicos": 0,
                "calificacion_promedio_general": 0.0,
                "año_publicacion_min": None,
                "año_publicacion_max": None
            }
        
        generos = set(libro.genero for libro in libros_activos)
        autores = set(libro.autor for libro in libros_activos)
        
        calificaciones = [l.calificacion_promedio for l in libros_activos if l.calificacion_promedio > 0]
        calificacion_promedio_general = sum(calificaciones) / len(calificaciones) if calificaciones else 0.0
        
        años = [l.año_publicacion for l in libros_activos]
        
        return {
            "total_libros": len(todos_libros),
            "libros_activos": len(libros_activos),
            "libros_inactivos": len(todos_libros) - len(libros_activos),
            "generos_unicos": len(generos),
            "autores_unicos": len(autores),
            "calificacion_promedio_general": round(calificacion_promedio_general, 2),
            "año_publicacion_min": min(años) if años else None,
            "año_publicacion_max": max(años) if años else None
        }