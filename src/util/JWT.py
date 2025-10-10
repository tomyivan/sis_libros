import jwt
from datetime import datetime, timedelta
import dotenv
import os
from src.custom.error_custom import APIError
dotenv.load_dotenv()

class JWTHandler:
    @staticmethod
    def nuevoToken(payload: dict, exp_minutes: int = 60) -> str:
        try:
            secreto = os.getenv("JWT_SECRET_KEY")
            if not secreto:
                raise ValueError("JWT_SECRET_KEY no encontrada en las variables de entorno")
            
            payloadCopy = payload.copy()
            payloadCopy['exp'] = datetime.utcnow() + timedelta(minutes=exp_minutes)
            token = jwt.encode(payloadCopy, secreto, algorithm='HS256')
            return token
        except Exception as e:
            print(f"Error al generar el token: {e}")
            raise APIError("Error al generar el token")
    @staticmethod
    def verificarToken(token: str) -> dict:
        try:
            secreto = os.getenv("JWT_SECRET_KEY")
            if not secreto:
                raise ValueError("JWT_SECRET_KEY no encontrada en las variables de entorno")
                
            decodificado = jwt.decode(token, secreto, algorithms=['HS256'])
            return decodificado
        except jwt.ExpiredSignatureError:
            print("El token ha expirado")
            raise APIError("El token ha expirado")
        except jwt.InvalidTokenError:
            print("Token inválido")
            raise APIError("Token inválido")
    @staticmethod
    def refrescarToken(token: str, exp_minutes: int = 60) -> str:
        try:
            decodificar = JWTHandler.verificarToken(token)
            # Eliminar la clave 'exp' para evitar conflictos al generar un nuevo token
            if 'exp' in decodificar:
                del decodificar['exp']
            nuevoToken = JWTHandler.nuevoToken(decodificar, exp_minutes)
            return nuevoToken
        except Exception as e:
            print(f"Error al refrescar el token: {e}")
            raise APIError("Error al refrescar el token")
