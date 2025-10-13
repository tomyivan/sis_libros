from src.dominio.puertos.calificacion_prt import CalificacionPuerto

class EliminarCalificacionServicio:
    def __init__(self, repo: CalificacionPuerto):
        self.repo = repo

    def ejecutar(self, calificacionId: str) -> bool:
        return self.repo.eliminarCalificacion(calificacionId)
