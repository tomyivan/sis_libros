from flask import Blueprint
from src.infrastuctura.dependencias import usuario_dep
from src.infrastuctura.http.autenticacion.auth_ctl import token_required, login_required
usuarioRuta = Blueprint('usuario', __name__, url_prefix='/usuario')

@usuarioRuta.route('/obtener', methods=['GET'])
@token_required
def obtener_usuario():
    return usuario_dep.usuario_controlador.obtenerUsuarios()

@usuarioRuta.route('/obtener/<idUsuario>', methods=['GET'])
@token_required
def obtenerUsuarioId(idUsuario):
    return usuario_dep.usuario_controlador.obtenerUsuario(idUsuario)

@usuarioRuta.route('/crear', methods=['POST'])
@token_required
def crear_usuario():
    return usuario_dep.usuario_controlador.crearUsuario()

@usuarioRuta.route('/actualizar', methods=['PUT'])
@token_required
def actualizar_usuario():
    return usuario_dep.usuario_controlador.actualizarUsuario()

@usuarioRuta.route('/desactivar', methods=['DELETE'])
@token_required
def desactivar_usuario():
    return usuario_dep.usuario_controlador.desactivarUsuario()

@usuarioRuta.route('/autenticar', methods=['POST'])
def autenticar_usuario():
    return usuario_dep.usuario_controlador.autenticarUsuario()