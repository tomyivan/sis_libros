from src.dominio.puertos.genero_prt import GeneroRepositorio


class EliminarGeneroServicio:
    def __init__(self, repo: GeneroRepositorio):
        self.repo = repo

    def ejecutar(self, genero_id: str):
        return self.repo.eliminar_genero(genero_id)
