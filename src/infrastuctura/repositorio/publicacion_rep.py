from datetime import datetime
from flask import json
from src.dominio.puertos.publicacion_prt import PublicacionPuerto
from src.dominio.modelos.publicacion_mod import PublicacionModelo
from src.helpers.redisconn_hlp import redCli
class PublicacionRepositorio(PublicacionPuerto):
    def __init__(self):
        self.redis = redCli
        self.channel = "notificacion"
    def nuevaPublicacion(self, publicacion: PublicacionModelo) -> bool:
        """Notifica a Redis que hay una nueva publicación (libro) agregada.
        Esto invalida las recomendaciones en caché para este libro.
        """
        try:
            # Accept either a model instance with __dict__ or a plain dict/json-serializable
            if hasattr(publicacion, '__dict__'):
                payload = publicacion.__dict__
            elif isinstance(publicacion, dict):
                payload = publicacion
            else:
                # fallback: try to use it directly
                payload = publicacion
            self.redis.publish(self.channel, json.dumps(payload))
            return True
        except Exception as e:
            print(f"Error al notificar nueva publicación: {e}")
            raise ValueError("Error al notificar nueva publicación: " + str(e))
        
    def obtenerPublicaciones(self) -> list:
        """Escucha el canal de Redis para nuevas publicaciones."""
        try:
            pubsub = self.redis.pubsub()
            pubsub.subscribe(self.channel)
            for msg in pubsub.listen():
                return msg
    
        except Exception as e:
            raise ValueError("Error al obtener publicaciones: " + str(e))
         
         