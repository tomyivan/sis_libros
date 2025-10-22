from src.dominio.puertos import comentario_prt
from src.dominio.modelos import comentarios_mod
from src.dominio.servicios.interaccion import interaccion_srv

class CrearComentarioServicio:
    def __init__(self, repo: comentario_prt.ComentarioPuerto,
                    interaccionSrv: interaccion_srv.InteraccionServicio):
        self.repo = repo
        self.interaccionSrv = interaccionSrv

    def crearComentario(self, comentario: comentarios_mod.ComentarioModelo) -> str:
        self.interaccionSrv.comentar(comentario.id_libro, comentario.texto, comentario.id_usuario)
        return self.repo.crearComentario(comentario)
