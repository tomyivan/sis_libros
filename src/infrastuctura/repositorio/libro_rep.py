from src.custom.error_custom import APIError
from src.helpers import MongoConnection
from src.dominio.modelos import libro_mod
from src.dominio.puertos import libro_prt
from bson import ObjectId
from datetime import datetime
from typing import List
import re

class LibroRepositorio(libro_prt.LibroPuerto):
    def __init__(self, conexion: MongoConnection):
        self.db = conexion.conectar()
        self.collection = self.db.libros

    def obtenerLibro(self, filtro: libro_mod.FiltroLibroModelo) -> libro_mod.LibroModeloDTO:
        try:
            query = self._construir_query(filtro)
            return self.collection.find_one(query)
            
        except Exception as e:
            print(f"Error al obtener libro: {e}")
            raise APIError("Error al obtener libro")

    def obtenerLibros(self, filtro: libro_mod.FiltroLibroModelo, offset: int = None, limit: int = None) -> List[libro_mod.LibroModeloDTO]:
        try:
            query = self._construir_query(filtro)
            cursor = self.collection.find(query).sort("fecha_creacion", -1)  # Más recientes primero
            if isinstance(offset, int) and offset > 0:
                cursor = cursor.skip(offset)
            if isinstance(limit, int) and limit > 0:
                cursor = cursor.limit(limit)
            return cursor
        except Exception as e:
            print(f"Error al obtener libros: {e}")
            raise APIError("Error al obtener libros")

    def crearLibro(self, libro: libro_mod.LibroModelo) -> str:
        try:
            libro_dict = libro.__dict__
            result = self.collection.insert_one(libro_dict)
            print(f"Libro creado con ID: {result.inserted_id}")
            return str(result.inserted_id)
        except APIError:
            raise
        except Exception as e:
            print(f"Error al crear libro: {e}")
            raise APIError("Error al crear libro")

    def actualizarLibro(self, libro: libro_mod.LibroModelo, libro_id: str) -> int:
        try:
            # Agregar fecha de modificación
            libro.fecha_modificacion = datetime.now()
            
            libro_dict = libro.__dict__
            result = self.collection.update_one(
                {"_id": ObjectId(libro_id)}, 
                {"$set": libro_dict}
            )
            return result.modified_count
        except APIError:
            raise
        except Exception as e:
            print(f"Error al actualizar libro: {e}")
            raise APIError("Error al actualizar libro")

    def eliminarLibro(self, libro_id: str) -> bool:
        try:
            # Soft delete - marcar como no disponible
            print(libro_id)
            result = self.collection.update_one(
                {"_id": ObjectId(libro_id)}, 
                {"$set": {"disponible": False, "fecha_modificacion": datetime.now()}}
            )
            return result.modified_count > 0
        except Exception as e:
            print(f"Error al eliminar libro: {e}")
            raise APIError("Error al eliminar libro")

    def _construir_query(self, filtro: libro_mod.FiltroLibroModelo) -> dict:
        """Construye la query de MongoDB basada en el filtro"""
        query = {}
        
        if filtro._id:
            query["_id"] = ObjectId(filtro._id)
        if filtro.titulo:
            query["titulo"] = {"$regex": filtro.titulo, "$options": "i"}
        if filtro.autor:
            query["autor"] = {"$regex": filtro.autor, "$options": "i"}
        if filtro.genero:
            query["genero"] = {"$regex": filtro.genero, "$options": "i"}
        if filtro.año_min or filtro.año_max:
            año_query = {}
            if filtro.año_min:
                año_query["$gte"] = filtro.año_min
            if filtro.año_max:
                año_query["$lte"] = filtro.año_max
            query["año_publicacion"] = año_query
        if filtro.editorial:
            query["editorial"] = {"$regex": filtro.editorial, "$options": "i"}
        if filtro.isbn:
            query["isbn"] = filtro.isbn
        if filtro.idioma:
            query["idioma"] = filtro.idioma
        if filtro.origen_pais:
            query["origen_pais"] = filtro.origen_pais
        if filtro.disponible is not None:
            query["disponible"] = filtro.disponible
        if filtro.tags:
            query["tags"] = {"$in": filtro.tags}
            
        return query
