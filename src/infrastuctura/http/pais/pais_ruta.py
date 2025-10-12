from flask import Blueprint
from src.infrastuctura.http.pais.pais_ctl import PaisControlador
from src.infrastuctura.http.autenticacion.auth_ctl import login_required, token_required
from src.infrastuctura.dependencias import pais_dep

paisRuta = Blueprint('pais', __name__, url_prefix='/pais')

pais_controlador = None

def init_pais_routes():
    global pais_controlador
    pais_controlador = pais_dep.pais_controlador

@paisRuta.route('/obtener', methods=['GET'])
@token_required
def obtener_paises():
    return pais_controlador.obtenerPaises()

@paisRuta.route('/obtener/<pais_id>', methods=['GET'])
@token_required
def obtener_pais(pais_id):
    return pais_controlador.obtenerPais(pais_id)

@paisRuta.route('/crear', methods=['POST'])
@token_required
def crear_pais():
    return pais_controlador.crearPais()

@paisRuta.route('/actualizar/<pais_id>', methods=['PUT'])
@token_required
def actualizar_pais(pais_id):
    return pais_controlador.actualizarPais(pais_id)

@paisRuta.route('/eliminar/<pais_id>', methods=['DELETE','POST'])
@token_required
def eliminar_pais(pais_id):
    return pais_controlador.eliminarPais(pais_id)

# Web views
@paisRuta.route('/web/list', methods=['GET'])
@login_required
def lista_paises_web():
    return pais_controlador.lista_paises()
