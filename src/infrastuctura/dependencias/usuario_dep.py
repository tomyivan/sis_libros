from src.infrastuctura.repositorio import usuario_rep
from src.app import usuario_app
from src.infrastuctura.http.usuario import usuario_ctl
from src.helpers import mongoconn_hlp
from src.dominio.servicios.usuario import crearUsuario_srv, obtenerUsuario_srv, autenticar_srv
connection = mongoconn_hlp.MongoConnection()
usuarioRepo = usuario_rep.UsuarioRepositorio(connection)

crearUsuarioSrv = crearUsuario_srv.CrearUsuarioServicio(usuarioRepo)
obtenerUsuarioSrv = obtenerUsuario_srv.ObtenerUsuarioServicio(usuarioRepo)
autenticarSrv = autenticar_srv.AutenticarServicio(obtenerUsuarioSrv)
usuario_app = usuario_app.UsuarioApp(usuarioRepo, crearUsuarioSrv, obtenerUsuarioSrv, autenticarSrv)
usuario_controlador = usuario_ctl.UsuarioControlador(usuario_app)
