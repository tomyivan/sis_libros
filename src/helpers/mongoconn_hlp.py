from pymongo import MongoClient
import dotenv
import os
import threading
from typing import Optional


class MongoConnection:
    

    _client: Optional[MongoClient] = None
    _lock = threading.Lock()

    def __init__(self, db_name: Optional[str] = None):
        dotenv.load_dotenv()
        self._db_name = db_name or os.getenv('MONGO_DB', 'recomendacion_libros')

    def conectar(self):
        
        if MongoConnection._client is None:
            with MongoConnection._lock:
                if MongoConnection._client is None:
                    mongo_uri = os.getenv('MONGO_URI')
                    if not mongo_uri:
                        raise RuntimeError('MONGO_URI no configurado en el entorno')
                    try:
                        MongoConnection._client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
                        MongoConnection._client.admin.command('ping')
                        print('Conexión a MongoDB establecida')
                    except Exception as e:
                        MongoConnection._client = None
                        print(f'Error al conectar a MongoDB: {e}')
                        raise

        # return the database object (indexed by name)
        return MongoConnection._client[self._db_name]

    @classmethod
    def close_client(cls):
        if cls._client is not None:
            try:
                cls._client.close()
            finally:
                cls._client = None
