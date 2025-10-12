from typing import List
from src.dominio.modelos import usuario_mod
from src.dominio.puertos import usuario_prt

class ObtenerUsuarioServicio:
    def __init__(self, repositorio: usuario_prt.UsuarioPuerto):
        self.repositorio = repositorio

    def obtenerUsuario(self, filtro) -> usuario_mod.UsuarioModeloDTO:
        """
        Obtener usuario por filtro (puede ser dict o FiltroUsuarioModelo)
        """
        if isinstance(filtro, dict):
            if "alias" in filtro:
                return self.repositorio.obtenerUsuarioPorAlias(filtro["alias"])
            else:
                filtro_obj = usuario_mod.FiltroUsuarioModelo(**filtro)
                return self.repositorio.obtenerUsuario(filtro_obj)
        else:
            return self.repositorio.obtenerUsuario(filtro)
        
    def obtenerUsuarios(self, filtro: usuario_mod.FiltroUsuarioModelo) -> List[usuario_mod.UsuarioModeloDTO]:
        return self.repositorio.obtenerUsuarios(filtro=filtro)
