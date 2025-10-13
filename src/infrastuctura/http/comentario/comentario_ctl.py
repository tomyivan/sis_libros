from flask import request, jsonify
from src.app.comentario_app import ComentarioApp
from src.util.responseApi import ResponseApi
from marshmallow import Schema, fields, ValidationError
from src.dominio.modelos import comentarios_mod

class ComentarioCreateSchema(Schema):
    idUsuario = fields.String(required=True)
    idLibro = fields.String(required=True)
    comentario = fields.String(required=True)


class ComentarioControlador:
    def __init__(self, app: ComentarioApp):
        self.app = app

    def crearComentario(self):
        try:
            data = request.get_json()
            schema = ComentarioCreateSchema()
            validated = schema.load(data)
            comentario_model = comentarios_mod.ComentarioModelo(**validated)
            cid = self.app.crearComentario(comentario_model)
            return jsonify(ResponseApi.exito({'comentario_id': cid}, 201))
        except ValidationError as e:
            return jsonify(ResponseApi.error(f"Error de validación: {e.messages}", 400))
        except Exception as e:
            return jsonify(ResponseApi.error(f"Error en el servidor: {str(e)}", 500))

    def obtenerComentario(self):
        try:
            filtro = comentarios_mod.FiltroComentarioModelo(
                idUsuario=request.args.get('idUsuario'),
                idLibro=request.args.get('idLibro'),
                _id=request.args.get('_id')
            )
            res = self.app.obtenerComentario(filtro)
            # serialize list of DTOs
            if res is None:
                return jsonify(ResponseApi.exito([], 200))
            out = [c.__dict__ if hasattr(c, '__dict__') else c for c in res]
            return jsonify(ResponseApi.exito(out, 200))
        except Exception as e:
            return jsonify(ResponseApi.error(f"Error al obtener comentarios: {str(e)}", 500))

    def actualizarComentario(self, comentarioId: str):
        try:
            data = request.get_json()
            schema = ComentarioCreateSchema()
            validated = schema.load(data)
            comentario_model = comentarios_mod.ComentarioModelo(**validated)
            modified = self.app.actualizarComentario(comentario_model, comentarioId)
            return jsonify(ResponseApi.exito({'modified_count': modified}, 200))
        except ValidationError as e:
            return jsonify(ResponseApi.error(f"Error de validación: {e.messages}", 400))
        except Exception as e:
            return jsonify(ResponseApi.error(f"Error en el servidor: {str(e)}", 500))

    def eliminarComentario(self, comentarioId: str):
        try:
            ok = self.app.eliminarComentario(comentarioId)
            return jsonify(ResponseApi.exito({'deleted': ok}, 200))
        except Exception as e:
            return jsonify(ResponseApi.error(f"Error en el servidor: {str(e)}", 500))
