import src.dominio.puertos.recomendacion_prt as recomendacion_prt
from typing import List
from src.dominio.modelos import recomendacion_mod
class ObtenerRecomendacionServicio:
    def __init__(self, repo: recomendacion_prt.RecomendacionPuerto):
        self.repo = repo

    def obtenerPorLibro(self, idLibro: str) -> List[recomendacion_mod.RecomendacionModeloDTO]:
        recomendaciones = self.repo.obtenerRecomendacionPorLibro(idLibro)
        if recomendaciones is None:
            return []
        return recomendaciones
