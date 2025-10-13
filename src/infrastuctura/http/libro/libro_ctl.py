from flask import request, jsonify, render_template, redirect, url_for, flash, current_app
from src.app.libro_app import LibroApp
from src.infrastuctura.dependencias import categoria_dep, tag_dep, genero_dep, idioma_dep, pais_dep
from src.util.responseApi import ResponseApi
from src.custom.error_custom import APIError
from marshmallow import Schema, fields, ValidationError
from typing import List
import os
from werkzeug.utils import secure_filename

class LibroCreateSchema(Schema):
    titulo = fields.String(required=True, validate=lambda x: len(x.strip()) > 0, 
                          error_messages={'required': 'El título es requerido', 'invalid': 'El título no puede estar vacío'})
    autor = fields.String(required=True, validate=lambda x: len(x.strip()) > 0,
                         error_messages={'required': 'El autor es requerido', 'invalid': 'El autor no puede estar vacío'})
    genero = fields.List(fields.String(), required=True, validate=lambda x: len(x) > 0,
                          error_messages={'required': 'El género es requerido', 'invalid': 'El género no puede estar vacío'})
    año_publicacion = fields.Integer(required=True, validate=lambda x: 1000 <= x <= 2025,
                                   error_messages={'required': 'El año de publicación es requerido', 'invalid': 'El año debe estar entre 1000 y 2025'})
    editorial = fields.String(required=True, validate=lambda x: len(x.strip()) > 0,
                             error_messages={'required': 'La editorial es requerida', 'invalid': 'La editorial no puede estar vacía'})
    paginas = fields.Integer(required=True, validate=lambda x: x > 0,
                           error_messages={'required': 'El número de páginas es requerido', 'invalid': 'El número de páginas debe ser mayor a 0'})
    idioma = fields.String(required=True, validate=lambda x: len(x.strip()) > 0,
                          error_messages={'required': 'El idioma es requerido', 'invalid': 'El idioma no puede estar vacío'})
    isbn = fields.String(required=True, validate=lambda x: len(x.strip()) > 0,
                        error_messages={'required': 'El ISBN es requerido', 'invalid': 'El ISBN no puede estar vacío'})
    categoria = fields.String(missing='')
    descripcion = fields.String(required=True, validate=lambda x: len(x.strip()) > 10,
                               error_messages={'required': 'La descripción es requerida', 'invalid': 'La descripción debe tener al menos 10 caracteres'})
    origen_pais = fields.String(required=True, validate=lambda x: len(x.strip()) > 0,
                               error_messages={'required': 'El país de origen es requerido', 'invalid': 'El país de origen no puede estar vacío'})
    disponible = fields.Boolean(missing=True)
    portada_url = fields.String(required=True, error_messages={'invalid': 'La URL de la portada debe ser válida'})
    tags = fields.List(fields.String(), missing=[])

class LibroUpdateSchema(LibroCreateSchema):
    # Hereda todos los campos de creación
    pass


class LibroControlador:
    def __init__(self, app: LibroApp):
        self.app = app

    def obtenerLibros(self):
        """Obtener lista de libros con filtros opcionales"""
        try:
            # Obtener parámetros de query: filtros, paginación y búsqueda
            filtros = {}
            if request.args.get('titulo'):
                filtros['titulo'] = request.args.get('titulo')
            if request.args.get('genero'):
                filtros['genero'] = request.args.get('genero')
            if request.args.get('autor'):
                filtros['autor'] = request.args.get('autor')
            if request.args.get('año_min'):
                filtros['año_min'] = int(request.args.get('año_min'))
            if request.args.get('año_max'):
                filtros['año_max'] = int(request.args.get('año_max'))
            if request.args.get('idioma'):
                filtros['idioma'] = request.args.get('idioma')
            if request.args.get('origen_pais'):
                filtros['origen_pais'] = request.args.get('origen_pais')
            if request.args.get('disponible') is not None:
                filtros['disponible'] = request.args.get('disponible').lower() == 'true'
            # Paginación lazy: offset/limit
            try:
                offset = int(request.args.get('offset', 0))
            except ValueError:
                offset = 0
            try:
                limit = int(request.args.get('limit', 6))
            except ValueError:
                limit = 6

            # Búsqueda por texto genérico (q)
            q = request.args.get('q')
            libros = self.app.obtenerLibros(filtros if filtros else None, offset=offset, limit=limit, q=q)

            # Convertir a dict para JSON
            libros_dict = [libro.__dict__ for libro in libros]

            return jsonify(ResponseApi.exito('Libro encontrados',{
                'libros': libros_dict,
                'total': len(libros_dict),
                'offset': offset,
                'limit': limit,
                'q': q
            }))
            
        except Exception as e:
            return jsonify(ResponseApi.error(f"Error al obtener libros: {str(e)}", 500))

    def obtenerLibro(self, libro_id: str):
        """Obtener un libro específico por ID"""
        try:
            libro = self.app.obtenerLibro(libro_id)
            if libro:
                return jsonify(ResponseApi.exito(libro.__dict__, 200))
            else:
                return jsonify(ResponseApi.error("Libro no encontrado", 404))
        except Exception as e:
            return jsonify(ResponseApi.error(f"Error al obtener libro: {str(e)}", 500))

    def crearLibro(self):
        """Crear un nuevo libro"""
        try:
            # Support JSON APIs and multipart/form-data (file upload from web form)
            if request.content_type and 'multipart/form-data' in request.content_type:
                # build data from form fields
                form = request.form
                print(form)
                data = {
                    'titulo': form.get('titulo'),
                    'autor': form.get('autor'),
                    'genero': form.get('genero').split(','),
                    'año_publicacion': int(form.get('año_publicacion')) if form.get('año_publicacion') else None,
                    'editorial': form.get('editorial'),
                    'paginas': int(form.get('paginas')) if form.get('paginas') else None,
                    'idioma': form.get('idioma'),
                    'categoria': form.get('categoria') or '',
                    'descripcion': form.get('descripcion'),
                    'origen_pais': form.get('origen_pais'),
                    'isbn': form.get('isbn'),
                    'disponible': True,
                    'tags': form.get('tags').split(',') 
                }
                print(data)
                # handle file upload
                portada = request.files.get('portada')
                if portada and portada.filename:
                    uploads_dir = os.path.join(current_app.root_path, 'static', 'uploads')
                    try:
                        os.makedirs(uploads_dir, exist_ok=True)
                    except Exception:
                        pass
                    filename = secure_filename(portada.filename)
                    # avoid collisions
                    import time, uuid
                    suffix = str(int(time.time())) + '_' + uuid.uuid4().hex[:6]
                    name, ext = os.path.splitext(filename)
                    filename_safe = f"{name}_{suffix}{ext}"
                    dest = os.path.join(uploads_dir, filename_safe)
                    portada.save(dest)
                    # set accessible URL
                    data['portada_url'] = url_for('static', filename=f'uploads/{filename_safe}', _external=False)

            else:
                data = request.get_json()

            # Validar datos con Marshmallow
            schema = LibroCreateSchema()
            validated_data = schema.load(data)

            # Crear libro
            libro_id = self.app.crearLibro(validated_data)

            return jsonify(ResponseApi.exito({
                'message': 'Libro creado exitosamente',
                'libro_id': libro_id
            }, 201))
            
        except ValidationError as e:
            print(e.messages)
            return jsonify(ResponseApi.error(f"Error de validación: {e.messages}", 400))
        except ValueError as e:
            print(e)
            return jsonify(ResponseApi.error(f"Error de datos: {str(e)}", 400))
        except Exception as e:
            print(e)
            return jsonify(ResponseApi.error(f"Error en el servidor: {str(e)}", 500))

    def actualizarLibro(self, libro_id: str):
        """Actualizar un libro existente"""
        try:
            # Support JSON APIs and multipart/form-data (editing from web form)
            if request.content_type and 'multipart/form-data' in request.content_type:
                form = request.form
                # Build dict from form (similar to crearLibro)
                data = {
                    'titulo': form.get('titulo'),
                    'autor': form.get('autor'),
                    'genero': form.get('genero').split(',') if form.get('genero') else [],
                    'año_publicacion': int(form.get('año_publicacion')) if form.get('año_publicacion') else None,
                    'editorial': form.get('editorial'),
                    'paginas': int(form.get('paginas')) if form.get('paginas') else None,
                    'idioma': form.get('idioma'),
                    'categoria': form.get('categoria') or '',
                    'descripcion': form.get('descripcion'),
                    'origen_pais': form.get('origen_pais'),
                    'isbn': form.get('isbn'),
                    'disponible': True,
                    'tags': form.get('tags').split(',') if form.get('tags') else []
                }

                # handle file upload (portada)
                portada = request.files.get('portada')
                if portada and portada.filename:
                    uploads_dir = os.path.join(current_app.root_path, 'static', 'uploads')
                    try:
                        os.makedirs(uploads_dir, exist_ok=True)
                    except Exception:
                        pass
                    filename = secure_filename(portada.filename)
                    import time, uuid
                    suffix = str(int(time.time())) + '_' + uuid.uuid4().hex[:6]
                    name, ext = os.path.splitext(filename)
                    filename_safe = f"{name}_{suffix}{ext}"
                    dest = os.path.join(uploads_dir, filename_safe)
                    portada.save(dest)
                    data['portada_url'] = url_for('static', filename=f'uploads/{filename_safe}', _external=False)
            else:
                data = request.get_json()

            # Validar datos con Marshmallow
            schema = LibroUpdateSchema()
            validated_data = schema.load(data)

            # Actualizar libro
            modified_count = self.app.actualizarLibro(libro_id, validated_data)
            
            if modified_count > 0:
                return jsonify(ResponseApi.exito('Libro actualizado exitosamente',{
                    'modified_count': modified_count
                }))
            else:
                return jsonify(ResponseApi.error("No se pudo actualizar el libro", 400))
                
        except ValidationError as e:
            return jsonify(ResponseApi.error(f"Error de validación: {e.messages}", 400))
        except ValueError as e:
            return jsonify(ResponseApi.error(f"Error de datos: {str(e)}", 400))
        except Exception as e:
            return jsonify(ResponseApi.error(f"Error en el servidor: {str(e)}", 500))

    def eliminarLibro(self, libro_id: str):
        """Eliminar (desactivar) un libro"""
        try:
            print(libro_id)
            success = self.app.eliminarLibro(libro_id)
            
            if success:
                return jsonify(ResponseApi.exito({
                    'message': 'Libro eliminado exitosamente'
                }, 200))
            else:
                return jsonify(ResponseApi.error("No se pudo eliminar el libro", 400))
                
        except ValueError as e:
            return jsonify(ResponseApi.error(str(e), 400))
        except Exception as e:
            return jsonify(ResponseApi.error(f"Error en el servidor: {str(e)}", 500))



    # --- Vistas web ---
    def lista_libros(self):
        """Renderiza la lista de libros en una plantilla web"""
        try:
            # Obtener primeros 10 libros para la vista inicial (lazy load)
            primeros = self.app.obtenerLibros(None, offset=0, limit=6)

            libros_list = [libro.__dict__ for libro in primeros]
            return render_template('books/list.html', libros=libros_list, initial_limit=6)
        except Exception as e:
            # Para la vista web, mostramos un mensaje flash y redirigimos al dashboard
            flash(f"Error al obtener libros: {str(e)}", 'danger')
            return redirect(url_for('auth.dashboard'))

    def crear_libro_web(self):
        """Maneja el formulario web para crear un libro (GET muestra formulario, POST lo procesa)"""
        # try:
            # Soporta edición: si viene edit_id en query params, cargar libro y prellenar
        edit_id = request.args.get('edit_id') if request.method == 'GET' else request.form.get('edit_id')
        if request.method == 'GET':
            # Preload categorias, tags y generos para los selects
            categorias = []
            tags = []
            generos = []
            idiomas = []
            paises = []
            try:
                categorias = [c.__dict__ for c in categoria_dep.categoria_app.obtenerCategorias()]
            except Exception:
                categorias = []
            try:
                tags = [t.__dict__ for t in tag_dep.tag_app.obtenerTags()]
            except Exception:
                tags = []
            try:
                generos = [g.__dict__ for g in genero_dep.genero_app.obtenerGeneros()]
            except Exception:
                generos = []
            try:
                idiomas = [i.__dict__ for i in idioma_dep.idioma_app.obtenerIdiomas()]
            except Exception:
                idiomas = []
            try:
                paises = [p.__dict__ for p in pais_dep.pais_app.obtenerPaises()]
            except Exception:
                paises = []

            if edit_id:
                libro = self.app.obtenerLibro(edit_id)
                if libro:
                    data = libro.__dict__
                    return render_template('books/create.html', data=data, categorias=categorias, tags=tags, generos=generos, idiomas=idiomas, paises=paises)
            return render_template('books/create.html', categorias=categorias, tags=tags, generos=generos, idiomas=idiomas, paises=paises)