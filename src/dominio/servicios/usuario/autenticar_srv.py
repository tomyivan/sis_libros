from src.dominio.modelos import auth_mod
from src.dominio.servicios.usuario import obtenerUsuario_srv
import bcrypt
class AutenticarServicio:
    def __init__(self, obtenerUsuarioSrv: obtenerUsuario_srv.ObtenerUsuarioServicio):
        self.obtenerUsuarioSrv = obtenerUsuarioSrv

    def autenticar(self, alias: str, password: str) -> auth_mod.AuthModelo:
        try:
            # Obtener el usuario por alias
            usuario = self.obtenerUsuarioSrv.obtenerUsuario({"alias": alias})
            if not usuario:
                print(f"Usuario no encontrado para alias: {alias}")
                return None
                
            if not usuario.password_hash:
                print("Usuario no tiene password_hash")
                return None
                
            # Verificar contraseña
            if bcrypt.checkpw(password.encode('utf-8'), usuario.password_hash.encode('utf-8')):
                # Asegurar que el ID es string
                user_id = str(usuario._id)
                
                # No generamos ni devolvemos tokens; la sesión del servidor controlará la autenticación web
                return auth_mod.AuthModelo(
                    token=None,
                    rol=usuario.rol,
                    idUsuario=user_id,
                    usuario=usuario.nombre,
                    alias=usuario.alias
                )
            else:
                print("Contraseña incorrecta")
                return None
                
        except Exception as e:
            print(f"Error durante autenticación: {str(e)}")
            return None
    
    # JWT token helpers removed: authentication is session-based for the web app
