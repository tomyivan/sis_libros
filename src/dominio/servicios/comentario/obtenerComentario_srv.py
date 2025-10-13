from src.dominio.puertos import comentario_prt
from src.dominio.modelos import comentarios_mod
from typing import List

class ObtenerComentarioServicio:
    def __init__(self, repo: comentario_prt.ComentarioPuerto):
        self.repo = repo

    def obtenerComentario(self, filtro: comentarios_mod.FiltroComentarioModelo) -> List[comentarios_mod.ComentarioModeloDTO]:
        return self.repo.obtenerComentario(filtro)
