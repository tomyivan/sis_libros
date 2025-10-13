from src.custom.error_custom import APIError
from src.helpers.mongoconn_hlp import MongoConnection
from src.dominio.modelos import comentarios_mod
from src.dominio.puertos import comentario_prt
from bson import ObjectId
from datetime import datetime
from typing import List

class ComentarioRepositorio(comentario_prt.ComentarioPuerto):
    def __init__(self, conexion: MongoConnection):
        self.db = conexion.conectar()
        self.collection = self.db.comentarios

    def crearComentario(self, comentario: comentarios_mod.ComentarioModelo) -> str:
        try:
            doc = comentario.__dict__
            doc['fecha_creacion'] = datetime.now()
            result = self.collection.insert_one(doc)
            return str(result.inserted_id)
        except Exception as e:
            print(f"Error al crear comentario: {e}")
            raise APIError("Error al crear comentario")

    def obtenerComentario(self, filtro: comentarios_mod.FiltroComentarioModelo) -> comentarios_mod.ComentarioModeloDTO:
        try:
            query = {}
            if filtro._id:
                query['_id'] = ObjectId(filtro._id)
            if filtro.idUsuario:
                query['idUsuario'] = filtro.idUsuario
            if filtro.idLibro:
                query['idLibro'] = filtro.idLibro

            docs = self.collection.find(query).sort('fecha_creacion', -1)
            comentarios = []
            for d in docs:
                d['_id'] = str(d['_1d']) if d.get('_1d') else str(d.get('_id'))
                comentarios.append(comentarios_mod.ComentarioModeloDTO(**d))
            return comentarios
        except Exception as e:
            print(f"Error al obtener comentario: {e}")
            raise APIError("Error al obtener comentario")

    def actualizarComentario(self, comentario: comentarios_mod.ComentarioModelo, comentarioId: str) -> int:
        try:
            update = comentario.__dict__
            update['fecha_modificacion'] = datetime.now()
            result = self.collection.update_one({"_id": ObjectId(comentarioId)}, {"$set": update})
            return result.modified_count
        except Exception as e:
            print(f"Error al actualizar comentario: {e}")
            raise APIError("Error al actualizar comentario")

    def eliminarComentario(self, comentarioId: str) -> bool:
        try:
            result = self.collection.delete_one({"_id": ObjectId(comentarioId)})
            return result.deleted_count > 0
        except Exception as e:
            print(f"Error al eliminar comentario: {e}")
            raise APIError("Error al eliminar comentario")
