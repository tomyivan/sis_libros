from src.dominio.puertos.calificacion_prt import CalificacionPuerto
from src.dominio.modelos.calificacion_mod import CalificacionModelo
from src.dominio.servicios.interaccion import interaccion_srv

class CrearCalificacionServicio:
    def __init__(self, repo: CalificacionPuerto,
                 interaccionSrv: interaccion_srv.InteraccionServicio):
        self.repo = repo
        self.interaccionSrv = interaccionSrv

    def ejecutar(self, calificacion: CalificacionModelo) -> str:
        # could add business rules (e.g., valid range) here
        self.interaccionSrv.calificar(calificacion.id_libro, calificacion.calificacion, calificacion.id_usuario)
        return self.repo.crearCalificacion(calificacion)





















