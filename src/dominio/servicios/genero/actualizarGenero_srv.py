from src.dominio.puertos.genero_prt import GeneroRepositorio
from src.dominio.modelos import genero_mod


class ActualizarGeneroServicio:
    def __init__(self, repo: GeneroRepositorio):
        self.repo = repo

    def ejecutar(self, genero_id: str, genero):
        return self.repo.actualizar_genero(genero_mod.GeneroModelo(**genero), genero_id)
