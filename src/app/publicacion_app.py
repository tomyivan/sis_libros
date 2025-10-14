from src.dominio.servicios.publicaciones import crearPublicacion_srv, obtenerPublicacion_srv
class PublicacionApp:
    def __init__(self, crearPublicacionServicio: crearPublicacion_srv.CrearPublicacionServicio,
                    obtenerPublicacionServicio: obtenerPublicacion_srv.ObtenerPublicacionServicio
                 ):
        self.crearPublicacionServicio = crearPublicacionServicio
        self.obtenerPublicacionServicio = obtenerPublicacionServicio

    def nuevaPublicacion(self, publicacion: dict) -> bool:
        return self.crearPublicacionServicio.crearPublicacion(publicacion)
    
    def obtenerPublicaciones(self) -> list:
        return self.obtenerPublicacionServicio.obtenerPublicaciones()
