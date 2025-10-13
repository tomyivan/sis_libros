from flask import Flask, jsonify, redirect, url_for
from src.infrastuctura.http.usuario.usuario_ruta import usuarioRuta
from src.infrastuctura.http.autenticacion.auth_ruta import authRuta
from src.infrastuctura.http.libro.libro_ruta import libroRuta, init_libro_routes
from src.infrastuctura.http.categoria.categoria_ruta import categoriaRuta, init_categoria_routes
from src.infrastuctura.http.tag.tag_ruta import tagRuta, init_tag_routes
from src.infrastuctura.http.pais.pais_ruta import paisRuta, init_pais_routes
from src.infrastuctura.http.idioma.idioma_ruta import idiomaRuta, init_idioma_routes
from src.infrastuctura.http.autenticacion.auth_ctl import AuthControlador
from src.infrastuctura.http.genero.genero_ruta import generoRuta, init_genero_routes
from src.infrastuctura.http.historial.historial_ruta import historialRuta, init_historial_routes
from src.infrastuctura.http.comentario.comentario_ruta import comentarioRuta, init_comentario_routes
from src.infrastuctura.http.calificacion.calificacion_ruta import calificacionRuta, init_calificacion_routes
from src.custom.error_custom import APIError
from src.util.responseApi import ResponseApi
import dotenv
import os
import secrets

dotenv.load_dotenv()

app = Flask(__name__, template_folder='src/template')

# Configuración de sesiones
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', secrets.token_hex(16))
app.config['SESSION_COOKIE_SECURE'] = False  # True en producción con HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# Inicializar dependencias de libros
init_libro_routes()
# Inicializar dependencias de categorias
init_categoria_routes()
# Inicializar dependencias de tags
init_tag_routes()
# Inicializar dependencias de generos
init_genero_routes()
# Inicializar dependencias de paises
init_pais_routes()
# Inicializar dependencias de idiomas
init_idioma_routes()
# Inicializar dependencias de historial
init_historial_routes()
# Inicializar dependencias de comentarios (wires controlador)
init_comentario_routes()
# Inicializar dependencias de calificaciones (wires controlador y registra blueprint)
init_calificacion_routes()
# Registrar blueprints
app.register_blueprint(authRuta)
app.register_blueprint(usuarioRuta)
app.register_blueprint(libroRuta)
app.register_blueprint(categoriaRuta)
app.register_blueprint(tagRuta)
app.register_blueprint(generoRuta)
app.register_blueprint(paisRuta)
app.register_blueprint(idiomaRuta)
app.register_blueprint(historialRuta)
app.register_blueprint(comentarioRuta)
app.register_blueprint(calificacionRuta)
# Inicializar controlador de auth para rutas globales
auth_controller = AuthControlador()


@app.route('/')
def index():
    # Redirigir a dashboard si está autenticado, sino a login
    return redirect(url_for('auth.login'))

@app.route('/dashboard')
def dashboard():
    return auth_controller.dashboard()
@app.errorhandler(APIError)
def handle_api_error(error):
    return jsonify(ResponseApi.error(error.message, [])) 

if __name__ == '__main__':
    app.run(debug=True, port=int(os.getenv("PORT")))
