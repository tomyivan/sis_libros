from flask import json
from datetime import datetime
from src.dominio.puertos.publicacion_prt import PublicacionPuerto
from src.dominio.modelos.publicacion_mod import PublicacionModelo
class ObtenerPublicacionServicio:
    def __init__(self, repositorio: PublicacionPuerto):
        self.repositorio = repositorio

    def obtenerPublicaciones(self) -> list:
        """Obtiene todas las publicaciones"""
        pub =  self.repositorio.obtenerPublicaciones()
        print(pub)
        if pub['type'] != 'message':
            return {
                "mensaje": "No hay nuevas publicaciones",
                "data": [],
                "fecha_creacion" : datetime.now()
            }
        return PublicacionModelo(pub['data']).__dict__

        
        