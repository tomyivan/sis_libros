import src.infrastuctura.dependencias.historial_dep as historial_dep
from flask import Blueprint, request
from src.infrastuctura.http.autenticacion.auth_ctl import token_required

historialRuta = Blueprint('historial', __name__, url_prefix='/historial')
historialCtl = None

def init_historial_routes():
    global historialCtl
    historialCtl = historial_dep.historialCtl

@historialRuta.route('/crear', methods=['POST'])
@token_required
def crear_historial():
    q = request.args.get('textoBusqueda', None)
    return historialCtl.crearHistorial()

@historialRuta.route('/obtener', methods=['GET'])
@token_required
def obtener_historial():
    q = request.args.get('textoBusqueda', None)
    return historialCtl.obtenerHistorial(q)
