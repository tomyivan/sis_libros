from flask import Blueprint
from src.infrastuctura.dependencias import calificacion_dep
from src.infrastuctura.http.autenticacion.auth_ctl import token_required

calificacionRuta = Blueprint('calificacion', __name__, url_prefix='/calificacion')

calificacion_controlador = None

def init_calificacion_routes():
    global calificacion_controlador
    calificacion_controlador = calificacion_dep.calificacion_controlador


@calificacionRuta.route('/crear', methods=['POST'])
@token_required
def crear_calificacion():
    return calificacion_controlador.crearCalificacion()


@calificacionRuta.route('/obtener', methods=['GET'])
@token_required
def obtener_calificaciones():
    return calificacion_controlador.obtenerCalificacion()


@calificacionRuta.route('/actualizar/<calificacionId>', methods=['PUT'])
@token_required
def actualizar_calificacion(calificacionId):
    return calificacion_controlador.actualizarCalificacion(calificacionId)


@calificacionRuta.route('/eliminar/<calificacionId>', methods=['DELETE'])
@token_required
def eliminar_calificacion(calificacionId):
    return calificacion_controlador.eliminarCalificacion(calificacionId)
