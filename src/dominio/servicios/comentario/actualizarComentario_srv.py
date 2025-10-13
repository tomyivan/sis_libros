from src.dominio.puertos import comentario_prt
from src.dominio.modelos import comentarios_mod

class ActualizarComentarioServicio:
    def __init__(self, repo: comentario_prt.ComentarioPuerto):
        self.repo = repo

    def actualizarComentario(self, comentario: comentarios_mod.ComentarioModelo, comentarioId: str) -> int:
        return self.repo.actualizarComentario(comentario, comentarioId)
