from src.dominio.puertos.calificacion_prt import CalificacionPuerto
from src.dominio.modelos.calificacion_mod import CalificacionModelo

class CrearCalificacionServicio:
    def __init__(self, repo: CalificacionPuerto):
        self.repo = repo

    def ejecutar(self, calificacion: CalificacionModelo) -> str:
        # could add business rules (e.g., valid range) here
        return self.repo.crearCalificacion(calificacion)
