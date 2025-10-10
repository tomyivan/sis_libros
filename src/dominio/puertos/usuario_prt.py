# Se define la interfaz para las operaciones relacionadas con usuarios.
from abc import ABC, abstractmethod
from src.dominio.modelos import usuario_mod
class UsuarioPuerto(ABC):
    @abstractmethod
    def obtenerUsuarios(self, filtro: usuario_mod.FiltroUsuarioModelo) -> list[usuario_mod.UsuarioModeloDTO]:
        pass

    @abstractmethod
    def obtenerUsuario(self, filtro: usuario_mod.FiltroUsuarioModelo) -> usuario_mod.UsuarioModeloDTO:
        pass

    @abstractmethod
    def crearUsuario(self, usuario: usuario_mod.UsuarioModelo) -> str:
        pass

    @abstractmethod
    def actualizarUsuario(self, usuario: usuario_mod.UsuarioModelo) -> str:
        pass

    @abstractmethod
    def desactivarUsuario(self, idUsuario: int) -> bool:
        pass

