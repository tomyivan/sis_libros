from flask import request, jsonify, render_template, redirect, url_for, flash
from src.app.tag_app import TagApp
from src.util.responseApi import ResponseApi
from marshmallow import Schema, fields, ValidationError

class TagSchema(Schema):
    nombre = fields.String(required=True)
    descripcion = fields.String(missing='')
    activo = fields.Boolean(missing=True)

class TagControlador:
    def __init__(self, app: TagApp):
        self.app = app

    def obtenerTags(self):
        try:
            # Paginación y búsqueda básica
            try:
                offset = int(request.args.get('offset', 0))
            except ValueError:
                offset = 0
            try:
                limit = int(request.args.get('limit', 10))
            except ValueError:
                limit = 10
            q = request.args.get('q')

            tags = self.app.obtenerTags(offset=offset, limit=limit, q=q)
            tags_dict = [t.__dict__ for t in tags]
            return jsonify(ResponseApi.exito({'tags': tags_dict, 'total': len(tags_dict), 'offset': offset, 'limit': limit, 'q': q}, 200))
        except Exception as e:
            return jsonify(ResponseApi.error(str(e), 500))

    def obtenerTag(self, tag_id: str):
        try:
            t = self.app.obtenerTag(tag_id)
            if t:
                return jsonify(ResponseApi.exito(t.__dict__, 200))
            return jsonify(ResponseApi.error('No encontrada', 404))
        except Exception as e:
            return jsonify(ResponseApi.error(str(e), 500))

    def crearTag(self):
        try:
            data = request.get_json() if request.is_json else request.form.to_dict()
            # Extraer edit_id si viene del formulario/modal
            if isinstance(data, dict) and 'edit_id' in data:
                data.pop('edit_id', None)

            schema = TagSchema()
            validated = schema.load(data)
            tag_id = self.app.crearTag(validated)
            if request.is_json:
                return jsonify(ResponseApi.exito({'tag_id': tag_id}, 201))
            flash('Tag creado', 'success')
            return redirect(url_for('tag.lista_tags_web'))
        except ValidationError as ve:
            if request.is_json:
                return jsonify(ResponseApi.error(str(ve.messages), 400))
            flash(f'Error: {ve.messages}', 'warning')
            return render_template('tag/create.html', data=data, errors=ve.messages)
        except Exception as e:
            return jsonify(ResponseApi.error(str(e), 500))

    def actualizarTag(self, tag_id: str):
        try:
            data = request.get_json() if request.is_json else request.form.to_dict()
            schema = TagSchema()
            validated = schema.load(data)
            modified = self.app.actualizarTag(tag_id, validated)
            return jsonify(ResponseApi.exito({'modified': modified}, 200))
        except ValidationError as ve:
            return jsonify(ResponseApi.error(str(ve.messages), 400))
        except Exception as e:
            return jsonify(ResponseApi.error(str(e), 500))

    def eliminarTag(self, tag_id: str):
        try:
            success = self.app.eliminarTag(tag_id)
            return jsonify(ResponseApi.exito({'deleted': success}, 200))
        except Exception as e:
            return jsonify(ResponseApi.error(str(e), 500))

    # Web views
    def lista_tags(self):
        try:
            primeros = self.app.obtenerTags(offset=0, limit=10)
            tags_list = [t.__dict__ for t in primeros]
            return render_template('tag/list.html', tags=tags_list, initial_limit=10)
        except Exception as e:
            print(e)
            flash('Error al listar tags', 'danger')
            return redirect(url_for('dashboard'))