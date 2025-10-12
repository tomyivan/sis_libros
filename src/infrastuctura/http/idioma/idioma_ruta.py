from flask import Blueprint
from src.infrastuctura.http.idioma.idioma_ctl import IdiomaControlador
from src.infrastuctura.http.autenticacion.auth_ctl import login_required, token_required
from src.infrastuctura.dependencias import idioma_dep

idiomaRuta = Blueprint('idioma', __name__, url_prefix='/idioma')

idioma_controlador = None

def init_idioma_routes():
    global idioma_controlador
    idioma_controlador = idioma_dep.idioma_controlador

@idiomaRuta.route('/obtener', methods=['GET'])
@token_required
def obtener_idiomas():
    return idioma_controlador.obtenerIdiomas()

@idiomaRuta.route('/obtener/<idioma_id>', methods=['GET'])
@token_required
def obtener_idioma(idioma_id):
    return idioma_controlador.obtenerIdioma(idioma_id)

@idiomaRuta.route('/crear', methods=['POST'])
@token_required
def crear_idioma():
    return idioma_controlador.crearIdioma()

@idiomaRuta.route('/actualizar/<idioma_id>', methods=['PUT'])
@token_required
def actualizar_idioma(idioma_id):
    return idioma_controlador.actualizarIdioma(idioma_id)

@idiomaRuta.route('/eliminar/<idioma_id>', methods=['DELETE','POST'])
@token_required
def eliminar_idioma(idioma_id):
    return idioma_controlador.eliminarIdioma(idioma_id)

# Web views
@idiomaRuta.route('/web/list', methods=['GET'])
@login_required
def lista_idiomas_web():
    return idioma_controlador.lista_idiomas()
