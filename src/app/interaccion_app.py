from typing import List
from src.dominio.servicios.interaccion.interaccion_srv import InteraccionServicio
from src.dominio.modelos.interaccion_mod import ComentarioModelo


class InteraccionApp:
    def __init__(self, interaccion_servicio: InteraccionServicio):
        self._servicio = interaccion_servicio

    def comentar_libro(self, id_usuario: str, id_libro: str, texto: str) -> None:
        self._servicio.comentar(id_usuario, id_libro, texto)

    def calificar_libro(self, id_usuario: str, id_libro: str, calificacion: float) -> None:
        self._servicio.calificar(id_usuario, id_libro, calificacion)

    def ver_libro(self, id_usuario: str, id_libro: str) -> None:
        self._servicio.ver(id_usuario, id_libro)

    def obtener_comentarios(self, id_libro: str) -> List[ComentarioModelo]:
        return self._servicio.obtener_comentarios(id_libro)
