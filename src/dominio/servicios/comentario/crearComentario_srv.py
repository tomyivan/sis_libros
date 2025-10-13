from src.dominio.puertos import comentario_prt
from src.dominio.modelos import comentarios_mod

class CrearComentarioServicio:
    def __init__(self, repo: comentario_prt.ComentarioPuerto):
        self.repo = repo

    def crearComentario(self, comentario: comentarios_mod.ComentarioModelo) -> str:
        return self.repo.crearComentario(comentario)
