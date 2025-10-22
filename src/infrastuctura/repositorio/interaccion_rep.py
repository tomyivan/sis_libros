import json
from typing import List
from src.dominio.puertos.interaccion_prt import InteraccionPuerto
from src.dominio.modelos.interaccion_mod import ComentarioModelo, CalificacionModelo, VisualizacionModelo
from src.helpers.redisconn_hlp import redCli


class InteraccionRepositorio(InteraccionPuerto):
    """Repositorio que guarda todas las interacciones en un ZSET global llamado 'interaccion'.

    No persiste en Mongo según la petición del usuario.
    """

    GLOBAL_ZSET = 'interaccion'

    def __init__(self):
        self._redis = redCli

    def _member(self, id_libro: str, id_usuario: str) -> str:
        # representamos el miembro como JSON para facilitar extracción posterior
        return json.dumps({'id_libro': id_libro, 'id_usuario': id_usuario})

    def _zadd_increment(self, member: str, score: float) -> None:
        try:
            # Zincrby para acumular el score por miembro
            self._redis.zincrby(self.GLOBAL_ZSET, score, member)
        except Exception:
            # no lanzamos excepción para no bloquear la app
            pass

    def guardar_comentario(self, comentario: ComentarioModelo) -> None:
        member = self._member(comentario.id_libro, comentario.id_usuario)
        score = 2.0
        self._zadd_increment(member, score)

    def guardar_calificacion(self, calificacion: CalificacionModelo) -> None:
        member = self._member(calificacion.id_libro, calificacion.id_usuario)
        score = float(calificacion.calificacion) * 2.0
        self._zadd_increment(member, score)

    def registrar_visualizacion(self, visualizacion: VisualizacionModelo) -> None:
        member = self._member(visualizacion.id_libro, visualizacion.id_usuario)
        score = 1.0
        self._zadd_increment(member, score)

    def obtener_comentarios_por_libro(self, id_libro: str) -> List[ComentarioModelo]:
        # Dado que no guardamos comentarios en Mongo, no hay forma directa de
        # recuperar el texto del comentario desde Redis si sólo guardamos scores.
        # Por eso esta función devuelve lista vacía o podría extraer miembros que
        # correspondan al libro y devolver instancias mínimas sin texto.
        resultados: List[ComentarioModelo] = []
        try:
            # obtener todos los miembros y filtrar por id_libro
            items = self._redis.zrange(self.GLOBAL_ZSET, 0, -1)
            for m in items:
                try:
                    obj = json.loads(m)
                    if obj.get('id_libro') == id_libro:
                        # no tenemos el texto del comentario en el ZSET
                        resultados.append(ComentarioModelo(id_usuario=obj.get('id_usuario'), id_libro=id_libro, texto='', fecha=None))
                except Exception:
                    continue
        except Exception:
            pass
        return resultados
