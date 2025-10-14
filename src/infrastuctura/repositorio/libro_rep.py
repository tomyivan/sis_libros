from src.custom.error_custom import APIError
from src.helpers import MongoConnection
from src.dominio.modelos import libro_mod
from src.dominio.puertos import libro_prt
from bson import ObjectId
from datetime import datetime
from typing import List

class LibroRepositorio(libro_prt.LibroPuerto):
    def __init__(self, conexion: MongoConnection):
        self.db = conexion.conectar()
        self.collection = self.db.libros

    def obtenerLibroInfo(self, idLibro: str) -> libro_mod.LibroInformacion:        
        try:
            pipeline = [
                {"$match": {"_id": ObjectId(idLibro)}},

                # lookup calificaciones: soporta idLibro como STRING o como ObjectId
                {
                    "$lookup": {
                        "from": "calificaciones",
                        "let": {"bookId": "$_id"},
                        "pipeline": [
                            {
                                "$match": {
                                    "$expr": {
                                        "$or": [
                                            {"$eq": ["$idLibro", "$$bookId"]},                    # si idLibro es ObjectId
                                            {"$eq": [{"$toString": "$idLibro"}, {"$toString": "$$bookId"}]},  # si idLibro es string
                                            {"$eq": [{"$toObjectId": "$idLibro"}, "$$bookId"]}     # si idLibro es string convertible a ObjectId
                                        ]
                                    }
                                }
                            }
                        ],
                        "as": "calificaciones"
                    }
                },

                # lookup comentarios: mismo enfoque
                {
                    "$lookup": {
                        "from": "comentarios",
                        "let": {"bookId": "$_id"},
                        "pipeline": [
                            {
                                "$match": {
                                    "$expr": {
                                        "$or": [
                                            {"$eq": ["$idLibro", "$$bookId"]},
                                            {"$eq": [{"$toString": "$idLibro"}, {"$toString": "$$bookId"}]},
                                            {"$eq": [{"$toObjectId": "$idLibro"}, "$$bookId"]}
                                        ]
                                    }
                                }
                            },
                            # opcional: ordenar comentarios por fecha descendente dentro del lookup
                            {"$sort": {"fecha_creacion": -1}}
                        ],
                        "as": "comentarios"
                    }
                },

                # calcular promedio y formatear comentarios
                {
                    "$addFields": {
                        "calificacion_promedio": {
                            "$cond": [
                                {"$gt": [{"$size": "$calificaciones"}, 0]},
                                {
                                    "$round": [
                                        {
                                            "$avg": {
                                                "$map": {
                                                    "input": "$calificaciones",
                                                    "as": "c",
                                                    # convertir a double si viene como string, y evitar valores nulos
                                                    "in": {
                                                        "$cond": [
                                                            {"$ifNull": ["$$c.calificacion", False]},
                                                            {"$toDouble": "$$c.calificacion"},
                                                            None
                                                        ]
                                                    }
                                                }
                                            }
                                        },
                                        2
                                    ]
                                },
                                None
                            ]
                        },
                        # Mapeo de comentarios ya ordenados por fecha dentro del lookup
                        "comentarios": {
                            "$map": {
                                "input": "$comentarios",
                                "as": "c",
                                "in": {
                                    "idUsuario": "$$c.idUsuario",
                                    "comentario": "$$c.comentario",
                                    "fecha_creacion": "$$c.fecha_creacion"
                                }
                            }
                        }
                    }
                },

                # proyectar solo lo necesario
                {
                    "$project": {
                        "_id": 1,
                        "titulo": 1,
                        "autor": 1,
                        "genero": 1,
                        "año_publicacion": 1,
                        "editorial": 1,
                        "isbn": 1,
                        "paginas": 1,
                        "idioma": 1,
                        "descripcion": 1,
                        "origen_pais": 1,
                        "disponible": 1,
                        "portada_url": 1,
                        "tags": 1,
                        "calificacion_promedio": 1,
                        "comentarios": 1
                    }
                }
            ]
            result = list(self.collection.aggregate(pipeline))
            if not result:
                return None
            return result[0]        
        except Exception as e:
            print(f"Error al obtener libro: {e}")
            raise APIError("Error al obtener libro")

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

