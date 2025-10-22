from flask import request, jsonify, render_template, redirect, url_for, session, flash
from src.util.responseApi import ResponseApi
from marshmallow import Schema, fields, ValidationError
from src.app.auth_app import AuthApp
from src.app.libro_app import LibroApp
from src.dominio.servicios.libro.obtenerLibro_srv import ObtenerLibroServicio

import functools

class LoginSchema(Schema):
    alias = fields.String(required=True, validate=lambda x: len(x.strip()) > 0, 
                         error_messages={'required': 'El alias es requerido', 'invalid': 'El alias no puede estar vacío'})
    password = fields.String(required=True, validate=lambda x: len(x.strip()) > 0, 
                           error_messages={'required': 'La contraseña es requerida', 'invalid': 'La contraseña no puede estar vacía'})

class AuthControlador:
    def __init__(self, auth_service: AuthApp,
                 libroSrv: ObtenerLibroServicio
                 ):
        # Inicializar servicios
        # mongo_conn = MongoConnection()
        # usuario_repo = UsuarioRepositorio(mongo_conn)
        # obtener_usuario_srv = ObtenerUsuarioServicio(usuario_repo)
        # self.auth_service = AutenticarServicio(obtener_usuario_srv)
        self.auth_service = auth_service
        self.libroService = libroSrv

    def mostrar_login(self):
        """Muestra la pantalla de login"""
        if 'user_id' in session:
            return redirect(url_for('dashboard'))
        return render_template('auth/login.html')
    def nuevo_usuario(self):

        return render_template('auth/create.html')
    def login(self):
        """Procesa el login del usuario"""
        try:
            if request.method == 'GET':
                return self.mostrar_login()
            
            # Validar datos del formulario
            data = request.get_json() if request.is_json else request.form.to_dict()
            
            schema = LoginSchema()
            validated_data = schema.load(data)
            
            # Autenticar usuario
            auth_result = self.auth_service.autenticarUsuario(
                validated_data['alias'], 
                validated_data['password']
            )
            print(auth_result)
            if auth_result:
                # Guardar información en la sesión
                session['user_id'] = auth_result.idUsuario
                session['user_name'] = auth_result.usuario
                session['user_alias'] = auth_result.alias
                # Nota: ya no almacenamos ni usamos tokens para validación en el servidor web; se valida por sesión
                session['rol'] = auth_result.rol
                
                # Respuesta diferente según el tipo de request
                if request.is_json:
                    return jsonify(ResponseApi.exito({
                        'message': 'Login exitoso',
                        'user': {
                            'id': auth_result.idUsuario,
                            'name': auth_result.usuario,
                            'alias': auth_result.alias,
                            'rol': auth_result.rol
                        }
                    }, 200))
                else:
                    flash('¡Bienvenido!', 'success')
                    return redirect(url_for('dashboard'))
            else:
                error_msg = 'Alias o contraseña incorrectos'
                if request.is_json:
                    return jsonify(ResponseApi.error(error_msg, 401))
                else:
                    flash(error_msg, 'error')
                    return render_template('auth/login.html')
                    
        except ValidationError as e:
            print(f"Error de validación: {e.messages}")
            error_msg = f"Error de validación: {e.messages}"
            if request.is_json:
                return jsonify(ResponseApi.error(error_msg, 400))
            else:
                flash(error_msg, 'error')
                return render_template('auth/login.html')
        except Exception as e:
            print(f"Error en el servidor: {str(e)}")
            error_msg = f"Error en el servidor: {str(e)}"
            if request.is_json:
                return jsonify(ResponseApi.error(error_msg, 500))
            else:
                flash(error_msg, 'error')
                return render_template('auth/login.html')
    
    def logout(self):
        """Cierra la sesión del usuario"""
        session.clear()
        flash('Sesión cerrada correctamente', 'info')
        return redirect(url_for('auth.login'))
    
    def dashboard(self):
        """Pantalla principal después del login"""
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        
        user_data = {
            'id': session.get('user_id'),
            'name': session.get('user_name'),
            'alias': session.get('user_alias'),
            'rol': session.get('rol')
        }
        total = self.libroService.totalLibros()
        print(session.get('rol')    )
        return render_template('dashboard/dashboard.html', user=user_data, totalLibros=total)
    


    def verificar_token_api(self):
        """Endpoint para verificar token (para APIs)"""
        try:
            # Ahora validamos por sesión: si hay user_id en sesión, devolvemos datos del usuario
            if 'user_id' not in session:
                return jsonify(ResponseApi.error('Autenticación requerida', 401))

            user_data = {
                'id': session.get('user_id'),
                'name': session.get('user_name'),
                'alias': session.get('user_alias'),
                'rol': session.get('rol')
            }
            return jsonify(ResponseApi.exito(user_data, 200))
        except Exception as e:
            return jsonify(ResponseApi.error(f'Error al verificar token: {str(e)}', 500))


# Decorador para proteger rutas
def login_required(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            if request.is_json:
                return jsonify(ResponseApi.error('Autenticación requerida', 401))
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

# Decorador para proteger APIs con token
def token_required(f):
    """Decorator para proteger rutas de API usando sesión en lugar de tokens.
    Si se necesita autenticación por token (API externa), podría añadirse un nuevo decorador.
    """
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        # Validación basada en sesión
        if 'user_id' not in session:
            return jsonify(ResponseApi.error('Autenticación requerida', 401) )
        # Rellenar current_user con la información de la sesión para que los controladores la usen
        request.current_user = {
            'id': session.get('user_id'),
            'name': session.get('user_name'),
            'alias': session.get('user_alias'),
            'rol': session.get('rol')
        }
        return f(*args, **kwargs)

    return decorated_function