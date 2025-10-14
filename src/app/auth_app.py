from src.dominio.servicios.usuario.autenticar_srv import AutenticarServicio

class AuthApp:
    def __init__(self, autenticar: AutenticarServicio):
        # Guardamos la dependencia con un nombre que no choque con métodos públicos
        self.autenticar_srv = autenticar

    def autenticarUsuario(self, alias, password):
        # Método público esperado por los controladores
        return self.autenticar_srv.autenticar(alias, password)