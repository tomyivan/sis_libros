from src.dominio.puertos.genero_prt import GeneroRepositorio
from src.dominio.modelos import genero_mod


class CrearGeneroServicio:
    def __init__(self, repo: GeneroRepositorio):
        self.repo = repo

    def ejecutar(self, genero):
        return self.repo.crear_genero(genero_mod.GeneroModelo(**genero))
