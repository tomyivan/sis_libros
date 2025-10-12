from src.dominio.puertos.idioma_prt import IdiomaPuerto
from src.dominio.modelos import idioma_mod


class CrearIdiomaServicio:
    def __init__(self, repo: IdiomaPuerto):
        self.repo = repo

    def ejecutar(self, idioma):
        return self.repo.crearIdioma(idioma_mod.IdiomaModelo(**idioma))
