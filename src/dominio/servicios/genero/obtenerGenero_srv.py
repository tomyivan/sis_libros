from src.dominio.puertos.genero_prt import GeneroRepositorio


class ObtenerGeneroServicio:
    def __init__(self, repo: GeneroRepositorio):
        self.repo = repo

    def ejecutar(self, genero_id: str):
        return self.repo.obtener_genero(genero_id)
