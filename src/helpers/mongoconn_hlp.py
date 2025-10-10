from pymongo import MongoClient
from pymongo.collection import Collection
import dotenv
import os
class MongoConnection:
    def conectar(self) :
        try:
            dotenv.load_dotenv()
            mongo_uri = os.getenv("MONGO_URI")
            client = MongoClient(mongo_uri)
            print("Conexión a MongoDB exitosa")
            return client.recomendacion_libros
        except Exception as e:
            print(f"Error al conectar a MongoDB: {e}")
            raise