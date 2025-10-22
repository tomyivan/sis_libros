from abc import ABC, abstractmethod
from typing import List
from src.dominio.modelos.interaccion_mod import ComentarioModelo, CalificacionModelo, VisualizacionModelo


class InteraccionPuerto(ABC):
    @abstractmethod
    def guardar_comentario(self, comentario: ComentarioModelo) -> None:
        raise NotImplementedError

    @abstractmethod
    def guardar_calificacion(self, calificacion: CalificacionModelo) -> None:
        raise NotImplementedError

    @abstractmethod
    def registrar_visualizacion(self, visualizacion: VisualizacionModelo) -> None:
        raise NotImplementedError

    @abstractmethod
    def obtener_comentarios_por_libro(self, id_libro: str) -> List[ComentarioModelo]:
        raise NotImplementedError
