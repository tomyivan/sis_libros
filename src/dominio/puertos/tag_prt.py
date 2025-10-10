from abc import ABC, abstractmethod
from typing import List
from src.dominio.modelos.tag_mod import TagModelo, TagModeloDTO

class TagPuerto(ABC):
    @abstractmethod
    def crearTag(self, tag: TagModelo) -> str:
        pass

    @abstractmethod
    def obtenerTag(self, tag_id: str) -> TagModeloDTO:
        pass

    @abstractmethod
    def obtenerTags(self) -> List[TagModeloDTO]:
        pass

    @abstractmethod
    def actualizarTag(self, tag: TagModelo, tag_id: str) -> int:
        pass

    @abstractmethod
    def eliminarTag(self, tag_id: str) -> bool:
        pass
