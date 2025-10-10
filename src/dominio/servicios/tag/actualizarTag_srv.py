from src.dominio.puertos.tag_prt import TagPuerto
from src.dominio.modelos import tag_mod

class ActualizarTagServicio:
    def __init__(self, repo: TagPuerto):
        self.repo = repo

    def ejecutar(self, tag_id: str, tag):
        return self.repo.actualizarTag(tag_mod.TagModelo(**tag), tag_id)
