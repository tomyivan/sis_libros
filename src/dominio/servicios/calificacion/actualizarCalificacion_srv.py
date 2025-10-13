from src.dominio.puertos.calificacion_prt import CalificacionPuerto
from src.dominio.modelos.calificacion_mod import CalificacionModelo

class ActualizarCalificacionServicio:
    def __init__(self, repo: CalificacionPuerto):
        self.repo = repo

    def ejecutar(self, calificacion: CalificacionModelo, calificacionId: str) -> int:
        return self.repo.actualizarCalificacion(calificacion, calificacionId)
