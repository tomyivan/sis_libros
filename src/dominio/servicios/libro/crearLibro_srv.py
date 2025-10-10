from src.dominio.modelos import libro_mod
from src.dominio.puertos import libro_prt
from datetime import datetime

class CrearLibroServicio:
    def __init__(self, repositorio: libro_prt.LibroPuerto):
        self.repositorio = repositorio

    def crearLibro(self, libro_data: dict) -> str:
        """Crear un nuevo libro con validaciones de negocio"""
        # Validaciones de negocio
        self._validarDatosLibro(libro_data)
        
        print(libro_data)
        # Crear el modelo del libro
        libro = libro_mod.LibroModelo(
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
            fecha_creacion=datetime.now(),
            calificacion_promedio=0.0,
            numero_calificaciones=0,
            portada_url=libro_data.get("portada_url"),
            tags=libro_data.get("tags", [])
        )

        return self.repositorio.crearLibro(libro)

    def _validarDatosLibro(self, libro_data: dict):
        """Validaciones de negocio específicas"""
        
        # Validar año de publicación
        año_actual = datetime.now().year
        if libro_data["año_publicacion"] > año_actual:
            raise ValueError("El año de publicación no puede ser mayor al año actual")
        
        if libro_data["año_publicacion"] < 1000:
            raise ValueError("El año de publicación debe ser mayor a 1000")
        
        # Validar páginas
        if libro_data["paginas"] <= 0:
            raise ValueError("El número de páginas debe ser mayor a 0")
        
        # Validar ISBN (formato básico)
        isbn = libro_data["isbn"].replace("-", "").replace(" ", "")
        if not (len(isbn) == 10 or len(isbn) == 13):
            raise ValueError("El ISBN debe tener 10 o 13 dígitos")
        
        # Validar que los campos de texto no estén vacíos
        campos_requeridos = ["titulo", "autor", "genero", "editorial", "idioma", "descripcion", "origen_pais"]
        for campo in campos_requeridos:
            if not libro_data.get(campo) or libro_data[campo].strip() == "":
                raise ValueError(f"El campo {campo} es requerido y no puede estar vacío")