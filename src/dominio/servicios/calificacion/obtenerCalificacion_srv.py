from src.dominio.puertos.calificacion_prt import CalificacionPuerto
from src.dominio.modelos.calificacion_mod import FiltroCalificacionModelo

class ObtenerCalificacionServicio:
    def __init__(self, repo: CalificacionPuerto):
        self.repo = repo

    def ejecutar(self, filtro: FiltroCalificacionModelo):
        return self.repo.obtenerCalificacion(filtro.__dict__)
