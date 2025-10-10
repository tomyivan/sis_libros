from src.custom.error_custom import APIError
from src.app import usuario_app
from src.dominio.modelos import usuario_mod
from src.util.responseApi import ResponseApi
from flask import request, jsonify
from marshmallow import Schema, fields, ValidationError
from datetime import datetime

class UsuarioSchema(Schema):
    id = fields.Integer(required=True, validate=lambda x: x > 0, error_messages={'required': 'El ID es requerido', 'invalid': 'El ID debe ser un número entero positivo'})
    nombre = fields.String(required=True, validate=lambda x: len(x.strip()) > 0, error_messages={'required': 'El nombre es requerido', 'invalid': 'El nombre no puede estar vacío'})
    email = fields.Email(required=True, error_messages={'required': 'El email es requerido', 'invalid': 'El email debe tener un formato válido'})
    pais = fields.String(required=True, validate=lambda x: len(x.strip()) > 0, error_messages={'required': 'El país es requerido', 'invalid': 'El país no puede estar vacío'})
    edad = fields.Integer(required=True, validate=lambda x: x > 0, error_messages={'required': 'La edad es requerida', 'invalid': 'La edad debe ser un número entero positivo'})
    password_hash = fields.String(required=True, validate=lambda x: len(x.strip()) > 0, error_messages={'required': 'El password_hash es requerido', 'invalid': 'El password_hash no puede estar vacío'})
    fecha_modificacion = fields.DateTime(required=True, error_messages={'required': 'La fecha de modificación es requerida', 'invalid': 'La fecha debe tener un formato válido'})

class UsuarioCreateSchema(Schema):    
    nombre = fields.String(required=True, validate=lambda x: len(x.strip()) > 0, error_messages={'required': 'El nombre es requerido', 'invalid': 'El nombre no puede estar vacío'})
    apellido = fields.String(required=True, validate=lambda x: len(x.strip()) > 0, error_messages={'required': 'El apellido es requerido', 'invalid': 'El apellido no puede estar vacío'})
    alias = fields.String(required=True, validate=lambda x: len(x.strip()) > 0, error_messages={'required': 'El alias es requerido', 'invalid': 'El alias no puede estar vacío'})
    email = fields.Email(required=True, error_messages={'required': 'El email es requerido', 'invalid': 'El email debe tener un formato válido'})
    pais = fields.String(required=True, validate=lambda x: len(x.strip()) > 0, error_messages={'required': 'El país es requerido', 'invalid': 'El país no puede estar vacío'})
    edad = fields.Integer(required=True, validate=lambda x: x > 0, error_messages={'required': 'La edad es requerida', 'invalid': 'La edad debe ser un número entero positivo'})
    password_hash = fields.String(required=True, validate=lambda x: len(x.strip()) > 0, error_messages={'required': 'El password_hash es requerido', 'invalid': 'El password_hash no puede estar vacío'})

class AuthSchema(Schema):
    alias = fields.String(required=True, validate=lambda x: len(x.strip()) > 0, error_messages={'required': 'El alias es requerido', 'invalid': 'El alias no puede estar vacío'})
    password = fields.String(required=True, validate=lambda x: len(x.strip()) > 0, error_messages={'required': 'El password es requerido', 'invalid': 'El password no puede estar vacío'})

class UsuarioControlador:
    def __init__(self, app: usuario_app.UsuarioApp):
        self.app = app
    def obtenerUsuarios(self):
        try:
            data = request.args.to_dict()
            filtro = usuario_mod.FiltroUsuarioModelo(
                idUsuario=data.get("idUsuario"),
                alias=data.get("alias"),
                pais=data.get("pais"),
                edad_minima=int(data.get("edad_minima")) if data.get("edad_minima") else None,
                edad_maxima=int(data.get("edad_maxima")) if data.get("edad_maxima") else None,
                activo=(data.get("activo").lower() == 'true') if data.get("activo") else None
            )
            response = self.app.obtenerUsuarios(filtro)
            if response:
                return ResponseApi.exito("Usuarios encontrados",[usuario.__dict__ for usuario in response])
            else:
                raise APIError("No se encontraron usuarios", 404)
        except Exception as e:
            raise APIError("Error en el servidor: " + str(e))
        
    def obtenerUsuario(self, idUsuario):
        try:
            response = self.app.obtenerUsuario(idUsuario)
            if response:
                return ResponseApi.exito( "Usuario encontrado", {
                    "_id": response.__dict__.get("_id"),
                    "nombre": response.__dict__.get("nombre"),
                    "apellido": response.__dict__.get("apellido"),
                    "alias": response.__dict__.get("alias"),
                    "email": response.__dict__.get("email"),
                    "pais": response.__dict__.get("pais"),
                    "edad": response.__dict__.get("edad"),
                    "fecha_creacion": response.__dict__.get("fecha_creacion"),
                    "fecha_modificacion": response.__dict__.get("fecha_modificacion")
                })
            else:
                raise APIError("No se encontró el usuario", 404)
        except Exception as e:
            raise APIError("Error en el servidor: " + str(e))


    def crearUsuario(self):
        try:
            data = request.get_json()
            print(data)
            # Validar datos con Marshmallow
            schema = UsuarioCreateSchema()
            validated_data = schema.load(data)
            validated_data['fecha_creacion'] = datetime.now()            
            usuario = usuario_mod.UsuarioModelo(**validated_data)
            response = self.app.crearUsuario(usuario)
            return jsonify(ResponseApi.exito("Usuario creado",{"id": response}))
        except ValidationError as e:
            raise APIError(e.messages)
        except Exception as e:
            raise APIError("Error en el servidor: " + str(e))

    def actualizarUsuario(self):
        try:
            data = request.get_json()
            
            # Validar datos con Marshmallow
            schema = UsuarioSchema()
            validated_data = schema.load(data)
            
            usuario = usuario_mod.UsuarioModelo(**validated_data)
            response = self.app.actualizarUsuario(usuario)
            return jsonify(ResponseApi.exito({"modified_count": response}, 200))
        except ValidationError as e:
            raise APIError(e.messages)
        except Exception as e:
            raise APIError("Error en el servidor: " + str(e))

    def desactivarUsuario(self):
        try:
            data = request.args.to_dict()
            idUsuario = int(data.get("idUsuario"))
            response = self.app.desactivarUsuario(idUsuario)
            return jsonify(ResponseApi.success_response({"id": response}, 200))
        except Exception as e:
            raise APIError("Error en el servidor: " + str(e))

    def autenticarUsuario(self):
        try:
            data = request.get_json()
            schema = AuthSchema()
            validated_data = schema.load(data)
            alias = validated_data['alias']
            password = validated_data['password']
            response = self.app.autenticarUsuario(alias, password)
            if response:
                return jsonify(ResponseApi.exito("Autenticación exitosa", response.__dict__))
            else:
                raise APIError("Alias o password incorrectos", 401)
        except Exception as e:
            raise APIError("Error en el servidor: " + str(e))