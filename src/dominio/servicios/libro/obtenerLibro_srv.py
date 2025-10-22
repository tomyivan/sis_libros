from src.dominio.modelos import libro_mod
from src.dominio.puertos import libro_prt
from typing import List
from src.dominio.servicios.interaccion import interaccion_srv
class ObtenerLibroServicio:
    def __init__(self, repositorio: libro_prt.LibroPuerto,
                 interaccionSrv: interaccion_srv.InteraccionServicio):
        self.repositorio = repositorio
        self.interaccionSrv = interaccionSrv

    def obtenerLibroInfo(self, libro_id: str, idUsuario: str = None ) -> libro_mod.LibroInformacion:
        """Obtener información detallada de un libro por su ID, incluyendo estadísticas agregadas."""
        # print("Obteniendo información del libro:", libro_id)
        libro = self.repositorio.obtenerLibroInfo(libro_id)

        if libro:
            libro['_id'] = str(libro['_id'])  # Convertir ObjectId a str
            self.interaccionSrv.ver(libro_id, idUsuario)
            return libro_mod.LibroInformacion(**libro)
        return None

    def obtenerLibro(self, libro_id: str) -> libro_mod.LibroModeloDTO:
        """Obtener un libro por ID"""
        filtro = libro_mod.FiltroLibroModelo(_id = libro_id)
        libro = self.repositorio.obtenerLibro(filtro)
        if libro:
            libro['_id'] = str(libro['_id'])  # Convertir ObjectId a str
            return libro_mod.LibroModeloDTO(**libro)
        return None
        
    def obtenerLibros(self, filtro: libro_mod.FiltroLibroModelo = None, offset: int = None, limit: int = None) -> List[libro_mod.LibroModeloDTO]:
        """Obtener lista de libros con filtros opcionales y paginación.
        Pasa offset/limit al repositorio cuando estén presentes.
        """
        if filtro is None:
            filtro = libro_mod.FiltroLibroModelo( titulo=filtro, disponible=True )
        libros = self.repositorio.obtenerLibros(filtro, offset=offset, limit=limit)
        nuevoLibro = []
        for libro in libros:
            libro['_id'] = str(libro['_id'])  # Convertir ObjectId a str
            nuevoLibro.append(libro_mod.LibroModeloDTO(**libro))
        return nuevoLibro
    
    def totalLibros(self) -> int:
        """Contar el total de libros en el repositorio."""
        return self.repositorio.totalLibros()