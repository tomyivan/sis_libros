from flask import Blueprint
from src.infrastuctura.http.categoria.categoria_ctl import CategoriaControlador
from src.infrastuctura.http.autenticacion.auth_ctl import login_required, token_required
from src.infrastuctura.dependencias import categoria_dep

categoriaRuta = Blueprint('categoria', __name__, url_prefix='/categoria')

categoria_controlador = None

def init_categoria_routes():
    global categoria_controlador
    categoria_controlador = categoria_dep.categoria_controlador

@categoriaRuta.route('/obtener', methods=['GET'])
@token_required
def obtener_categorias():
    return categoria_controlador.obtenerCategorias()

@categoriaRuta.route('/obtener/<categoria_id>', methods=['GET'])
@token_required
def obtener_categoria(categoria_id):
    return categoria_controlador.obtenerCategoria(categoria_id)

@categoriaRuta.route('/crear', methods=['POST'])
@token_required
def crear_categoria():
    return categoria_controlador.crearCategoria()

@categoriaRuta.route('/actualizar/<categoria_id>', methods=['PUT'])
@token_required
def actualizar_categoria(categoria_id):
    return categoria_controlador.actualizarCategoria(categoria_id)

@categoriaRuta.route('/eliminar/<categoria_id>', methods=['DELETE','POST'])
@token_required
def eliminar_categoria(categoria_id):
    return categoria_controlador.eliminarCategoria(categoria_id)

# Web views
@categoriaRuta.route('/web/list', methods=['GET'])
@login_required
def lista_categorias_web():
    return categoria_controlador.lista_categorias()

@categoriaRuta.route('/web/create', methods=['GET','POST'])
@login_required
def crear_categoria_web():
    return categoria_controlador.crear_categoria_web()
