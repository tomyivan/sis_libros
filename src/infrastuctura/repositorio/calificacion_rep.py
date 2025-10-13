from src.dominio.modelos import calificacion_mod
from src.dominio.puertos import calificacion_prt
from src.helpers import MongoConnection
from src.custom.error_custom import APIError

class CalificacionRepositorio(calificacion_prt.CalificacionPuerto):
    def __init__(self, conexion: MongoConnection):
        self.db = conexion.conectar()
        self.collection = self.db.calificaciones
    def crearCalificacion(self, calificacion: calificacion_mod.C) -> str:
        try:
            result = self.collection.insert_one(calificacion.__dict__)
            return str(result.inserted_id)
        except Exception as e:
            print(f"Error al crear calificacion: {e}")
            raise APIError("Error al crear calificación")
    def obtenerCalificacion(self, filtro: dict) -> calificacion_mod.CalificacionModeloDTO:
        try:
            result = self.collection.find_one(filtro)
            if result:
                return calificacion_mod.CalificacionModeloDTO(**result)
            return None
        except Exception as e:
            print(f"Error al obtener calificacion: {e}")
            raise APIError("Error al obtener calificación")
        
    def actualizarCalificacion(self, calificacion: calificacion_mod.CalificacionModelo, calificacionId: str) -> int:
        try:
            result = self.collection.update_one({"_id": calificacionId}, {"$set": calificacion.__dict__})
            return result.modified_count
        except Exception as e:
            print(f"Error al actualizar calificacion: {e}")
            raise APIError("Error al actualizar calificación")
        
    def eliminarCalificacion(self, calificacionId: str) -> bool:
        try:
            result = self.collection.delete_one({"_id": calificacionId})
            return result.deleted_count > 0
        except Exception as e:
            print(f"Error al eliminar calificacion: {e}")
            raise APIError("Error al eliminar calificación")
        
    
