import bcrypt
from src.dominio.puertos import usuario_prt
from src.dominio.modelos import usuario_mod
class CrearUsuarioServicio:
    def __init__(self, usuario_repositorio: usuario_prt.UsuarioPuerto):
        self.usuario_repositorio = usuario_repositorio
    def __hash_password(self, password: str) -> str:
        print("entro")
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    def crearUsuario(self, usuario: usuario_mod.UsuarioModelo) -> str:
        usuario.password_hash = self.__hash_password(usuario.password_hash)
        return self.usuario_repositorio.crearUsuario(usuario)

    
        