from abc import ABC, abstractmethod

class PublicacionPuerto(ABC):
    @abstractmethod
    def nuevaPublicacion(self, idLibro: str) -> bool:
        pass

    @abstractmethod
    def obtenerPublicaciones(self) -> list:
        pass
    