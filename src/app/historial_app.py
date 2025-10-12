import src.dominio.modelos.historial_mod as historial_mod
from src.dominio.puertos.historial_prt import HistorialPuerto
class HistoriaApp:
    def __init__(self, repo: HistorialPuerto):
        self.repo = repo

    def registrarHistorial(self, historial: dict):
        print(historial)
        return self.repo.registrarHistorial(historial_mod.HistorialModelo(**historial))

    def obtenerHistorial(self, usuario_id: str, libro: str = "" ):
        return self.repo.obtenerHistorial(usuario_id, libro)