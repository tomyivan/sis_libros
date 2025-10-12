from flask import Blueprint
from src.infrastuctura.http.genero.genero_ctl import GeneroControlador
from src.infrastuctura.http.autenticacion.auth_ctl import login_required, token_required
from src.infrastuctura.dependencias import genero_dep

generoRuta = Blueprint('genero', __name__, url_prefix='/genero')

genero_controlador = None

def init_genero_routes():
    global genero_controlador
    genero_controlador = genero_dep.genero_controlador

@generoRuta.route('/obtener', methods=['GET'])
@token_required
def obtener_generos():
    return genero_controlador.obtenerGeneros()

@generoRuta.route('/obtener/<genero_id>', methods=['GET'])
@token_required
def obtener_genero(genero_id):
    return genero_controlador.obtenerGenero(genero_id)

@generoRuta.route('/crear', methods=['POST'])
@token_required
def crear_genero():
    return genero_controlador.crearGenero()

@generoRuta.route('/actualizar/<genero_id>', methods=['PUT'])
@token_required
def actualizar_genero(genero_id):
    return genero_controlador.actualizarGenero(genero_id)

@generoRuta.route('/eliminar/<genero_id>', methods=['DELETE','POST'])
@token_required
def eliminar_genero(genero_id):
    return genero_controlador.eliminarGenero(genero_id)

# Web views
@generoRuta.route('/web/list', methods=['GET'])
@login_required
def lista_generos_web():
    return genero_controlador.lista_generos()