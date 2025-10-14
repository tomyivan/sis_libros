from src.dominio.servicios.usuario.obtenerUsuario_srv import ObtenerUsuarioServicio
from src.helpers.mongoconn_hlp import MongoConnection
from src.dominio.servicios.usuario.autenticar_srv import AutenticarServicio
from src.dominio.servicios.usuario.obtenerUsuario_srv import ObtenerUsuarioServicio
from src.infrastuctura.repositorio.usuario_rep import UsuarioRepositorio
from src.app.auth_app import AuthApp
from src.infrastuctura.http.autenticacion.auth_ctl import AuthControlador

mongo_conn = MongoConnection()
usuario_repo = UsuarioRepositorio(mongo_conn)
obtener_usuario_srv = ObtenerUsuarioServicio(usuario_repo)
auth = AutenticarServicio(obtener_usuario_srv)
auth_app = AuthApp(auth)

auth_controller = AuthControlador(auth_app)