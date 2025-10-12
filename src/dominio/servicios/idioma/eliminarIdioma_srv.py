from src.dominio.puertos.idioma_prt import IdiomaPuerto


class EliminarIdiomaServicio:
    def __init__(self, repo: IdiomaPuerto):
        self.repo = repo

    def ejecutar(self, idioma_id: str):
        return self.repo.eliminarIdioma(idioma_id)
