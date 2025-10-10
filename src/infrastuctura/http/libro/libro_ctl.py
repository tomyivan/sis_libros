from flask import request, jsonify, render_template, redirect, url_for, flash
from src.app.libro_app import LibroApp
from src.util.responseApi import ResponseApi
from src.custom.error_custom import APIError
from marshmallow import Schema, fields, ValidationError
from typing import List

class LibroCreateSchema(Schema):
    titulo = fields.String(required=True, validate=lambda x: len(x.strip()) > 0, 
                          error_messages={'required': 'El título es requerido', 'invalid': 'El título no puede estar vacío'})
    autor = fields.String(required=True, validate=lambda x: len(x.strip()) > 0,
                         error_messages={'required': 'El autor es requerido', 'invalid': 'El autor no puede estar vacío'})
    genero = fields.String(required=True, validate=lambda x: len(x.strip()) > 0,
                          error_messages={'required': 'El género es requerido', 'invalid': 'El género no puede estar vacío'})
    año_publicacion = fields.Integer(required=True, validate=lambda x: 1000 <= x <= 2025,
                                   error_messages={'required': 'El año de publicación es requerido', 'invalid': 'El año debe estar entre 1000 y 2025'})
    editorial = fields.String(required=True, validate=lambda x: len(x.strip()) > 0,
                             error_messages={'required': 'La editorial es requerida', 'invalid': 'La editorial no puede estar vacía'})
    isbn = fields.String(required=True, validate=lambda x: len(x.replace('-', '').replace(' ', '')) in [10, 13],
                        error_messages={'required': 'El ISBN es requerido', 'invalid': 'El ISBN debe tener 10 o 13 dígitos'})
    paginas = fields.Integer(required=True, validate=lambda x: x > 0,
                           error_messages={'required': 'El número de páginas es requerido', 'invalid': 'El número de páginas debe ser mayor a 0'})
    idioma = fields.String(required=True, validate=lambda x: len(x.strip()) > 0,
                          error_messages={'required': 'El idioma es requerido', 'invalid': 'El idioma no puede estar vacío'})
    descripcion = fields.String(required=True, validate=lambda x: len(x.strip()) > 10,
                               error_messages={'required': 'La descripción es requerida', 'invalid': 'La descripción debe tener al menos 10 caracteres'})
    origen_pais = fields.String(required=True, validate=lambda x: len(x.strip()) > 0,
                               error_messages={'required': 'El país de origen es requerido', 'invalid': 'El país de origen no puede estar vacío'})
    disponible = fields.Boolean(missing=True)
    portada_url = fields.Url(allow_none=True, error_messages={'invalid': 'La URL de la portada debe ser válida'})
    tags = fields.List(fields.String(), missing=[])

class LibroUpdateSchema(LibroCreateSchema):
    # Hereda todos los campos de creación
    pass

class CalificacionSchema(Schema):
    calificacion = fields.Float(required=True, validate=lambda x: 1.0 <= x <= 5.0,
                               error_messages={'required': 'La calificación es requerida', 'invalid': 'La calificación debe estar entre 1.0 y 5.0'})

class BusquedaSchema(Schema):
    texto = fields.String(required=True, validate=lambda x: len(x.strip()) >= 3,
                         error_messages={'required': 'El texto de búsqueda es requerido', 'invalid': 'El texto debe tener al menos 3 caracteres'})

class LibroControlador:
    def __init__(self, app: LibroApp):
        self.app = app

    def obtenerLibros(self):
        """Obtener lista de libros con filtros opcionales"""
        try:
            # Obtener parámetros de query
            filtros = {}
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

            libros = self.app.obtenerLibros(filtros if filtros else None)
            
            # Convertir a dict para JSON
            libros_dict = [libro.__dict__ for libro in libros]
            
            return jsonify(ResponseApi.exito({
                'libros': libros_dict,
                'total': len(libros_dict)
            }, 200))
            
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
            return jsonify(ResponseApi.error(f"Error de validación: {e.messages}", 400))
        except ValueError as e:
            return jsonify(ResponseApi.error(f"Error de datos: {str(e)}", 400))
        except Exception as e:
            return jsonify(ResponseApi.error(f"Error en el servidor: {str(e)}", 500))

    def actualizarLibro(self, libro_id: str):
        """Actualizar un libro existente"""
        try:
            data = request.get_json()
            
            # Validar datos con Marshmallow
            schema = LibroUpdateSchema()
            validated_data = schema.load(data)
            
            # Actualizar libro
            modified_count = self.app.actualizarLibro(libro_id, validated_data)
            
            if modified_count > 0:
                return jsonify(ResponseApi.exito({
                    'message': 'Libro actualizado exitosamente',
                    'modified_count': modified_count
                }, 200))
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

    def reactivarLibro(self, libro_id: str):
        """Reactivar un libro previamente eliminado"""
        try:
            success = self.app.reactivarLibro(libro_id)
            
            if success:
                return jsonify(ResponseApi.exito({
                    'message': 'Libro reactivado exitosamente'
                }, 200))
            else:
                return jsonify(ResponseApi.error("No se pudo reactivar el libro", 400))
                
        except ValueError as e:
            return jsonify(ResponseApi.error(str(e), 400))
        except Exception as e:
            return jsonify(ResponseApi.error(f"Error en el servidor: {str(e)}", 500))

    def buscarLibros(self):
        """Buscar libros por texto"""
        try:
            data = request.args.to_dict() if request.method == 'GET' else request.get_json()
            
            # Validar datos
            schema = BusquedaSchema()
            validated_data = schema.load(data)
            
            libros = self.app.buscarLibros(validated_data['texto'])
            
            # Convertir a dict para JSON
            libros_dict = [libro.__dict__ for libro in libros]
            
            return jsonify(ResponseApi.exito({
                'libros': libros_dict,
                'total': len(libros_dict),
                'termino_busqueda': validated_data['texto']
            }, 200))
            
        except ValidationError as e:
            return jsonify(ResponseApi.error(f"Error de validación: {e.messages}", 400))
        except Exception as e:
            return jsonify(ResponseApi.error(f"Error en el servidor: {str(e)}", 500))

    def calificarLibro(self, libro_id: str):
        """Agregar una calificación a un libro"""
        try:
            data = request.get_json()
            
            # Validar datos
            schema = CalificacionSchema()
            validated_data = schema.load(data)
            
            modified_count = self.app.calificarLibro(libro_id, validated_data['calificacion'])
            
            if modified_count > 0:
                return jsonify(ResponseApi.exito({
                    'message': 'Calificación agregada exitosamente',
                    'calificacion': validated_data['calificacion']
                }, 200))
            else:
                return jsonify(ResponseApi.error("No se pudo agregar la calificación", 400))
                
        except ValidationError as e:
            return jsonify(ResponseApi.error(f"Error de validación: {e.messages}", 400))
        except ValueError as e:
            return jsonify(ResponseApi.error(str(e), 400))
        except Exception as e:
            return jsonify(ResponseApi.error(f"Error en el servidor: {str(e)}", 500))

    def obtenerLibrosPorGenero(self, genero: str):
        """Obtener libros por género"""
        try:
            libros = self.app.obtenerLibrosPorGenero(genero)
            
            # Convertir a dict para JSON
            libros_dict = [libro.__dict__ for libro in libros]
            
            return jsonify(ResponseApi.exito({
                'libros': libros_dict,
                'total': len(libros_dict),
                'genero': genero
            }, 200))
            
        except Exception as e:
            return jsonify(ResponseApi.error(f"Error al obtener libros por género: {str(e)}", 500))

    def obtenerLibrosPorAutor(self, autor: str):
        """Obtener libros por autor"""
        try:
            libros = self.app.obtenerLibrosPorAutor(autor)
            
            # Convertir a dict para JSON
            libros_dict = [libro.__dict__ for libro in libros]
            
            return jsonify(ResponseApi.exito({
                'libros': libros_dict,
                'total': len(libros_dict),
                'autor': autor
            }, 200))
            
        except Exception as e:
            return jsonify(ResponseApi.error(f"Error al obtener libros por autor: {str(e)}", 500))

    def obtenerEstadisticas(self):
        """Obtener estadísticas de libros"""
        try:
            estadisticas = self.app.obtenerEstadisticasLibros()
            return jsonify(ResponseApi.exito(estadisticas, 200))
        except Exception as e:
            return jsonify(ResponseApi.error(f"Error al obtener estadísticas: {str(e)}", 500))

    def obtenerMejorCalificados(self):
        """Obtener libros mejor calificados"""
        try:
            limite = int(request.args.get('limite', 10))
            libros = self.app.obtenerLibrosMejorCalificados(limite)
            
            # Convertir a dict para JSON
            libros_dict = [libro.__dict__ for libro in libros]
            
            return jsonify(ResponseApi.exito({
                'libros': libros_dict,
                'total': len(libros_dict),
                'limite': limite
            }, 200))
            
        except Exception as e:
            return jsonify(ResponseApi.error(f"Error al obtener libros mejor calificados: {str(e)}", 500))

    # --- Vistas web ---
    def lista_libros(self):
        """Renderiza la lista de libros en una plantilla web"""
        try:
            # Obtener todos los libros (puede extenderse con filtros por query)
            libros = self.app.obtenerLibros(None)
            libros_list = [libro.__dict__ for libro in libros]
            return render_template('books/list.html', libros=libros_list)
        except Exception as e:
            # Para la vista web, mostramos un mensaje flash y redirigimos al dashboard
            flash(f"Error al obtener libros: {str(e)}", 'danger')
            return redirect(url_for('auth.dashboard'))

    def crear_libro_web(self):
        """Maneja el formulario web para crear un libro (GET muestra formulario, POST lo procesa)"""
        try:
            # Soporta edición: si viene edit_id en query params, cargar libro y prellenar
            edit_id = request.args.get('edit_id') if request.method == 'GET' else request.form.get('edit_id')
            if request.method == 'GET':
                if edit_id:
                    libro = self.app.obtenerLibro(edit_id)
                    if libro:
                        data = libro.__dict__
                        return render_template('books/create.html', data=data)
                return render_template('books/create.html')

            # POST: procesar formulario
            form = request.form.to_dict()

            # Normalizar campos que deben ser enteros/booleanos/listas
            if 'paginas' in form and form['paginas'] != '':
                try:
                    form['paginas'] = int(form['paginas'])
                except ValueError:
                    # dejar como string para que la validación lo capture
                    pass
            if 'año_publicacion' in form and form['año_publicacion'] != '':
                try:
                    form['año_publicacion'] = int(form['año_publicacion'])
                except ValueError:
                    pass
            if 'disponible' in form:
                form['disponible'] = form['disponible'].lower() in ['true', '1', 'on', 'yes']
            # tags: aceptar coma-separado
            if 'tags' in form and isinstance(form['tags'], str):
                tags = [t.strip() for t in form['tags'].split(',') if t.strip()]
                form['tags'] = tags

            schema = LibroCreateSchema()
            try:
                validated_data = schema.load(form)
            except ValidationError as ve:
                # Mostrar errores en la plantilla
                errors = ve.messages
                flash(f"Errores de validación: {errors}", 'warning')
                # Renderizar el formulario con los datos ingresados y errores
                return render_template('books/create.html', data=form, errors=errors)

            # Si viene edit_id en el formulario, actualizar
            if edit_id:
                modified = self.app.actualizarLibro(edit_id, validated_data)
                if modified and modified > 0:
                    flash('Libro actualizado exitosamente', 'success')
                else:
                    flash('No se pudo actualizar el libro', 'warning')
                return redirect(url_for('libro.lista_libros_web'))

            # Crear libro usando la capa de aplicación
            libro_id = self.app.crearLibro(validated_data)
            flash('Libro creado exitosamente', 'success')
            return redirect(url_for('libro.lista_libros_web'))

        except Exception as e:
            flash(f"Error al crear libro: {str(e)}", 'danger')
            return render_template('books/create.html', data=request.form.to_dict())