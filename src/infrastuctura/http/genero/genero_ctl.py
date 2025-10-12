from flask import request, jsonify, render_template, redirect, url_for, flash
from src.app.genero_app import GeneroApp
from src.util.responseApi import ResponseApi
from marshmallow import Schema, fields, ValidationError
from src.dominio.modelos.genero_mod import GeneroModelo


class GeneroSchema(Schema):
    nombre = fields.String(required=True)
    descripcion = fields.String(missing='')
    activo = fields.Boolean(missing=True)


class GeneroControlador:
    def __init__(self, app: GeneroApp):
        self.app = app

    def obtenerGeneros(self):
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

            generos = self.app.obtenerGeneros(offset=offset, limit=limit, q=q)
            generos_dict = [g.__dict__ for g in generos]
            return jsonify(ResponseApi.exito({'generos': generos_dict, 'total': len(generos_dict), 'offset': offset, 'limit': limit, 'q': q}, 200))
        except Exception as e:
            return jsonify(ResponseApi.error(str(e), 500))

    def obtenerGenero(self, genero_id: str):
        try:
            g = self.app.obtenerGenero(genero_id)
            if g:
                return jsonify(ResponseApi.exito(g.__dict__, 200))
            return jsonify(ResponseApi.error('No encontrado', 404))
        except Exception as e:
            return jsonify(ResponseApi.error(str(e), 500))

    def crearGenero(self):
        try:
            data = request.get_json() if request.is_json else request.form.to_dict()
            schema = GeneroSchema()
            validated = schema.load(data)
            genero_id = self.app.crearGenero(validated)
            if request.is_json:
                return jsonify(ResponseApi.exito({'genero_id': genero_id}, 201))
            flash('Género creado', 'success')
            return redirect(url_for('genero.lista_generos_web'))
        except ValidationError as ve:
            if request.is_json:
                return jsonify(ResponseApi.error(str(ve.messages), 400))
            flash(f'Error: {ve.messages}', 'warning')
            return render_template('genero/create.html', data=data, errors=ve.messages)
        except Exception as e:
            return jsonify(ResponseApi.error(str(e), 500))

    def actualizarGenero(self, genero_id: str):
        try:
            data = request.get_json() if request.is_json else request.form.to_dict()
            schema = GeneroSchema()
            validated = schema.load(data)
            modified = self.app.actualizarGenero(genero_id, validated)
            return jsonify(ResponseApi.exito({'modified': modified}, 200))
        except ValidationError as ve:
            return jsonify(ResponseApi.error(str(ve.messages), 400))
        except Exception as e:
            return jsonify(ResponseApi.error(str(e), 500))

    def eliminarGenero(self, genero_id: str):
        try:
            success = self.app.eliminarGenero(genero_id)
            return jsonify(ResponseApi.exito({'deleted': success}, 200))
        except Exception as e:
            return jsonify(ResponseApi.error(str(e), 500))

    # Web views
    def lista_generos(self):
        try:
            primeros = self.app.obtenerGeneros(offset=0, limit=10)
            generos_list = [g.__dict__ for g in primeros]
            return render_template('genero/list.html', categorias=generos_list, initial_limit=10)
        except Exception as e:
            print(e)
            flash('Error al listar géneros', 'danger')
            return redirect(url_for('dashboard'))
