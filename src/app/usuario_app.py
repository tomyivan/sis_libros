from src.dominio.puertos import usuario_prt
from src.dominio.servicios.usuario import crearUsuario_srv, obtenerUsuario_srv, autenticar_srv
from src.dominio.modelos import usuario_mod, auth_mod
class UsuarioApp:
    def __init__(self, repositorio: usuario_prt.UsuarioPuerto,
                 crearUsuarioSrv: crearUsuario_srv.CrearUsuarioServicio,
                 obtenerUsuarioSrv: obtenerUsuario_srv.ObtenerUsuarioServicio,
                 autenticarSrv: autenticar_srv.AutenticarServicio
                 ):
        self.repositorio = repositorio
        self.crearUsuarioSrv = crearUsuarioSrv
        self.obtenerUsuarioSrv = obtenerUsuarioSrv
        self.autenticarSrv = autenticarSrv
    def obtenerUsuario(self, idUsuario: int) -> dict | None:
        return self.obtenerUsuarioSrv.obtenerUsuario({"_id": idUsuario})
        
    def obtenerUsuarios(self, filtro: usuario_mod.FiltroUsuarioModelo):
        return self.obtenerUsuarioSrv.obtenerUsuarios(filtro)
    def crearUsuario(self, usuario: usuario_mod.UsuarioModelo):
        return self.crearUsuarioSrv.crearUsuario(usuario)
    def actualizarUsuario(self, usuario: usuario_mod.UsuarioModelo):
        return self.repositorio.actualizarUsuario(usuario)
    def desactivarUsuario(self, idUsuario: int):
        return self.repositorio.desactivarUsuario(idUsuario)

    def autenticarUsuario(self, alias: str, password: str) -> auth_mod.AuthModelo | None:
        return self.autenticarSrv.autenticar(alias, password)
