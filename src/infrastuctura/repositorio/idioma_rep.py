from src.custom.error_custom import APIError
from src.helpers.mongoconn_hlp import MongoConnection
from src.dominio.modelos import idioma_mod
from src.dominio.puertos import idioma_prt
from bson import ObjectId
from datetime import datetime
from typing import List


class IdiomaRepositorio(idioma_prt.IdiomaPuerto):
    def __init__(self, conexion: MongoConnection):
        self.db = conexion.conectar()
        self.collection = self.db.idiomas

    def crearIdioma(self, idioma: idioma_mod.IdiomaModelo) -> str:
        try:
            if idioma.fecha_creacion is None:
                idioma.fecha_creacion = datetime.now()
            result = self.collection.insert_one(idioma.__dict__)
            return str(result.inserted_id)
        except Exception as e:
            print(f"Error al crear idioma: {e}")
            raise APIError("Error al crear idioma")

    def obtenerIdioma(self, idioma_id: str) -> idioma_mod.IdiomaModeloDTO:
        try:
            doc = self.collection.find_one({"_id": ObjectId(idioma_id)})
            if not doc:
                return None
            doc['_id'] = str(doc['_id'])
            return idioma_mod.IdiomaModeloDTO(**doc)
        except Exception as e:
            print(f"Error al obtener idioma: {e}")
            raise APIError("Error al obtener idioma")

    def obtenerIdiomas(self) -> List[idioma_mod.IdiomaModeloDTO]:
        try:
            docs = self.collection.find().sort('fecha_creacion', -1)
            items = []
            for d in docs:
                d['_id'] = str(d['_id'])
                items.append(idioma_mod.IdiomaModeloDTO(**d))
            return items
        except Exception as e:
            print(f"Error al obtener idiomas: {e}")
            raise APIError("Error al obtener idiomas")

    def actualizarIdioma(self, idioma: idioma_mod.IdiomaModelo, idioma_id: str) -> int:
        try:
            idioma.fecha_creacion = idioma.fecha_creacion or None
            idioma.fecha_modificacion = datetime.now()
            result = self.collection.update_one({"_id": ObjectId(idioma_id)}, {"$set": idioma.__dict__})
            return result.modified_count
        except Exception as e:
            print(f"Error al actualizar idioma: {e}")
            raise APIError("Error al actualizar idioma")

    def eliminarIdioma(self, idioma_id: str) -> bool:
        try:
            result = self.collection.delete_one({"_id": ObjectId(idioma_id)})
            return result.deleted_count > 0
        except Exception as e:
            print(f"Error al eliminar idioma: {e}")
            raise APIError("Error al eliminar idioma")
