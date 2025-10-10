from src.custom.error_custom import APIError
from src.helpers.mongoconn_hlp import MongoConnection
from src.dominio.modelos import tag_mod
from src.dominio.puertos import tag_prt
from bson import ObjectId
from datetime import datetime
from typing import List

class TagRepositorio(tag_prt.TagPuerto):
    def __init__(self, conexion: MongoConnection):
        self.db = conexion.conectar()
        self.collection = self.db.tags

    def crearTag(self, tag: tag_mod.TagModelo) -> str:
        try:
            if tag.fecha_creacion is None:
                tag.fecha_creacion = datetime.now()
            result = self.collection.insert_one(tag.__dict__)
            return str(result.inserted_id)
        except Exception as e:
            print(f"Error al crear tag: {e}")
            raise APIError("Error al crear tag")

    def obtenerTag(self, tag_id: str) -> tag_mod.TagModeloDTO:
        try:
            doc = self.collection.find_one({"_id": ObjectId(tag_id)})
            if not doc:
                return None
            doc['_id'] = str(doc['_id'])
            return tag_mod.TagModeloDTO(**doc)
        except Exception as e:
            print(f"Error al obtener tag: {e}")
            raise APIError("Error al obtener tag")

    def obtenerTags(self) -> List[tag_mod.TagModeloDTO]:
        try:
            docs = self.collection.find().sort('fecha_creacion', -1)
            tags = []
            for d in docs:
                d['_id'] = str(d['_id'])
                tags.append(tag_mod.TagModeloDTO(**d))
            return tags
        except Exception as e:
            print(f"Error al obtener tags: {e}")
            raise APIError("Error al obtener tags")

    def actualizarTag(self, tag: tag_mod.TagModelo, tag_id: str) -> int:
        try:
            tag.fecha_modificacion = datetime.now()
            result = self.collection.update_one({"_id": ObjectId(tag_id)}, {"$set": tag.__dict__})
            return result.modified_count
        except Exception as e:
            print(f"Error al actualizar tag: {e}")
            raise APIError("Error al actualizar tag")

    def eliminarTag(self, tag_id: str) -> bool:
        try:
            result = self.collection.delete_one({"_id": ObjectId(tag_id)})
            return result.deleted_count > 0
        except Exception as e:
            print(f"Error al eliminar tag: {e}")
            raise APIError("Error al eliminar tag")
