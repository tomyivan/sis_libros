from src.dominio.puertos.pais_prt import PaisPuerto


class EliminarPaisServicio:
    def __init__(self, repo: PaisPuerto):
        self.repo = repo

    def ejecutar(self, pais_id: str):
        return self.repo.eliminarPais(pais_id)
