from src.custom.error_custom import APIError
from src.helpers import MongoConnection
from typing import List
from src.dominio.modelos import usuario_mod
from src.dominio.puertos import usuario_prt
from bson import ObjectId

class UsuarioRepositorio(usuario_prt.UsuarioPuerto):
    def __init__(self, conexion: MongoConnection):
        self.db = conexion.conectar()
        self.collection = self.db.usuarios

    def obtenerUsuario(self, filtro: usuario_mod.FiltroUsuarioModelo) -> usuario_mod.UsuarioModeloDTO:
        try:
            query = {k: (ObjectId(v) if k == "_id" else v) for k, v in filtro.__dict__.items() if v is not None}
            respuesta = self.collection.find_one(query,
                                                 projection={"_id": 1, "nombre": 1, "apellido": 1, "alias": 1, "email": 1, "pais": 1, "edad": 1, "fecha_creacion": 1, "fecha_modificacion": 1, "password_hash": 1}
                                                 )
            if respuesta:
                return usuario_mod.UsuarioModeloDTO(**{**respuesta, "_id": str(respuesta["_id"])})
            return None
        except Exception as e:
            print(f"Error al obtener usuario: {e}")
            raise APIError("Error al obtener usuario")
        
    def obtenerUsuarios(self, filtro: usuario_mod.FiltroUsuarioModelo) -> List[usuario_mod.UsuarioModeloDTO]:
        try:
            query = {k: v for k, v in filtro.__dict__.items() if v is not None}
            respuesta = self.collection.find(query,
                                             projection={"_id": 1, "nombre": 1, "apellido": 1, "alias": 1, "email": 1, "pais": 1, "edad": 1, "fecha_creacion": 1, "fecha_modificacion": 1})

            usuarios = []
            for usuario in respuesta:
                usuario_dict = dict(usuario)  # Convertimos a dict por si acaso
                usuario_dict["_id"] = str(usuario_dict["_id"])  # Convertimos ObjectId a str
                usuarios.append(usuario_mod.UsuarioModeloDTO(**usuario_dict))
            return usuarios

        except Exception as e:
            print(f"Error al obtener usuarios: {e}")
            raise APIError("Error al obtener usuarios")

    
    def crearUsuario(self, usuario: usuario_mod.UsuarioModelo) -> str:
        try:
            usuario_dict = usuario.__dict__
            result = self.collection.insert_one(usuario_dict)
            print(f"Usuario creado con ID: {result.inserted_id}")
            return str(result.inserted_id)
        except Exception as e:
            print(f"Error al crear usuario: {e}")
            raise APIError("Error al crear usuario")
    
    def actualizarUsuario(self, usuario: usuario_mod.UsuarioModelo) -> str:
        try:
            usuario_dict = usuario.__dict__
            result = self.collection.update_one({"id": usuario.id}, {"$set": usuario_dict})
            return result.modified_count
        except Exception as e:
            print(f"Error al actualizar usuario: {e}")
            raise APIError("Error al actualizar usuario")
    
    def desactivarUsuario(self, idUsuario: int) -> bool:
        try:
            result = self.collection.update_one({"id": idUsuario}, {"$set": {"activo": False}})
            return result.modified_count > 0
        except Exception as e:
            print(f"Error al desactivar usuario: {e}")
            raise APIError("Error al desactivar usuario")
    
    def obtenerUsuarioPorAlias(self, alias: str) -> usuario_mod.UsuarioModeloDTO:
        """
        Obtiene un usuario por su alias para autenticación
        """
        try:
            filtro = usuario_mod.FiltroUsuarioModelo(alias=alias)
            return self.obtenerUsuario(filtro)
        except Exception as e:
            print(f"Error al obtener usuario por alias: {e}")
            raise APIError("Error al obtener usuario por alias")
