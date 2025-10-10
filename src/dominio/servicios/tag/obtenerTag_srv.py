from src.dominio.puertos.tag_prt import TagPuerto

class ObtenerTagServicio:
    def __init__(self, repo: TagPuerto):
        self.repo = repo

    def ejecutar(self, tag_id: str):
        return self.repo.obtenerTag(tag_id)
