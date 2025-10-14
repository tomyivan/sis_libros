from src.dominio.puertos import publicacion_prt
from src.dominio.modelos import publicacion_mod
class CrearPublicacionServicio:
    def __init__(self, repositorio: publicacion_prt.PublicacionPuerto):
        self.repositorio = repositorio

    def crearPublicacion(self, publicacion: dict) -> bool:
        """Crea una nueva publicación y notifica a los suscriptores."""
        
        return self.repositorio.nuevaPublicacion(publicacion_mod.PublicacionModelo(**publicacion))