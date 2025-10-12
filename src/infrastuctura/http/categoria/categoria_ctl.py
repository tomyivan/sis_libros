from flask import request, jsonify, render_template, redirect, url_for, flash
from src.app.categoria_app import CategoriaApp
from src.util.responseApi import ResponseApi
from marshmallow import Schema, fields, ValidationError

class CategoriaSchema(Schema):
    nombre = fields.String(required=True)
    descripcion = fields.String(missing='')
    activo = fields.Boolean(missing=True)

class CategoriaControlador:
    def __init__(self, app: CategoriaApp):
        self.app = app

    def obtenerCategorias(self):
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

            categorias = self.app.obtenerCategorias(offset=offset, limit=limit, q=q)
            categorias_dict = [c.__dict__ for c in categorias]
            return jsonify(ResponseApi.exito({'categorias': categorias_dict, 'total': len(categorias_dict), 'offset': offset, 'limit': limit, 'q': q}, 200))
        except Exception as e:
            return jsonify(ResponseApi.error(str(e), 500))

    def obtenerCategoria(self, categoria_id: str):
        try:
            cat = self.app.obtenerCategoria(categoria_id)
            if cat:
                return jsonify(ResponseApi.exito(cat.__dict__, 200))
            return jsonify(ResponseApi.error('No encontrada', 404))
        except Exception as e:
            return jsonify(ResponseApi.error(str(e), 500))

    def crearCategoria(self):
        try:
            data = request.get_json() if request.is_json else request.form.to_dict()

            # Extraer edit_id si viene del formulario/modal y no hacerlo pasar al schema
            schema = CategoriaSchema()
            validated = schema.load(data)
            categoria_id = self.app.crearCategoria(validated)
            if request.is_json:
                return jsonify(ResponseApi.exito({'categoria_id': categoria_id}, 201))
            flash('Categoría creada', 'success')
            return redirect(url_for('categoria.lista_categorias'))
        except ValidationError as ve:
            if request.is_json:
                return jsonify(ResponseApi.error(str(ve.messages), 400))
            flash(f'Error: {ve.messages}', 'warning')
            return render_template('categoria/create.html', data=data, errors=ve.messages)
        except Exception as e:
            return jsonify(ResponseApi.error(str(e), 500))

    def actualizarCategoria(self, categoria_id: str):
        try:
            data = request.get_json() if request.is_json else request.form.to_dict()
            schema = CategoriaSchema()
            validated = schema.load(data)
            modified = self.app.actualizarCategoria(categoria_id, validated)
            return jsonify(ResponseApi.exito({'modified': modified}, 200))
        except ValidationError as ve:
            return jsonify(ResponseApi.error(str(ve.messages), 400))
        except Exception as e:
            return jsonify(ResponseApi.error(str(e), 500))

    def eliminarCategoria(self, categoria_id: str):
        try:
            success = self.app.eliminarCategoria(categoria_id)
            return jsonify(ResponseApi.exito({'deleted': success}, 200))
        except Exception as e:
            return jsonify(ResponseApi.error(str(e), 500))

    # Web views
    def lista_categorias(self):
        try:
            primeros = self.app.obtenerCategorias(offset=0, limit=10)
            categorias_list = [c.__dict__ for c in primeros]
            return render_template('categoria/list.html', categorias=categorias_list, initial_limit=10)
        except Exception as e:
            print(e)
            flash('Error al listar categorías', 'danger')
            return redirect(url_for('dashboard'))

    def crear_categoria_web(self):
        if request.method == 'GET':
            return render_template('categoria/create.html')
        return self.crearCategoria()
