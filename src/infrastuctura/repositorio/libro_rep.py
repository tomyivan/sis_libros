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
            respuesta = self.collection.find_one(query)
            if respuesta:
                return self._convertir_a_dto(respuesta)
            return None
        except Exception as e:
            print(f"Error al obtener libro: {e}")
            raise APIError("Error al obtener libro")

    def obtenerLibros(self, filtro: libro_mod.FiltroLibroModelo) -> List[libro_mod.LibroModeloDTO]:
        try:
            query = self._construir_query(filtro)
            respuesta = self.collection.find(query).sort("fecha_creacion", -1)  # Más recientes primero
            
            libros = []
            for libro in respuesta:
                libros.append(self._convertir_a_dto(libro))
            return libros

        except Exception as e:
            print(f"Error al obtener libros: {e}")
            raise APIError("Error al obtener libros")

    def crearLibro(self, libro: libro_mod.LibroModelo) -> str:
        try:
            # Agregar fecha de creación si no existe
            if libro.fecha_creacion is None:
                libro.fecha_creacion = datetime.now()
            
            # Validar ISBN único
            if self._isbn_existe(libro.isbn):
                raise APIError("Ya existe un libro con este ISBN")
            
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
            
            # Validar ISBN único (excluyendo el libro actual)
            if self._isbn_existe(libro.isbn, excluir_id=libro_id):
                raise APIError("Ya existe otro libro con este ISBN")
            
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
            result = self.collection.update_one(
                {"_id": ObjectId(libro_id)}, 
                {"$set": {"disponible": False, "fecha_modificacion": datetime.now()}}
            )
            return result.modified_count > 0
        except Exception as e:
            print(f"Error al eliminar libro: {e}")
            raise APIError("Error al eliminar libro")

    def buscarLibrosPorTexto(self, texto: str) -> List[libro_mod.LibroModeloDTO]:
        try:
            # Búsqueda de texto en múltiples campos
            regex_pattern = re.compile(texto, re.IGNORECASE)
            query = {
                "$or": [
                    {"titulo": {"$regex": regex_pattern}},
                    {"autor": {"$regex": regex_pattern}},
                    {"descripcion": {"$regex": regex_pattern}},
                    {"editorial": {"$regex": regex_pattern}},
                    {"tags": {"$regex": regex_pattern}}
                ],
                "disponible": True
            }
            
            respuesta = self.collection.find(query).sort("calificacion_promedio", -1)
            
            libros = []
            for libro in respuesta:
                libros.append(self._convertir_a_dto(libro))
            return libros

        except Exception as e:
            print(f"Error al buscar libros por texto: {e}")
            raise APIError("Error al buscar libros")

    def obtenerLibrosPorGenero(self, genero: str) -> List[libro_mod.LibroModeloDTO]:
        try:
            query = {"genero": {"$regex": genero, "$options": "i"}, "disponible": True}
            respuesta = self.collection.find(query).sort("calificacion_promedio", -1)
            
            libros = []
            for libro in respuesta:
                libros.append(self._convertir_a_dto(libro))
            return libros

        except Exception as e:
            print(f"Error al obtener libros por género: {e}")
            raise APIError("Error al obtener libros por género")

    def obtenerLibrosPorAutor(self, autor: str) -> List[libro_mod.LibroModeloDTO]:
        try:
            query = {"autor": {"$regex": autor, "$options": "i"}, "disponible": True}
            respuesta = self.collection.find(query).sort("año_publicacion", -1)
            
            libros = []
            for libro in respuesta:
                libros.append(self._convertir_a_dto(libro))
            return libros

        except Exception as e:
            print(f"Error al obtener libros por autor: {e}")
            raise APIError("Error al obtener libros por autor")

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
        if filtro.calificacion_min:
            query["calificacion_promedio"] = {"$gte": filtro.calificacion_min}
        if filtro.tags:
            query["tags"] = {"$in": filtro.tags}
            
        return query

    def _convertir_a_dto(self, documento: dict) -> libro_mod.LibroModeloDTO:
        """Convierte un documento de MongoDB a LibroModeloDTO"""
        documento["_id"] = str(documento["_id"])
        
        # Manejar campos opcionales
        if "tags" not in documento:
            documento["tags"] = []
        if "calificacion_promedio" not in documento:
            documento["calificacion_promedio"] = 0.0
        if "numero_calificaciones" not in documento:
            documento["numero_calificaciones"] = 0
            
        return libro_mod.LibroModeloDTO(**documento)

    def _isbn_existe(self, isbn: str, excluir_id: str = None) -> bool:
        """Verifica si un ISBN ya existe en la base de datos"""
        query = {"isbn": isbn}
        if excluir_id:
            query["_id"] = {"$ne": ObjectId(excluir_id)}
        
        return self.collection.find_one(query) is not None