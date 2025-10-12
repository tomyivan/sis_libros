from src.dominio.puertos.historial_prt import HistorialPuerto
from src.dominio.modelos import historial_mod
import src.helpers.redisconn_hlp as redisconn_hlp
import json
import redis
from typing import List


class HistorialRepositorio(HistorialPuerto):
    def __init__(self):
        self.redCli = redisconn_hlp.redCli
        self.key = "historial"

    def obtenerHistorial(self, idUsuario: str, libro: str = "") -> List[historial_mod.HistorialModeloDTO]:
        user_key = f"{self.key}:{idUsuario}"
        try:
            key_type = self.redCli.type(user_key)
            if key_type != 'set' and key_type != 'none':
                return []
            historiales = self.redCli.smembers(user_key)
            historial_list = []
            for historial_json in historiales:
                historial_dict = json.loads(historial_json)
                if libro:
                    if libro.lower() in (historial_dict.get('textoBusqueda') or '').lower():
                        historial_list.append(historial_mod.HistorialModeloDTO(**historial_dict))
                else:
                    historial_list.append(historial_mod.HistorialModeloDTO(**historial_dict))
            return historial_list
        except Exception as e:
            print(f"Error al obtener el historial: {e}")
            return []
    
    def registrarHistorial(self, historial: historial_mod.HistorialModelo) -> str:
        historial_dict = historial.__dict__
        historial_json = json.dumps(historial_dict, ensure_ascii=False)
        user_key = f"{self.key}:{historial.idUsuario}"
        # index key for case-insensitive duplicate checks
        index_key = f"{user_key}:idx"
        try:
            key_type = self.redCli.type(user_key)
            if key_type and key_type != 'set' and key_type != 'none':
                self.redCli.delete(user_key)
            # Verificar si el historial ya existe antes de agregarlo (case-insensitive)
            normalized = (historial_dict.get('textoBusqueda') or '').strip().lower()
            if normalized and self.redCli.sismember(index_key, normalized):
                return "El historial ya existe, no se registró duplicado"

            # Add both the original JSON entry and the normalized index
            self.redCli.sadd(user_key, historial_json)
            if normalized:
                self.redCli.sadd(index_key, normalized)
            return "Historial registrado exitosamente"
        except redis.exceptions.ResponseError:
            # If a WRONGTYPE occurred, try to recover by deleting the key and retrying the add
            try:
                self.redCli.delete(user_key)
                try:
                    self.redCli.delete(index_key)
                except Exception:
                    pass
                self.redCli.sadd(user_key, historial_json)
                # also try to add to index
                normalized = (historial_dict.get('textoBusqueda') or '').strip().lower()
                if normalized:
                    self.redCli.sadd(index_key, normalized)
                return "Historial registrado exitosamente"
            except Exception as e:
                raise