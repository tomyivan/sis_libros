from src.dominio.servicios.recomendacion import recomendacionPorContenido_srv
class RecomendarApp:
    def __init__(self, recomendarPorContenidoServicio: recomendacionPorContenido_srv.RecomendarPorContenido):
        self.recomendarPorContenidoServicio = recomendarPorContenidoServicio

    def ejecutarRecomendacion(self) -> bool:
        return self.recomendarPorContenidoServicio.recomendarPorContenido()