from flask import Blueprint
from src.infrastuctura.http.libro.libro_ctl import LibroControlador
from src.infrastuctura.http.autenticacion.auth_ctl import token_required
from src.infrastuctura.http.autenticacion.auth_ctl import login_required
from src.infrastuctura.dependencias import libro_dep

# Crear blueprint para libros
libroRuta = Blueprint('libro', __name__, url_prefix='/libro')

# Controlador se inicializa en dependencias
libro_controlador = None

def init_libro_routes():
    """Inicializar controlador desde dependencias"""
    global libro_controlador
    libro_controlador = libro_dep.libro_controlador




@libroRuta.route('/obtener', methods=['GET'])
@token_required
def obtener_libros():
    return libro_controlador.obtenerLibros()

@libroRuta.route('/obtener/<libro_id>', methods=['GET'])
@token_required
def obtener_libro(libro_id):
    return libro_controlador.obtenerLibro(libro_id)



# Rutas de modificación
@libroRuta.route('/crear', methods=['POST'])
# comentar el si es neseario para la prueba
# @token_required
def crear_libro():
    return libro_controlador.crearLibro()

@libroRuta.route('/actualizar/<libro_id>', methods=['PUT'])
@token_required
def actualizar_libro(libro_id):
    return libro_controlador.actualizarLibro(libro_id)

@libroRuta.route('/eliminar/<libro_id>', methods=['DELETE'])
@token_required
def eliminar_libro(libro_id):
    return libro_controlador.eliminarLibro(libro_id)




# Vistas web sencillas
@libroRuta.route('/web/list', methods=['GET'])
@login_required
def lista_libros_web():
    return libro_controlador.lista_libros()


@libroRuta.route('/web/create', methods=['GET', 'POST'])
@login_required
def crear_libro_web():
    return libro_controlador.crear_libro_web()


# Rutas web adicionales que envuelven los métodos del controlador
@libroRuta.route('/web/obtener', methods=['GET'])
@login_required
def obtener_libros_web():
    return libro_controlador.obtenerLibros()


@libroRuta.route('/web/obtener/<libro_id>', methods=['GET'])
@login_required
def obtener_libro_web(libro_id):
    return libro_controlador.obtenerLibro(libro_id)





@libroRuta.route('/web/crear', methods=['POST'])
@login_required
def crear_libro_web_post():
    # reutiliza el método de creación (espera JSON en APIs), devolverá JSON
    return libro_controlador.crearLibro()


@libroRuta.route('/web/actualizar/<libro_id>', methods=['POST', 'PUT'])
@login_required
def actualizar_libro_web(libro_id):
    return libro_controlador.actualizarLibro(libro_id)

# Rutas de consulta
@libroRuta.route('/info/<libro_id>', methods=['GET'])
@token_required
def obtener_libro_info(libro_id):
    return libro_controlador.libro_web_view(libro_id)
