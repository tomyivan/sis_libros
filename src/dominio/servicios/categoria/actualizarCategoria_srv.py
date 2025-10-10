from src.dominio.puertos.categoria_prt import CategoriaPuerto
from src.dominio.modelos import categoria_mod
class ActualizarCategoriaServicio:
    def __init__(self, repo: CategoriaPuerto):
        self.repo = repo

    def ejecutar(self, categoria_id: str, categoria):
        return self.repo.actualizarCategoria(categoria_mod.CategoriaModelo(**categoria), categoria_id)
