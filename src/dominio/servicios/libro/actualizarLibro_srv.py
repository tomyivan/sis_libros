from src.dominio.modelos import libro_mod
from src.dominio.puertos import libro_prt
from datetime import datetime

class ActualizarLibroServicio:
    def __init__(self, repositorio: libro_prt.LibroPuerto):
        self.repositorio = repositorio

    def actualizarLibro(self, libro_id: str, libro_data: dict) -> int:
        """Actualizar un libro existente"""
        
        # Verificar que el libro existe
        libro_existente = self.repositorio.obtenerLibro(
            libro_mod.FiltroLibroModelo(_id=libro_id)
        )
        if not libro_existente:
            raise ValueError("El libro no existe")
        
        # Validaciones de negocio
        self._validarDatosActualizacion(libro_data)
        
        # Crear el modelo actualizado
        libro_actualizado = libro_mod.LibroModelo(
            titulo=libro_data["titulo"],
            autor=libro_data["autor"],
            genero=libro_data["genero"],
            año_publicacion=libro_data["año_publicacion"],
            editorial=libro_data["editorial"],
            isbn=libro_data["isbn"],
            paginas=libro_data["paginas"],
            idioma=libro_data["idioma"],
            descripcion=libro_data["descripcion"],
            origen_pais=libro_data["origen_pais"],
            disponible=libro_data.get("disponible", True),
            fecha_creacion=libro_existente.fecha_creacion,  # Mantener fecha original
            fecha_modificacion=datetime.now(),
            calificacion_promedio=libro_existente.calificacion_promedio,  # Mantener calificación
            numero_calificaciones=libro_existente.numero_calificaciones,
            portada_url=libro_data.get("portada_url", libro_existente.portada_url),
            tags=libro_data.get("tags", libro_existente.tags or [])
        )
        
        return self.repositorio.actualizarLibro(libro_actualizado, libro_id)

    def actualizarCalificacion(self, libro_id: str, nueva_calificacion: float) -> int:
        """Actualizar la calificación de un libro"""
        
        # Verificar que el libro existe
        libro_existente = self.repositorio.obtenerLibro(
            libro_mod.FiltroLibroModelo(_id=libro_id)
        )
        if not libro_existente:
            raise ValueError("El libro no existe")
        
        # Validar calificación
        if not (1.0 <= nueva_calificacion <= 5.0):
            raise ValueError("La calificación debe estar entre 1.0 y 5.0")
        
        # Calcular nueva calificación promedio
        total_actual = libro_existente.calificacion_promedio * libro_existente.numero_calificaciones
        nuevo_total = total_actual + nueva_calificacion
        nuevo_numero_calificaciones = libro_existente.numero_calificaciones + 1
        nueva_calificacion_promedio = nuevo_total / nuevo_numero_calificaciones
        
        # Crear libro actualizado solo con calificación
        libro_actualizado = libro_mod.LibroModelo(
            titulo=libro_existente.titulo,
            autor=libro_existente.autor,
            genero=libro_existente.genero,
            año_publicacion=libro_existente.año_publicacion,
            editorial=libro_existente.editorial,
            isbn=libro_existente.isbn,
            paginas=libro_existente.paginas,
            idioma=libro_existente.idioma,
            descripcion=libro_existente.descripcion,
            origen_pais=libro_existente.origen_pais,
            disponible=libro_existente.disponible,
            fecha_creacion=libro_existente.fecha_creacion,
            fecha_modificacion=datetime.now(),
            calificacion_promedio=round(nueva_calificacion_promedio, 2),
            numero_calificaciones=nuevo_numero_calificaciones,
            portada_url=libro_existente.portada_url,
            tags=libro_existente.tags
        )
        
        return self.repositorio.actualizarLibro(libro_actualizado, libro_id)

    def _validarDatosActualizacion(self, libro_data: dict):
        """Validaciones específicas para actualización"""
        
        # Reutilizar validaciones de creación
        año_actual = datetime.now().year
        if libro_data["año_publicacion"] > año_actual:
            raise ValueError("El año de publicación no puede ser mayor al año actual")
        
        if libro_data["año_publicacion"] < 1000:
            raise ValueError("El año de publicación debe ser mayor a 1000")
        
        if libro_data["paginas"] <= 0:
            raise ValueError("El número de páginas debe ser mayor a 0")
        
        isbn = libro_data["isbn"].replace("-", "").replace(" ", "")
        if not (len(isbn) == 10 or len(isbn) == 13):
            raise ValueError("El ISBN debe tener 10 o 13 dígitos")
        
        campos_requeridos = ["titulo", "autor", "genero", "editorial", "idioma", "descripcion", "origen_pais"]
        for campo in campos_requeridos:
            if not libro_data.get(campo) or libro_data[campo].strip() == "":
                raise ValueError(f"El campo {campo} es requerido y no puede estar vacío")