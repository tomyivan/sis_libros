from flask import Blueprint, request
from src.infrastuctura.http.autenticacion.auth_ctl import AuthControlador

# Crear blueprint para autenticación
authRuta = Blueprint('auth', __name__, url_prefix='/auth')

# Inicializar controlador
auth_controller = AuthControlador()

# Rutas de autenticación
@authRuta.route('/login', methods=['GET', 'POST'])
def login():
    return auth_controller.login()

@authRuta.route('/logout', methods=['POST', 'GET'])
def logout():
    return auth_controller.logout()

@authRuta.route('/verify-token', methods=['POST'])
def verify_token():
    return auth_controller.verificar_token_api()

# Ruta para mostrar el dashboard después del login
@authRuta.route('/dashboard')
def dashboard():
    return auth_controller.dashboard()