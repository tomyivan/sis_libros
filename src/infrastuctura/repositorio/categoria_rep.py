from src.custom.error_custom import APIError
from src.helpers import MongoConnection
from src.dominio.modelos import categoria_mod
from src.dominio.puertos import categoria_prt
from bson import ObjectId
from datetime import datetime
from typing import List

class CategoriaRepositorio(categoria_prt.CategoriaPuerto):
    def __init__(self, conexion: MongoConnection):
        self.db = conexion.conectar()
        self.collection = self.db.categorias

    def crearCategoria(self, categoria: categoria_mod.CategoriaModelo) -> str:
        try:
            # print(categoria)
            if categoria.fecha_creacion is None:
                categoria.fecha_creacion = datetime.now()
            print(categoria.__dict__)
            result = self.collection.insert_one(categoria.__dict__)
            return str(result.inserted_id)
        except Exception as e:
            print(f"Error al crear categoria: {e}")
            raise APIError("Error al crear categoría")

    def obtenerCategoria(self, categoria_id: str) -> categoria_mod.CategoriaModeloDTO:
        try:
            doc = self.collection.find_one({"_id": ObjectId(categoria_id)})
            if not doc:
                return None
            doc['_id'] = str(doc['_id'])
            return categoria_mod.CategoriaModeloDTO(**doc)
        except Exception as e:
            print(f"Error al obtener categoria: {e}")
            raise APIError("Error al obtener categoría")

    def obtenerCategorias(self) -> List[categoria_mod.CategoriaModeloDTO]:
        try:
            docs = self.collection.find().sort('fecha_creacion', -1)
            categorias = []
            for d in docs:
                d['_id'] = str(d['_id'])
                categorias.append(categoria_mod.CategoriaModeloDTO(**d))
            return categorias
        except Exception as e:
            print(f"Error al obtener categorias: {e}")
            raise APIError("Error al obtener categorías")

    def actualizarCategoria(self, categoria: categoria_mod.CategoriaModelo, categoria_id: str) -> int:
        try:
            categoria.fecha_modificacion = datetime.now()
            result = self.collection.update_one({"_id": ObjectId(categoria_id)}, {"$set": categoria.__dict__})
            return result.modified_count
        except Exception as e:
            print(f"Error al actualizar categoria: {e}")
            raise APIError("Error al actualizar categoría")

    def eliminarCategoria(self, categoria_id: str) -> bool:
        try:
            result = self.collection.delete_one({"_id": ObjectId(categoria_id)})
            return result.deleted_count > 0
        except Exception as e:
            print(f"Error al eliminar categoria: {e}")
            raise APIError("Error al eliminar categoría")
