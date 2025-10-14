from src.dominio.modelos import recomendacion_mod
from src.dominio.puertos.recomendacion_prt import RecomendacionPuerto
from src.helpers.mongoconn_hlp import MongoConnection
from src.helpers.redisconn_hlp import redCli
import json
from bson import ObjectId
from datetime import datetime
from typing import Any, List


class RecomendacionRepositorio(RecomendacionPuerto):
    def __init__(self, conexion: MongoConnection):
        self.db = conexion.conectar()
        self.collection = self.db.recomendaciones
        self.redis = redCli

    def obtenerRecomendacionPorLibro(self, idLibro: str):
        """Obtener recomendaciones desde Redis.

        Prioridad de lectura:
          1) `recomendaciones:books:{id}` -> Redis LIST con elementos JSON (cada elemento es objeto libro)
          2) `recomendaciones:{id}` -> compatibilidad (JSON con lista de ids u objetos)
        Devuelve una lista de objetos (dict) o None.
        """
        # 1) set de objetos (no ordenado)
        set_key = f"recomendaciones:set:{idLibro}"
        if self.redis.exists(set_key):
            try:
                items = self.redis.smembers(set_key)
                return [json.loads(x) for x in items]
            except Exception:
                return None

        # 2) compatibilidad con clave antigua
        raw = self.redis.get(f"recomendaciones:{idLibro}")
        if not raw:
            return None
        try:
            return json.loads(raw)
        except Exception:
            return raw

    def _normalize_for_json(self, v: Any):
        """Convierte ObjectId y datetime a tipos serializables por JSON."""
        if isinstance(v, ObjectId):
            return str(v)
        if isinstance(v, datetime):
            return v.isoformat()
        return v

    def _normalize_doc(self, doc: dict) -> dict:
        out = {}
        for k, v in dict(doc).items():
            if isinstance(v, list):
                out[k] = [self._normalize_for_json(x) for x in v]
            else:
                out[k] = self._normalize_for_json(v)
        return out

    def guardarRecomendacionRedis(self, idLibro: str, recomendaciones) -> None:
        """Guardar recomendaciones en Redis.

        Ahora guarda objetos completos de libros en la clave `recomendaciones:books:{idLibro}` como
        una LIST donde cada elemento es un JSON con el objeto del libro. También mantiene un SET
        con los ids en `recomendaciones:ids:{idLibro}` para búsquedas rápidas.

        `recomendaciones` puede ser una lista de ids (str/ObjectId) o una lista de dicts.
        """
        set_key = f"recomendaciones:set:{idLibro}"
        ids_key = f"recomendaciones:ids:{idLibro}"
        ttl = 3600

        # limpiar claves previas
        try:
            self.redis.delete(set_key)
            self.redis.delete(ids_key)
        except Exception:
            pass

        # Resolver cada recomendación a objeto completo
        objs: List[dict] = []
        ids: List[str] = []
        for rec in recomendaciones:
            # si es dict, normalizar
            if isinstance(rec, dict):
                obj = self._normalize_doc(rec)
                obj_id = str(obj.get("_id") or obj.get("id") or "")
            else:
                # asumir id -> intentar obtener book:{id} desde redis o desde mongo
                rec_id = str(rec)
                # intentar Redis book cache
                try:
                    raw = self.redis.get(f"book:{rec_id}")
                    if raw:
                        obj = json.loads(raw)
                    else:
                        # fallback: obtener desde Mongo
                        try:
                            doc = self.db.libros.find_one({"_id": ObjectId(rec_id)})
                            if doc:
                                obj = self._normalize_doc(doc)
                            else:
                                obj = {"_id": rec_id}
                        except Exception:
                            obj = {"_id": rec_id}
                except Exception:
                    obj = {"_id": rec_id}

            # push into set (members are JSON strings)
            try:
                self.redis.sadd(set_key, json.dumps(obj))
                ids.append(str(obj.get("_id") or obj.get("id") or ""))
            except Exception:
                continue

        # aplicar TTL
        try:
            self.redis.expire(set_key, ttl)
            self.redis.expire(ids_key, ttl)
        except Exception:
            pass
    
