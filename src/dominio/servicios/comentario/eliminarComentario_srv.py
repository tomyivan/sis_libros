from src.dominio.puertos import comentario_prt

class EliminarComentarioServicio:
    def __init__(self, repo: comentario_prt.ComentarioPuerto):
        self.repo = repo

    def eliminarComentario(self, comentarioId: str) -> bool:
        return self.repo.eliminarComentario(comentarioId)
