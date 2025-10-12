from src.dominio.puertos.pais_prt import PaisPuerto


class ObtenerPaisServicio:
    def __init__(self, repo: PaisPuerto):
        self.repo = repo

    def ejecutar(self, pais_id: str):
        print(f"Ejecutando ObtenerPaisServicio con pais_id: {pais_id}")
        respuesta = self.repo.obtenerPais(pais_id)
        print(f"Respuesta obtenida: {respuesta}")
        return respuesta