from flask import request, jsonify, render_template, redirect, url_for, flash
from src.app.pais_app import PaisApp
from src.util.responseApi import ResponseApi
from marshmallow import Schema, fields, ValidationError


class PaisSchema(Schema):
    nombre = fields.String(required=True)


class PaisControlador:
    def __init__(self, app: PaisApp):
        self.app = app

    def obtenerPaises(self):
        try:
            try:
                offset = int(request.args.get('offset', 0))
            except ValueError:
                offset = 0
            try:
                limit = int(request.args.get('limit', 10))
            except ValueError:
                limit = 10
            q = request.args.get('q')

            paises = self.app.obtenerPaises(offset=offset, limit=limit, q=q)
            paises_dict = [p.__dict__ for p in paises]
            return jsonify(ResponseApi.exito({'paises': paises_dict, 'total': len(paises_dict), 'offset': offset, 'limit': limit, 'q': q}, 200))
        except Exception as e:
            return jsonify(ResponseApi.error(str(e), 500))

    def obtenerPais(self, pais_id: str):
        try:
            p = self.app.obtenerPais(pais_id)
            if p:
                return jsonify(ResponseApi.exito(p.__dict__, 200))
            return jsonify(ResponseApi.error('No encontrada', 404))
        except Exception as e:
            return jsonify(ResponseApi.error(str(e), 500))

    def crearPais(self):
        try:
            data = request.get_json() if request.is_json else request.form.to_dict()
            if isinstance(data, dict) and 'edit_id' in data:
                data.pop('edit_id', None)

            schema = PaisSchema()
            validated = schema.load(data)
            pais_id = self.app.crearPais(validated)
            if request.is_json:
                return jsonify(ResponseApi.exito({'pais_id': pais_id}, 201))
            flash('País creado', 'success')
            return redirect(url_for('pais.lista_paises_web'))
        except ValidationError as ve:
            if request.is_json:
                return jsonify(ResponseApi.error(str(ve.messages), 400))
            flash(f'Error: {ve.messages}', 'warning')
            return render_template('pais/create.html', data=data, errors=ve.messages)
        except Exception as e:
            return jsonify(ResponseApi.error(str(e), 500))

    def actualizarPais(self, pais_id: str):
        try:
            data = request.get_json() if request.is_json else request.form.to_dict()
            schema = PaisSchema()
            validated = schema.load(data)
            modified = self.app.actualizarPais(pais_id, validated)
            return jsonify(ResponseApi.exito({'modified': modified}, 200))
        except ValidationError as ve:
            return jsonify(ResponseApi.error(str(ve.messages), 400))
        except Exception as e:
            return jsonify(ResponseApi.error(str(e), 500))

    def eliminarPais(self, pais_id: str):
        try:
            success = self.app.eliminarPais(pais_id)
            return jsonify(ResponseApi.exito({'deleted': success}, 200))
        except Exception as e:
            return jsonify(ResponseApi.error(str(e), 500))

    # Web views
    def lista_paises(self):
        try:
            primeros = self.app.obtenerPaises(offset=0, limit=10)
            paises_list = [p.__dict__ for p in primeros]
            return render_template('pais/list.html', paises=paises_list, initial_limit=10)
        except Exception as e:
            print(e)
            flash('Error al listar países', 'danger')
            return redirect(url_for('dashboard'))
