from src.dominio.servicios.calificacion.crearCalificacion_srv import CrearCalificacionServicio
from src.dominio.servicios.calificacion.obtenerCalificacion_srv import ObtenerCalificacionServicio
from src.dominio.servicios.calificacion.actualizarCalificacion_srv import ActualizarCalificacionServicio
from src.dominio.servicios.calificacion.eliminarCalificacion_srv import EliminarCalificacionServicio

class CalificacionApp:
    def __init__(self, 
                 crear: CrearCalificacionServicio,
                 obtener: ObtenerCalificacionServicio,
                 actualizar: ActualizarCalificacionServicio,
                 eliminar: EliminarCalificacionServicio):
        self.crear = crear
        self.obtener = obtener
        self.actualizar = actualizar
        self.eliminar = eliminar

    def crearCalificacion(self, calificacion):
        return self.crear.ejecutar(calificacion)

    def obtenerCalificacion(self, filtro):
        return self.obtener.ejecutar(filtro)

    def actualizarCalificacion(self, calificacion, calificacionId):
        return self.actualizar.ejecutar(calificacion, calificacionId)

    def eliminarCalificacion(self, calificacionId):
        return self.eliminar.ejecutar(calificacionId)
