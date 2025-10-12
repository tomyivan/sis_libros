from src.custom.error_custom import APIError
from src.helpers.mongoconn_hlp import MongoConnection
from src.dominio.modelos import pais_mod
from src.dominio.puertos import pais_prt
from bson import ObjectId
from datetime import datetime
from typing import List


class PaisRepositorio(pais_prt.PaisPuerto):
    def __init__(self, conexion: MongoConnection):
        self.db = conexion.conectar()
        self.collection = self.db.paises

    def crearPais(self, pais: pais_mod.PaisModelo) -> str:
        try:
            if pais.fecha_creacion is None:
                pais.fecha_creacion = datetime.now()
            result = self.collection.insert_one(pais.__dict__)
            return str(result.inserted_id)
        except Exception as e:
            print(f"Error al crear pais: {e}")
            raise APIError("Error al crear país")

    def obtenerPais(self, pais_id: str) -> pais_mod.PaisModeloDTO:
        try:
            doc = self.collection.find_one({"_id": ObjectId(pais_id)})
            if not doc:
                return None
            doc['_id'] = str(doc['_id'])
            return pais_mod.PaisModeloDTO(**doc)
        except Exception as e:
            print(f"Error al obtener pais: {e}")
            raise APIError("Error al obtener país")

    def obtenerPaises(self) -> List[pais_mod.PaisModeloDTO]:
        try:
            docs = self.collection.find().sort('fecha_creacion', -1)
            items = []
            for d in docs:
                d['_id'] = str(d['_id'])
                items.append(pais_mod.PaisModeloDTO(**d))
            return items
        except Exception as e:
            print(f"Error al obtener paises: {e}")
            raise APIError("Error al obtener países")

    def actualizarPais(self, pais: pais_mod.PaisModelo, pais_id: str) -> int:
        try:
            pais.fecha_creacion = pais.fecha_creacion or None
            pais.fecha_modificacion = datetime.now()
            result = self.collection.update_one({"_id": ObjectId(pais_id)}, {"$set": pais.__dict__})
            return result.modified_count
        except Exception as e:
            print(f"Error al actualizar pais: {e}")
            raise APIError("Error al actualizar país")

    def eliminarPais(self, pais_id: str) -> bool:
        try:
            result = self.collection.delete_one({"_id": ObjectId(pais_id)})
            return result.deleted_count > 0
        except Exception as e:
            print(f"Error al eliminar pais: {e}")
            raise APIError("Error al eliminar país")
