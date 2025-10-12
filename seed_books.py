"""
Script para poblar la base de datos con libros de ejemplo
Ejecutar: python seed_books.py
"""
import requests
import json
def cargarLibroDeJson(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def conectarApi(url, libro):
    response = requests.post(url, json=libro)
    print(response.json())

def cargarLibros(libros):
    # Aquí iría la lógica para guardar los libros en la base de datos
    for libro in libros:
        print(f"Cargando libro: {libro['titulo']}")
        conectarApi('http://localhost:5000/libro/crear', libro)

print("Cargando libros de ejemplo...")
libros = cargarLibroDeJson('libros.json')
cargarLibros(libros)
# def obtenerLibrosDesdeApi(url):
#     response = requests.get(url)
#     if response.status_code == 200:
#         return response.json()
#     return []

