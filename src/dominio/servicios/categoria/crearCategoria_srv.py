from src.dominio.puertos.categoria_prt import CategoriaPuerto
from src.dominio.modelos import categoria_mod
class CrearCategoriaServicio:
    def __init__(self, repo: CategoriaPuerto):
        self.repo = repo

    def ejecutar(self, categoria):
        return self.repo.crearCategoria(categoria_mod.CategoriaModelo(**categoria))
