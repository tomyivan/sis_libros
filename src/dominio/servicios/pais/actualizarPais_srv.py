from src.dominio.puertos.pais_prt import PaisPuerto
from src.dominio.modelos import pais_mod


class ActualizarPaisServicio:
    def __init__(self, repo: PaisPuerto):
        self.repo = repo

    def ejecutar(self, pais_id: str, pais):
        return self.repo.actualizarPais(pais_mod.PaisModelo(**pais), pais_id)
