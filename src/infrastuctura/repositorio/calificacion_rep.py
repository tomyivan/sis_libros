from src.dominio.modelos import calificacion_mod
from src.dominio.puertos import calificacion_prt
from src.helpers.mongoconn_hlp import MongoConnection
from src.custom.error_custom import APIError
from bson import ObjectId


class CalificacionRepositorio(calificacion_prt.CalificacionPuerto):
    def __init__(self, conexion: MongoConnection):
        self.db = conexion.conectar()
        self.collection = self.db.calificaciones

    def crearCalificacion(self, calificacion: calificacion_mod.CalificacionModelo) -> str:
        try:
            doc = calificacion.__dict__
            result = self.collection.insert_one(doc)
            return str(result.inserted_id)
        except Exception as e:
            print(f"Error al crear calificacion: {e}")
            raise APIError("Error al crear calificación")

    def obtenerCalificacion(self, filtro: dict):
        try:
            query = {}
            if filtro is None:
                filtro = {}
            # allow passing either dict or FiltroCalificacionModelo.__dict__
            query.update(filtro)
            if query.get('_id'):
                try:
                    query['_id'] = ObjectId(query['_id'])
                except Exception:
                    pass
            result = self.collection.find_one(query)
            if result:
                result['_id'] = str(result.get('_id'))
                return result
            return None
        except Exception as e:
            print(f"Error al obtener calificacion: {e}")
            raise APIError("Error al obtener calificación")

    def actualizarCalificacion(self, calificacion: calificacion_mod.CalificacionModelo, calificacionId: str) -> int:
        try:
            result = self.collection.update_one({"_id": ObjectId(calificacionId)}, {"$set": calificacion.__dict__})
            return result.modified_count
        except Exception as e:
            print(f"Error al actualizar calificacion: {e}")
            raise APIError("Error al actualizar calificación")

    def eliminarCalificacion(self, calificacionId: str) -> bool:
        try:
            result = self.collection.delete_one({"_id": ObjectId(calificacionId)})
            return result.deleted_count > 0
        except Exception as e:
            print(f"Error al eliminar calificacion: {e}")
            raise APIError("Error al eliminar calificación")


