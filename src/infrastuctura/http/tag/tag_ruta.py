from flask import Blueprint
from src.infrastuctura.http.tag.tag_ctl import TagControlador
from src.infrastuctura.http.autenticacion.auth_ctl import login_required, token_required
from src.infrastuctura.dependencias import tag_dep

tagRuta = Blueprint('tag', __name__, url_prefix='/tag')

tag_controlador = None

def init_tag_routes():
    global tag_controlador
    tag_controlador = tag_dep.tag_controlador

@tagRuta.route('/obtener', methods=['GET'])
@token_required
def obtener_tags():
    return tag_controlador.obtenerTags()

@tagRuta.route('/obtener/<tag_id>', methods=['GET'])
@token_required
def obtener_tag(tag_id):
    return tag_controlador.obtenerTag(tag_id)

@tagRuta.route('/crear', methods=['POST'])
@token_required
def crear_tag():
    return tag_controlador.crearTag()

@tagRuta.route('/actualizar/<tag_id>', methods=['PUT'])
@token_required
def actualizar_tag(tag_id):
    return tag_controlador.actualizarTag(tag_id)

@tagRuta.route('/eliminar/<tag_id>', methods=['DELETE','POST'])
@token_required
def eliminar_tag(tag_id):
    return tag_controlador.eliminarTag(tag_id)

# Web views
@tagRuta.route('/web/list', methods=['GET'])
@login_required
def lista_tags_web():
    return tag_controlador.lista_tags()

@tagRuta.route('/web/create', methods=['GET','POST'])
@login_required
def crear_tag_web():
    return tag_controlador.crear_tag_web()
