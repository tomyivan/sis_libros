import redis
import os
import dotenv 
dotenv.load_dotenv()
# Configuración de Redis
puerto = os.getenv('REDIS_PORT', 6379)
host = os.getenv('REDIS_URI', 'localhost')
redCli = r = redis.Redis(host=host, port=puerto, db=0, decode_responses=True)
