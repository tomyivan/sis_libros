from src.dominio.puertos.tag_prt import TagPuerto
from src.dominio.modelos import tag_mod

class CrearTagServicio:
    def __init__(self, repo: TagPuerto):
        self.repo = repo

    def ejecutar(self, tag):
        return self.repo.crearTag(tag_mod.TagModelo(**tag))
