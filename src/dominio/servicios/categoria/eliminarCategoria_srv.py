from src.dominio.puertos.categoria_prt import CategoriaPuerto

class EliminarCategoriaServicio:
    def __init__(self, repo: CategoriaPuerto):
        self.repo = repo

    def ejecutar(self, categoria_id: str):
        return self.repo.eliminarCategoria(categoria_id)
