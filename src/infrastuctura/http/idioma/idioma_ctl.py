from flask import request, jsonify, render_template, redirect, url_for, flash
from src.app.idioma_app import IdiomaApp
from src.util.responseApi import ResponseApi
from marshmallow import Schema, fields, ValidationError


class IdiomaSchema(Schema):
    nombre = fields.String(required=True)


class IdiomaControlador:
    def __init__(self, app: IdiomaApp):
        self.app = app

    def obtenerIdiomas(self):
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

            idiomas = self.app.obtenerIdiomas(offset=offset, limit=limit, q=q)
            idiomas_dict = [p.__dict__ for p in idiomas]
            return jsonify(ResponseApi.exito({'idiomas': idiomas_dict, 'total': len(idiomas_dict), 'offset': offset, 'limit': limit, 'q': q}, 200))
        except Exception as e:
            return jsonify(ResponseApi.error(str(e), 500))

    def obtenerIdioma(self, idioma_id: str):
        try:
            p = self.app.obtenerIdioma(idioma_id)
            if p:
                return jsonify(ResponseApi.exito(p.__dict__, 200))
            return jsonify(ResponseApi.error('No encontrada', 404))
        except Exception as e:
            return jsonify(ResponseApi.error(str(e), 500))

    def crearIdioma(self):
        try:
            data = request.get_json() if request.is_json else request.form.to_dict()
            if isinstance(data, dict) and 'edit_id' in data:
                data.pop('edit_id', None)

            schema = IdiomaSchema()
            validated = schema.load(data)
            idioma_id = self.app.crearIdioma(validated)
            if request.is_json:
                return jsonify(ResponseApi.exito({'idioma_id': idioma_id}, 201))
            flash('Idioma creado', 'success')
            return redirect(url_for('idioma.lista_idiomas_web'))
        except ValidationError as ve:
            if request.is_json:
                return jsonify(ResponseApi.error(str(ve.messages), 400))
            flash(f'Error: {ve.messages}', 'warning')
            return render_template('idioma/create.html', data=data, errors=ve.messages)
        except Exception as e:
            return jsonify(ResponseApi.error(str(e), 500))

    def actualizarIdioma(self, idioma_id: str):
        try:
            data = request.get_json() if request.is_json else request.form.to_dict()
            schema = IdiomaSchema()
            validated = schema.load(data)
            modified = self.app.actualizarIdioma(idioma_id, validated)
            return jsonify(ResponseApi.exito({'modified': modified}, 200))
        except ValidationError as ve:
            return jsonify(ResponseApi.error(str(ve.messages), 400))
        except Exception as e:
            return jsonify(ResponseApi.error(str(e), 500))

    def eliminarIdioma(self, idioma_id: str):
        try:
            success = self.app.eliminarIdioma(idioma_id)
            return jsonify(ResponseApi.exito({'deleted': success}, 200))
        except Exception as e:
            return jsonify(ResponseApi.error(str(e), 500))

    # Web views
    def lista_idiomas(self):
        try:
            primeros = self.app.obtenerIdiomas(offset=0, limit=10)
            idiomas_list = [p.__dict__ for p in primeros]
            return render_template('idioma/list.html', idiomas=idiomas_list, initial_limit=10)
        except Exception as e:
            print(e)
            flash('Error al listar idiomas', 'danger')
            return redirect(url_for('dashboard'))