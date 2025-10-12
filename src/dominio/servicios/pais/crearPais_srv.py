from src.dominio.puertos.pais_prt import PaisPuerto
from src.dominio.modelos import pais_mod


class CrearPaisServicio:
    def __init__(self, repo: PaisPuerto):
        self.repo = repo

    def ejecutar(self, pais):
        return self.repo.crearPais(pais_mod.PaisModelo(**pais))
