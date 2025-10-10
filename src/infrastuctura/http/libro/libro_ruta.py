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

# Rutas de consulta
@libroRuta.route('/obtener', methods=['GET'])
@token_required
def obtener_libros():
    return libro_controlador.obtenerLibros()

@libroRuta.route('/obtener/<libro_id>', methods=['GET'])
@token_required
def obtener_libro(libro_id):
    return libro_controlador.obtenerLibro(libro_id)

@libroRuta.route('/buscar', methods=['GET', 'POST'])
@token_required
def buscar_libros():
    return libro_controlador.buscarLibros()

@libroRuta.route('/genero/<genero>', methods=['GET'])
@token_required
def obtener_por_genero(genero):
    return libro_controlador.obtenerLibrosPorGenero(genero)

@libroRuta.route('/autor/<autor>', methods=['GET'])
@token_required
def obtener_por_autor(autor):
    return libro_controlador.obtenerLibrosPorAutor(autor)

@libroRuta.route('/mejor-calificados', methods=['GET'])
@token_required
def obtener_mejor_calificados():
    return libro_controlador.obtenerMejorCalificados()

@libroRuta.route('/estadisticas', methods=['GET'])
@token_required
def obtener_estadisticas():
    return libro_controlador.obtenerEstadisticas()

# Rutas de modificación
@libroRuta.route('/crear', methods=['POST'])
@token_required
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

@libroRuta.route('/reactivar/<libro_id>', methods=['PUT'])
@token_required
def reactivar_libro(libro_id):
    return libro_controlador.reactivarLibro(libro_id)

@libroRuta.route('/calificar/<libro_id>', methods=['POST'])
@token_required
def calificar_libro(libro_id):
    return libro_controlador.calificarLibro(libro_id)


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


@libroRuta.route('/web/buscar', methods=['GET', 'POST'])
@login_required
def buscar_libros_web():
    return libro_controlador.buscarLibros()


@libroRuta.route('/web/genero/<genero>', methods=['GET'])
@login_required
def obtener_por_genero_web(genero):
    return libro_controlador.obtenerLibrosPorGenero(genero)


@libroRuta.route('/web/autor/<autor>', methods=['GET'])
@login_required
def obtener_por_autor_web(autor):
    return libro_controlador.obtenerLibrosPorAutor(autor)


@libroRuta.route('/web/mejor-calificados', methods=['GET'])
@login_required
def obtener_mejor_calificados_web():
    return libro_controlador.obtenerMejorCalificados()


@libroRuta.route('/web/estadisticas', methods=['GET'])
@login_required
def obtener_estadisticas_web():
    return libro_controlador.obtenerEstadisticas()


@libroRuta.route('/web/crear', methods=['POST'])
@login_required
def crear_libro_web_post():
    # reutiliza el método de creación (espera JSON en APIs), devolverá JSON
    return libro_controlador.crearLibro()


@libroRuta.route('/web/actualizar/<libro_id>', methods=['POST', 'PUT'])
@login_required
def actualizar_libro_web(libro_id):
    return libro_controlador.actualizarLibro(libro_id)


@libroRuta.route('/web/eliminar/<libro_id>', methods=['POST', 'DELETE'])
@login_required
def eliminar_libro_web(libro_id):
    return libro_controlador.eliminarLibro(libro_id)


@libroRuta.route('/web/reactivar/<libro_id>', methods=['POST', 'PUT'])
@login_required
def reactivar_libro_web(libro_id):
    return libro_controlador.reactivarLibro(libro_id)


@libroRuta.route('/web/calificar/<libro_id>', methods=['POST'])
@login_required
def calificar_libro_web(libro_id):
    return libro_controlador.calificarLibro(libro_id)