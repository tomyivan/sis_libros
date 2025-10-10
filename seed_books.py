"""
Script para poblar la base de datos con libros de ejemplo
Ejecutar: python seed_books.py
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.helpers.mongoconn_hlp import MongoConnection
from src.infrastuctura.repositorio.libro_rep import LibroRepositorio
from src.dominio.modelos.libro_mod import LibroModelo
from datetime import datetime

def create_sample_books():
    try:
        # Conectar a la base de datos
        mongo_conn = MongoConnection()
        libro_repo = LibroRepositorio(mongo_conn)
        
        # Libros de ejemplo
        libros_ejemplo = [
            {
                "titulo": "Cien años de soledad",
                "autor": "Gabriel García Márquez",
                "genero": "Realismo mágico",
                "año_publicacion": 1967,
                "editorial": "Sudamericana",
                "isbn": "978-0-06-088328-7",
                "paginas": 417,
                "idioma": "Español",
                "descripcion": "La historia de la familia Buendía a lo largo de siete generaciones en el pueblo ficticio de Macondo.",
                "origen_pais": "Colombia",
                "tags": ["realismo mágico", "literatura latinoamericana", "clásico"]
            },
            {
                "titulo": "Don Quijote de la Mancha",
                "autor": "Miguel de Cervantes",
                "genero": "Novela",
                "año_publicacion": 1605,
                "editorial": "Juan de la Cuesta",
                "isbn": "978-0-14-243723-0",
                "paginas": 863,
                "idioma": "Español",
                "descripcion": "Las aventuras del ingenioso hidalgo Don Quijote de La Mancha y su escudero Sancho Panza.",
                "origen_pais": "España",
                "tags": ["clásico", "aventura", "literatura española"]
            },
            {
                "titulo": "1984",
                "autor": "George Orwell",
                "genero": "Distopía",
                "año_publicacion": 1949,
                "editorial": "Secker & Warburg",
                "isbn": "978-0-452-28423-4",
                "paginas": 328,
                "idioma": "Inglés",
                "descripcion": "Una distopía que describe un futuro totalitario donde el Gran Hermano todo lo ve.",
                "origen_pais": "Reino Unido",
                "tags": ["distopía", "ciencia ficción", "político"]
            },
            {
                "titulo": "El Principito",
                "autor": "Antoine de Saint-Exupéry",
                "genero": "Fábula",
                "año_publicacion": 1943,
                "editorial": "Reynal & Hitchcock",
                "isbn": "978-0-15-601219-9",
                "paginas": 96,
                "idioma": "Francés",
                "descripcion": "La historia de un pequeño príncipe que viaja por diferentes planetas.",
                "origen_pais": "Francia",
                "tags": ["infantil", "filosofía", "fábula"]
            },
            {
                "titulo": "Rayuela",
                "autor": "Julio Cortázar",
                "genero": "Literatura experimental",
                "año_publicacion": 1963,
                "editorial": "Sudamericana",
                "isbn": "978-0-394-75284-0",
                "paginas": 635,
                "idioma": "Español",
                "descripcion": "Una novela experimental que puede leerse de múltiples maneras.",
                "origen_pais": "Argentina",
                "tags": ["experimental", "literatura latinoamericana", "vanguardia"]
            },
            {
                "titulo": "La casa de los espíritus",
                "autor": "Isabel Allende",
                "genero": "Realismo mágico",
                "año_publicacion": 1982,
                "editorial": "Sudamericana",
                "isbn": "978-0-553-38370-8",
                "paginas": 448,
                "idioma": "Español",
                "descripcion": "La saga de la familia del Toro-Trueba a través de cuatro generaciones.",
                "origen_pais": "Chile",
                "tags": ["realismo mágico", "literatura latinoamericana", "saga familiar"]
            },
            {
                "titulo": "Harry Potter y la piedra filosofal",
                "autor": "J.K. Rowling",
                "genero": "Fantasía",
                "año_publicacion": 1997,
                "editorial": "Bloomsbury",
                "isbn": "978-0-7475-3269-9",
                "paginas": 223,
                "idioma": "Inglés",
                "descripcion": "Un niño huérfano descubre que es un mago y asiste a Hogwarts.",
                "origen_pais": "Reino Unido",
                "tags": ["fantasía", "juvenil", "magia", "aventura"]
            },
            {
                "titulo": "El amor en los tiempos del cólera",
                "autor": "Gabriel García Márquez",
                "genero": "Romance",
                "año_publicacion": 1985,
                "editorial": "Sudamericana",
                "isbn": "978-0-307-38973-7",
                "paginas": 368,
                "idioma": "Español",
                "descripcion": "Una historia de amor que trasciende el tiempo y las circunstancias.",
                "origen_pais": "Colombia",
                "tags": ["romance", "realismo mágico", "literatura latinoamericana"]
            },
            {
                "titulo": "Crónica de una muerte anunciada",
                "autor": "Gabriel García Márquez",
                "genero": "Novela corta",
                "año_publicacion": 1981,
                "editorial": "Sudamericana",
                "isbn": "978-1-4000-3471-0",
                "paginas": 122,
                "idioma": "Español",
                "descripcion": "La reconstrucción de un crimen de honor anunciado desde el principio.",
                "origen_pais": "Colombia",
                "tags": ["novela corta", "crimen", "realismo mágico"]
            },
            {
                "titulo": "Ficciones",
                "autor": "Jorge Luis Borges",
                "genero": "Cuentos",
                "año_publicacion": 1944,
                "editorial": "Sur",
                "isbn": "978-0-8021-1564-9",
                "paginas": 174,
                "idioma": "Español",
                "descripcion": "Colección de cuentos que exploran temas como el infinito, los laberintos y la realidad.",
                "origen_pais": "Argentina",
                "tags": ["cuentos", "filosofía", "literatura argentina", "laberintos"]
            }
        ]
        
        libros_creados = 0
        libros_existentes = 0
        
        for libro_data in libros_ejemplo:
            try:
                # Verificar si ya existe por ISBN
                if not libro_repo._isbn_existe(libro_data["isbn"]):
                    libro = LibroModelo(
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
                        disponible=True,
                        fecha_creacion=datetime.now(),
                        calificacion_promedio=round(__import__('random').uniform(3.5, 5.0), 1),
                        numero_calificaciones=__import__('random').randint(10, 100),
                        tags=libro_data.get("tags", [])
                    )
                    
                    result = libro_repo.crearLibro(libro)
                    if result:
                        print(f"✅ Libro creado: {libro_data['titulo']}")
                        libros_creados += 1
                    else:
                        print(f"❌ Error al crear: {libro_data['titulo']}")
                else:
                    print(f"ℹ️  Ya existe: {libro_data['titulo']}")
                    libros_existentes += 1
                    
            except Exception as e:
                print(f"❌ Error con {libro_data['titulo']}: {str(e)}")
        
        print(f"\n📊 Resumen:")
        print(f"   Libros creados: {libros_creados}")
        print(f"   Libros existentes: {libros_existentes}")
        print(f"   Total procesados: {len(libros_ejemplo)}")
        
        if libros_creados > 0:
            print(f"\n🎉 ¡Base de datos poblada exitosamente!")
        else:
            print(f"\n📚 La base de datos ya tenía todos los libros")
            
    except Exception as e:
        print(f"❌ Error general: {str(e)}")

if __name__ == "__main__":
    print("📚 Poblando la base de datos con libros de ejemplo...")
    create_sample_books()