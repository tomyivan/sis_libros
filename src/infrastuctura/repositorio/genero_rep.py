from src.custom.error_custom import APIError
from src.helpers.mongoconn_hlp import MongoConnection
from src.dominio.modelos import genero_mod
from src.dominio.puertos import genero_prt
from bson import ObjectId
from datetime import datetime
from typing import List, Optional


class GeneroRepositorioMongo(genero_prt.GeneroRepositorio):
    def __init__(self, conexion: MongoConnection):
        self.db = conexion.conectar()
        self.collection = self.db.generos

    def crear_genero(self, genero: genero_mod.GeneroModelo) -> str:
        try:
            if genero.fecha_creacion is None:
                genero.fecha_creacion = datetime.now()
            result = self.collection.insert_one(genero.__dict__)
            return str(result.inserted_id)
        except Exception as e:
            print(f"Error al crear genero: {e}")
            raise APIError("Error al crear género")

    def obtener_genero(self, genero_id: str) -> Optional[genero_mod.GeneroModeloDTO]:
        try:
            doc = self.collection.find_one({"_id": ObjectId(genero_id)})
            if not doc:
                return None
            doc['_id'] = str(doc['_id'])
            return genero_mod.GeneroModeloDTO(**doc)
        except Exception as e:
            print(f"Error al obtener genero: {e}")
            raise APIError("Error al obtener género")

    def obtener_generos(self) -> List[genero_mod.GeneroModeloDTO]:
        try:
            docs = self.collection.find().sort('fecha_creacion', -1)
            generos = []
            for d in docs:
                d['_id'] = str(d['_id'])
                generos.append(genero_mod.GeneroModeloDTO(**d))
            return generos
        except Exception as e:
            print(f"Error al obtener generos: {e}")
            raise APIError("Error al obtener géneros")

    def actualizar_genero(self, genero: genero_mod.GeneroModelo, genero_id: str) -> int:
        try:
            genero.fecha_modificacion = datetime.now()
            result = self.collection.update_one({"_id": ObjectId(genero_id)}, {"$set": genero.__dict__})
            return result.modified_count
        except Exception as e:
            print(f"Error al actualizar genero: {e}")
            raise APIError("Error al actualizar género")

    def eliminar_genero(self, genero_id: str) -> bool:
        try:
            result = self.collection.delete_one({"_id": ObjectId(genero_id)})
            return result.deleted_count > 0
        except Exception as e:
            print(f"Error al eliminar genero: {e}")
            raise APIError("Error al eliminar género")
