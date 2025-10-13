from flask import request, jsonify
from src.app.calificacion_app import CalificacionApp
from src.util.responseApi import ResponseApi
from marshmallow import Schema, fields, ValidationError
from src.dominio.modelos import calificacion_mod

class CalificacionCreateSchema(Schema):
    idUsuario = fields.String(required=True)
    idLibro = fields.String(required=True)
    calificacion = fields.Integer(required=True)


class CalificacionControlador:
    def __init__(self, app: CalificacionApp):
        self.app = app

    def crearCalificacion(self):
        try:
            data = request.get_json()
            schema = CalificacionCreateSchema()
            validated = schema.load(data)
            cal_model = calificacion_mod.CalificacionModelo(**validated)
            cid = self.app.crearCalificacion(cal_model)
            return jsonify(ResponseApi.exito({'calificacion_id': cid}, 201))
        except ValidationError as e:
            return jsonify(ResponseApi.error(f"Error de validación: {e.messages}", 400))
        except Exception as e:
            return jsonify(ResponseApi.error(f"Error en el servidor: {str(e)}", 500))

    def obtenerCalificacion(self):
        try:
            filtro = calificacion_mod.FiltroCalificacionModelo(
                idUsuario=request.args.get('idUsuario'),
                idLibro=request.args.get('idLibro'),
                _id=request.args.get('_id')
            )
            res = self.app.obtenerCalificacion(filtro)
            if res is None:
                return jsonify(ResponseApi.exito(None, 200))
            # if DTO, return dict
            out = res.__dict__ if hasattr(res, '__dict__') else res
            return jsonify(ResponseApi.exito(out, 200))
        except Exception as e:
            return jsonify(ResponseApi.error(f"Error al obtener calificaciones: {str(e)}", 500))

    def actualizarCalificacion(self, calificacionId: str):
        try:
            data = request.get_json()
            schema = CalificacionCreateSchema()
            validated = schema.load(data)
            cal_model = calificacion_mod.CalificacionModelo(**validated)
            modified = self.app.actualizarCalificacion(cal_model, calificacionId)
            return jsonify(ResponseApi.exito({'modified_count': modified}, 200))
        except ValidationError as e:
            return jsonify(ResponseApi.error(f"Error de validación: {e.messages}", 400))
        except Exception as e:
            return jsonify(ResponseApi.error(f"Error en el servidor: {str(e)}", 500))

    def eliminarCalificacion(self, calificacionId: str):
        try:
            ok = self.app.eliminarCalificacion(calificacionId)
            return jsonify(ResponseApi.exito({'deleted': ok}, 200))
        except Exception as e:
            return jsonify(ResponseApi.error(f"Error en el servidor: {str(e)}", 500))
