from flask import Blueprint
from src.infrastuctura.dependencias import comentario_dep
from src.infrastuctura.http.autenticacion.auth_ctl import token_required

comentarioRuta = Blueprint('comentario', __name__, url_prefix='/comentario')

comentario_controlador = None

def init_comentario_routes():
    global comentario_controlador
    comentario_controlador = comentario_dep.comentario_controlador


@comentarioRuta.route('/crear', methods=['POST'])
@token_required
def crear_comentario():
    return comentario_controlador.crearComentario()


@comentarioRuta.route('/obtener', methods=['GET'])
@token_required
def obtener_comentarios():
    return comentario_controlador.obtenerComentario()


@comentarioRuta.route('/actualizar/<comentarioId>', methods=['PUT'])
@token_required
def actualizar_comentario(comentarioId):
    return comentario_controlador.actualizarComentario(comentarioId)


@comentarioRuta.route('/eliminar/<comentarioId>', methods=['DELETE'])
@token_required
def eliminar_comentario(comentarioId):
    return comentario_controlador.eliminarComentario(comentarioId)
