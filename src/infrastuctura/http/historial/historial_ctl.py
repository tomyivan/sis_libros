import src.app.historial_app as historial_app
from flask import Blueprint, request, jsonify, session
from src.util.responseApi import ResponseApi
from marshmallow import Schema, fields, ValidationError

class HistorialSchema(Schema):
    textoBusqueda = fields.String(required=True)

class HistorialControlador:
    def __init__(self, app: historial_app.HistoriaApp):
        self.app = app

    def obtenerHistorial(self, q: str = None):
        try: 
            idUsuario = session.get('user_id')
            historiales = self.app.obtenerHistorial(idUsuario, q)
            historiales_dict = [h.__dict__ for h in historiales]
            return jsonify(ResponseApi.exito('historiales obtenidos',{'historiales': historiales_dict, 'total': len(historiales_dict), 'q': q}))
        except Exception as e:
            print(f"Error al obtener historiales: {e}")
            raise ValueError(f'Error al obtener historiales: {str(e)}')

    def crearHistorial(self):
        try:
            data = request.get_json() if request.is_json else request.form.to_dict()

            schema = HistorialSchema()
            validated = schema.load(data)
            idUsuario = session.get('user_id')
            historial_id = self.app.registrarHistorial({**validated, 'idUsuario': idUsuario})
            
            return jsonify(ResponseApi.exito('Historia creada',{'historial_id': historial_id}))
        except ValidationError as ve:
            raise ValueError(f'Error de validación: {ve.messages}')
        except Exception as e:
            raise ValueError(f'Error al crear historia: {str(e)}')

