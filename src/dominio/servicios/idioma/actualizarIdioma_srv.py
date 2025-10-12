from src.dominio.puertos.idioma_prt import IdiomaPuerto
from src.dominio.modelos import idioma_mod


class ActualizarIdiomaServicio:
    def __init__(self, repo: IdiomaPuerto):
        self.repo = repo

    def ejecutar(self, idioma_id: str, idioma):
        return self.repo.actualizarIdioma(idioma_mod.IdiomaModelo(**idioma), idioma_id)
