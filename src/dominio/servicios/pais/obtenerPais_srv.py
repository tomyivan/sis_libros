from src.dominio.puertos.pais_prt import PaisPuerto


class ObtenerPaisServicio:
    def __init__(self, repo: PaisPuerto):
        self.repo = repo

    def ejecutar(self, pais_id: str):
        respuesta = self.repo.obtenerPais(pais_id)
        return respuesta