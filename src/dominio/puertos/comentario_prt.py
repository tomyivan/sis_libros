from abc import ABC, abstractmethod
from typing import List
from src.dominio.modelos.comentarios_mod import ComentarioModelo, ComentarioModeloDTO, FiltroComentarioModelo

class ComentarioPuerto(ABC):
    @abstractmethod
    def crearComentario(self, comentario: ComentarioModelo) -> str:
        pass

    @abstractmethod
    def obtenerComentario(self, filtro: FiltroComentarioModelo) -> ComentarioModeloDTO:
        pass

    @abstractmethod
    def actualizarComentario(self, comentario: ComentarioModelo, comentarioId: str) -> int:
        pass

    @abstractmethod
    def eliminarComentario(self, comentarioId: str) -> bool:
        pass
