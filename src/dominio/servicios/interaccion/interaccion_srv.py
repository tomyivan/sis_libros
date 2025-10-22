from datetime import datetime
from typing import List
from src.dominio.puertos.interaccion_prt import InteraccionPuerto
from src.dominio.modelos.interaccion_mod import ComentarioModelo, CalificacionModelo, VisualizacionModelo


class InteraccionServicio:
    def __init__(self, interaccion_puerto: InteraccionPuerto):
        self._puerto = interaccion_puerto

    def comentar(self,  id_libro: str, texto: str, idUsuario: str) -> None:
        if not texto or texto.strip() == '':
            raise ValueError('El comentario no puede estar vacío')
        comentario = ComentarioModelo(id_usuario=idUsuario, id_libro=id_libro, texto=texto.strip(), fecha=datetime.utcnow())
        self._puerto.guardar_comentario(comentario)

    def calificar(self,  id_libro: str, calificacion: float, idUsuario: str) -> None:
        if calificacion is None:
            raise ValueError('Calificación requerida')
        if calificacion < 0 or calificacion > 5:
            raise ValueError('La calificación debe estar entre 0 y 5')
        cal = CalificacionModelo(id_usuario=idUsuario, id_libro=id_libro, calificacion=float(calificacion), fecha=datetime.utcnow())
        self._puerto.guardar_calificacion(cal)

    def ver(self, id_libro: str, idUsuario: str) -> None:   
        vista = VisualizacionModelo(id_usuario=idUsuario, id_libro=id_libro, fecha=datetime.utcnow())
        self._puerto.registrar_visualizacion(vista)

    def obtener_comentarios(self, id_libro: str) -> List[ComentarioModelo]:
        return self._puerto.obtener_comentarios_por_libro(id_libro)
