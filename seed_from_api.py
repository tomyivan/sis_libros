"""
Seeder para poblar la colección `libros` usando la Open Library API (con opción genérica para otras APIs).

Este script soporta dos modos principales para Open Library:
 - search: usa https://openlibrary.org/search.json?q=...&page=...
 - subject: usa https://openlibrary.org/subjects/{subject}.json?limit=...&offset=...

También puede usarse con cualquier API genérica pasando --url y --items-key.

Ejemplo (Open Library search, modo de prueba):
  python seed_from_api.py --openlibrary --q "python" --per-page 50 --sample-only

Ejemplo (subject):
  python seed_from_api.py --openlibrary --subject "science_fiction" --per-page 100 --sample-only

Requiere tener la variable de entorno MONGO_URI apuntando a la base de datos.
"""

import argparse
import time
import sys
import os
import json
from urllib.parse import urljoin

# Añadir repo al path (mismo patrón que seed_books.py)
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from src.helpers.mongoconn_hlp import MongoConnection
from src.infrastuctura.repositorio.libro_rep import LibroRepositorio
from src.dominio.modelos.libro_mod import LibroModelo
from datetime import datetime


DEFAULT_ITEMS_KEYS = ['results', 'items', 'data', 'docs', 'works']


def requests_session_with_retries(total_retries=5, backoff_factor=0.5, status_forcelist=(500, 502, 503, 504)):
    session = requests.Session()
    retries = Retry(total=total_retries, backoff_factor=backoff_factor, status_forcelist=status_forcelist)
    adapter = HTTPAdapter(max_retries=retries)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


def extract_value(item, possible_keys):
    """Extrae el primer valor disponible de una lista de posibles claves. Soporta dot-notation."""
    for k in possible_keys:
        if isinstance(k, str) and '.' in k:
            parts = k.split('.')
            val = item
            ok = True
            for p in parts:
                if isinstance(val, dict) and p in val:
                    val = val[p]
                else:
                    ok = False
                    break
            if ok and val is not None:
                return val
        else:
            if isinstance(item, dict) and k in item and item[k] is not None:
                return item[k]
    return None


def default_map_item_openlibrary_doc(doc):
    """Mapea un documento/obra de OpenLibrary a los campos del libro.

    doc puede ser un item de search.json (docs) o un elemento de works (subjects).
    """
    titulo = doc.get('title') or doc.get('work_title') or 'Sin título'
    authors = doc.get('author_name') or []
    if isinstance(authors, list):
        autor = ', '.join(authors)
    else:
        autor = authors or 'Desconocido'

    genero = ''
    tags = doc.get('subject') or doc.get('subjects') or []
    if isinstance(tags, str):
        tags = [t.strip() for t in tags.split(',') if t.strip()]

    anio = doc.get('first_publish_year') or 0
    try:
        anio = int(anio) if anio else 0
    except Exception:
        anio = 0

    editorial = None
    if 'publisher' in doc and isinstance(doc['publisher'], list) and doc['publisher']:
        editorial = doc['publisher'][0]
    elif 'publishers' in doc and isinstance(doc['publishers'], list) and doc['publishers']:
        editorial = doc['publishers'][0]

    isbn = None
    if 'isbn' in doc and isinstance(doc['isbn'], list) and doc['isbn']:
        isbn = doc['isbn'][0]
    elif 'isbn_10' in doc and isinstance(doc['isbn_10'], list) and doc['isbn_10']:
        isbn = doc['isbn_10'][0]
    elif 'isbn_13' in doc and isinstance(doc['isbn_13'], list) and doc['isbn_13']:
        isbn = doc['isbn_13'][0]

    paginas = doc.get('number_of_pages_median') or doc.get('number_of_pages') or 0
    try:
        paginas = int(paginas) if paginas else 0
    except Exception:
        paginas = 0

    idioma = None
    if 'language' in doc and isinstance(doc['language'], list) and doc['language']:
        # language entries can be like {'key':'/languages/eng'} or 'eng'
        first = doc['language'][0]
        if isinstance(first, dict) and 'key' in first:
            idioma = first['key'].split('/')[-1]
        else:
            idioma = first

    descripcion = ''
    if 'first_sentence' in doc:
        fs = doc['first_sentence']
        if isinstance(fs, dict) and 'value' in fs:
            descripcion = fs['value']
        elif isinstance(fs, str):
            descripcion = fs
    if not descripcion and 'subtitle' in doc:
        descripcion = doc.get('subtitle') or ''

    if not isbn:
        isbn = f"seed-ol-{int(time.time()*1000)}-{abs(hash(titulo)) & 0xffff}"

    mapped = {
        'titulo': titulo,
        'autor': autor,
        'genero': genero or '',
        'año_publicacion': anio,
        'editorial': editorial or '',
        'isbn': isbn,
        'paginas': paginas or 0,
        'idioma': idioma or '',
        'descripcion': descripcion or '',
        'origen_pais': '',
        'tags': tags or [],
        'disponible': True,
        'fecha_creacion': datetime.now(),
        'calificacion_promedio': 0.0,
        'numero_calificaciones': 0
    }
    return mapped


def parse_map_arg(map_arg):
    mapping = {}
    if not map_arg:
        return mapping
    pairs = map_arg.split(',')
    for p in pairs:
        if '=' in p:
            k, v = p.split('=', 1)
            mapping[k.strip()] = v.strip()
    return mapping


def apply_custom_map(item, mapping):
    mapped = {}
    for dst, src in mapping.items():
        mapped[dst] = extract_value(item, [src])
    return mapped


def ensure_non_empty(mapped):
    """Rellena valores por defecto cuando un campo está vacío o nulo para evitar campos vacíos en BD."""
    now = datetime.now()
    # Título y autor
    if not mapped.get('titulo'):
        mapped['titulo'] = 'Sin título'
    if not mapped.get('autor'):
        mapped['autor'] = 'Desconocido'

    # Genero/editorial
    if not mapped.get('genero'):
        mapped['genero'] = 'General'
    if not mapped.get('editorial'):
        mapped['editorial'] = 'Desconocido'

    # Año
    try:
        año = int(mapped.get('año_publicacion') or mapped.get('anio') or 0)
    except Exception:
        año = 0
    if año <= 0:
        año = now.year
    mapped['año_publicacion'] = año

    # ISBN
    if not mapped.get('isbn'):
        mapped['isbn'] = f"seed-ol-{int(time.time()*1000)}-{abs(hash(mapped.get('titulo'))) & 0xffff}"

    # Paginas
    try:
        paginas = int(mapped.get('paginas') or 0)
    except Exception:
        paginas = 0
    if paginas <= 0:
        paginas = 100
    mapped['paginas'] = paginas

    # Idioma
    if not mapped.get('idioma'):
        mapped['idioma'] = 'und'

    # Descripción y origen país
    if not mapped.get('descripcion'):
        mapped['descripcion'] = 'Sin descripción'
    if not mapped.get('origen_pais'):
        mapped['origen_pais'] = 'Unknown'

    # Tags (si no hay tags, añadir uno de seed)
    tags = mapped.get('tags')
    if not tags:
        mapped['tags'] = ['seeded']
    else:
        # asegurar lista y no vacía
        if isinstance(tags, str):
            mapped['tags'] = [t.strip() for t in tags.split(',') if t.strip()] or ['seeded']
        elif isinstance(tags, list) and len(tags) == 0:
            mapped['tags'] = ['seeded']

    # Fecha creación/modificacion
    if not mapped.get('fecha_creacion'):
        mapped['fecha_creacion'] = now
    mapped['fecha_modificacion'] = mapped.get('fecha_modificacion') or now

    # Portada (usar cover API si hay isbn)
    if not mapped.get('portada_url'):
        isbn = mapped.get('isbn')
        if isbn:
            mapped['portada_url'] = f"https://covers.openlibrary.org/b/isbn/{isbn}-L.jpg"
        else:
            mapped['portada_url'] = 'https://via.placeholder.com/150x200?text=No+Cover'

    # Disponibilidad y calificaciones
    mapped['disponible'] = bool(mapped.get('disponible', True))
    mapped['calificacion_promedio'] = float(mapped.get('calificacion_promedio') or 0.0)
    mapped['numero_calificaciones'] = int(mapped.get('numero_calificaciones') or 0)

    return mapped


def main():
    parser = argparse.ArgumentParser(description='Seeder desde Open Library hacia MongoDB (colección libros)')
    parser.add_argument('--url', required=False, help='URL base de la API genérica (opcional)')
    parser.add_argument('--openlibrary', action='store_true', help='Usar Open Library API (search o subject)')
    parser.add_argument('--subject', default=None, help='Si se usa Open Library, usar subject endpoint: /subjects/{subject}.json')
    parser.add_argument('--q', default='the', help='Query para search.json (Open Library)')
    parser.add_argument('--items-key', default=None, help='Clave en JSON donde están los items (results/items/data/docs/works)')
    parser.add_argument('--page-param', default='page', help='Nombre del parámetro de página (search)')
    parser.add_argument('--per-page-param', default='limit', help='Nombre del parámetro de tamaño por página (limit)')
    parser.add_argument('--start-page', type=int, default=1, help='Página inicial')
    parser.add_argument('--per-page', type=int, default=100, help='Items por página')
    parser.add_argument('--max-records', type=int, default=0, help='Máximo total a insertar (0 = ilimitado)')
    parser.add_argument('--delay', type=float, default=0.1, help='Delay entre peticiones en segundos')
    parser.add_argument('--map', default=None, help='Mapeo simple: "titulo=title,autor=authors"')
    parser.add_argument('--sample-only', action='store_true', help='No insertar en DB, solo muestre ejemplo y conteo')
    args = parser.parse_args()

    custom_mapping = parse_map_arg(args.map)

    session = requests_session_with_retries()

    # Si estamos en modo sample-only no forzamos la conexión a MongoDB ni la importación
    libro_repo = None
    if not args.sample_only:
        mongo_conn = MongoConnection()
        libro_repo = LibroRepositorio(mongo_conn)

    # Para evitar recorrer miles de páginas en pruebas, si estamos en sample-only
    # y no se pasó --max-records, aplicamos un tope sensible (per-page * 5)
    if args.sample_only and args.max_records == 0:
        suggested = max(10, args.per_page * 5)
        print(f"--sample-only activado: limitando prueba a {suggested} registros (use --max-records para cambiar)")
        args.max_records = suggested

    page = args.start_page
    total_processed = 0
    total_inserted = 0
    total_skipped = 0

    try:
        while True:
            # Construir la petición según modo
            if args.openlibrary:
                if args.subject:
                    # Subject endpoint usa offset
                    offset = (page - 1) * args.per_page
                    url = f"https://openlibrary.org/subjects/{args.subject}.json"
                    params = {'limit': args.per_page, 'offset': offset}
                    print(f"Fetching subject {args.subject} offset={offset} limit={args.per_page} (page {page})...")
                else:
                    url = 'https://openlibrary.org/search.json'
                    params = {'q': args.q, 'page': page, 'limit': args.per_page}
                    print(f"Searching Open Library q={args.q} page={page} limit={args.per_page}...")

                resp = session.get(url, params=params, timeout=30)
                if resp.status_code != 200:
                    print(f"HTTP {resp.status_code} fetching {resp.url}: {resp.text[:200]}")
                    if 400 <= resp.status_code < 500:
                        break
                    else:
                        time.sleep(args.delay)
                        continue

                data = resp.json()

                # Obtener lista de documentos
                items = None
                if args.subject:
                    items = data.get('works')
                else:
                    items = data.get('docs') or data.get('works')

            else:
                # modo genérico
                if not args.url:
                    print('Modo genérico requiere --url si no usa --openlibrary')
                    return
                params = {args.page_param: page, args.per_page_param: args.per_page}
                print(f"Fetching page {page} (params={params}) from {args.url}...")
                resp = session.get(args.url, params=params, timeout=30)
                if resp.status_code != 200:
                    print(f"HTTP {resp.status_code} fetching {resp.url}: {resp.text[:200]}")
                    if 400 <= resp.status_code < 500:
                        break
                    else:
                        time.sleep(args.delay)
                        continue
                data = resp.json()

                items = None
                if args.items_key and isinstance(data, dict):
                    items = data.get(args.items_key)
                if items is None:
                    for k in DEFAULT_ITEMS_KEYS:
                        if isinstance(data, dict) and k in data:
                            items = data[k]
                            break
                    if items is None and isinstance(data, list):
                        items = data

            if items is None:
                print('No se encontraron items en la respuesta (revisa --items-key o parámetros).')
                break

            if not items:
                print('No hay items en la página, finalizando.')
                break

            for item in items:
                if args.max_records and total_processed >= args.max_records:
                    break
                total_processed += 1

                # Mapear
                if custom_mapping:
                    mapped = apply_custom_map(item, custom_mapping)
                else:
                    if args.openlibrary:
                        mapped = default_map_item_openlibrary_doc(item)
                    else:
                        # heurístico genérico
                        mapped = {
                            'titulo': extract_value(item, ['title', 'name']) or 'Sin título',
                            'autor': extract_value(item, ['author', 'author_name', 'authors']) or 'Desconocido',
                            'genero': extract_value(item, ['genre', 'category']) or '',
                            'año_publicacion': extract_value(item, ['first_publish_year', 'year', 'published_year']) or 0,
                            'editorial': extract_value(item, ['publisher', 'publishers']) or '',
                            'isbn': extract_value(item, ['isbn', 'isbn_13', 'identificador']) or f"seed-{int(time.time()*1000)}-{abs(hash(str(item))) & 0xffff}",
                            'paginas': extract_value(item, ['number_of_pages_median', 'pages', 'page_count']) or 0,
                            'idioma': extract_value(item, ['language', 'idioma']) or '',
                            'descripcion': extract_value(item, ['first_sentence', 'description', 'summary']) or '',
                            'origen_pais': extract_value(item, ['country', 'origin_country']) or '',
                            'tags': extract_value(item, ['subject', 'subjects', 'tags']) or [],
                            'disponible': True,
                            'fecha_creacion': datetime.now(),
                            'calificacion_promedio': 0.0,
                            'numero_calificaciones': 0
                        }

                # Asegurar campos no vacíos
                mapped = ensure_non_empty(mapped)

                libro = LibroModelo(
                    titulo=mapped.get('titulo'),
                    autor=mapped.get('autor'),
                    genero=mapped.get('genero'),
                    año_publicacion=mapped.get('año_publicacion'),
                    editorial=mapped.get('editorial') or '',
                    isbn=mapped.get('isbn'),
                    paginas=mapped.get('paginas') or 0,
                    idioma=mapped.get('idioma') or '',
                    descripcion=mapped.get('descripcion') or '',
                    origen_pais=mapped.get('origen_pais') or '',
                    disponible=mapped.get('disponible', True),
                    fecha_creacion=mapped.get('fecha_creacion', datetime.now()),
                    fecha_modificacion=mapped.get('fecha_modificacion'),
                    calificacion_promedio=mapped.get('calificacion_promedio', 0.0),
                    numero_calificaciones=mapped.get('numero_calificaciones', 0),
                    portada_url=mapped.get('portada_url'),
                    tags=mapped.get('tags', [])
                )

                if args.sample_only:
                    if total_inserted < 5:
                        print('Ejemplo mapeado:', json.dumps(libro.__dict__, default=str, ensure_ascii=False, indent=2))
                    total_inserted += 1
                    continue

                try:
                    libro_id = libro_repo.crearLibro(libro)
                    if libro_id:
                        total_inserted += 1
                        if total_inserted % 100 == 0:
                            print(f"Inserted {total_inserted} items so far...")
                except Exception as e:
                    total_skipped += 1
                    print(f"Skip/err on item {total_processed}: {str(e)}")

                if args.max_records and total_processed >= args.max_records:
                    break

            if args.max_records and total_processed >= args.max_records:
                print('Alcanzado max_records, finalizando.')
                break

            page += 1
            time.sleep(args.delay)

        print('\nResumen:')
        print(f'  Procesados: {total_processed}')
        print(f'  Insertados: {total_inserted}')
        print(f'  Saltados/Errores: {total_skipped}')

    except KeyboardInterrupt:
        print('Interrumpido por usuario')
    except Exception as e:
        print('Error general en el seeder:', str(e))


if __name__ == '__main__':
    main()
