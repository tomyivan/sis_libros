from src.infrastuctura.dependencias.publicacion_dep import pubCtl
from flask import Blueprint
publicacionRuta = Blueprint('publicacion', __name__, url_prefix='/publicacion')
@publicacionRuta.route('/obtener', methods=['GET'])
def obtener_publicaciones():
    return pubCtl.obtenerPublicaciones()