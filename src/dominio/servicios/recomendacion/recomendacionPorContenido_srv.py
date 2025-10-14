from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from src.dominio.servicios.libro import obtenerLibro_srv
from src.dominio.puertos.recomendacion_prt import RecomendacionPuerto

class RecomendarPorContenido:
    def __init__(self, obtenerLibroServicio: obtenerLibro_srv.ObtenerLibroServicio,
                 repositorio: RecomendacionPuerto):
        self.obtenerLibroServicio = obtenerLibroServicio
        self.repoRecomendacion = repositorio
        self.stopWord = [
            'de', 'la', 'que', 'el', 'en', 'y', 'a', 'los', 'del', 'se', 'las', 'por', 'un', 'para', 'con', 'no', 'una',
            'su', 'al', 'lo', 'como', 'más', 'pero', 'sus', 'le', 'ya', 'o', 'este', 'sí', 'porque', 'esta', 'entre',
            'cuando', 'muy', 'sin', 'sobre', 'también', 'me', 'hasta', 'hay', 'donde', 'quien', 'desde', 'todo', 'nos',
            'durante', 'todos', 'uno', 'les', 'ni', 'contra', 'otros', 'ese', 'eso', 'ante', 'ellos', 'e', 'esto', 'mí',
            'antes', 'algunos', 'qué', 'unos', 'yo', 'otro', 'otras', 'otra', 'él', 'tanto', 'esa', 'estos', 'mucho', 'quienes', 'nada', 'muchos', 'cual', 'poco', 'ella', 'estar', 'estas', 'algunas', 'algo', 'nosotros', 'mi', 'mis', 'tú', 'te', 'ti', 'tu', 'tus', 'ellas', 'nosotras', 'vosotros', 'vosotras', 'os', 'mío', 'mía', 'míos', 'mías', 'tuyo', 'tuya'
        ]
    def recomendarPorContenido(self) -> bool:

        libros = self.obtenerLibroServicio.obtenerLibros()
        print(libros)
        ids = []
        textos = []
        for libro in libros:
            ids.append(libro._id)
            contenido = libro.titulo + ' ' + (libro.descripcion or '') + ' ' + ' '.join(libro.tags)
            textos.append(contenido)
        tfidf = TfidfVectorizer(stop_words=self.stopWord)
        tfidfMatrix = tfidf.fit_transform(textos)

        cosenoSim = cosine_similarity(tfidfMatrix, tfidfMatrix) 
        
        for idx, idLibro in enumerate(ids):
            similares = list(enumerate(cosenoSim[idx]))
            similares = sorted(similares, key=lambda x: x[1], reverse=True) 
            similares = [ids[i] for i, score in similares if ids[i] != idLibro]
            # Guardar lista directamente; el repositorio la serializará como JSON
            self.repoRecomendacion.guardarRecomendacionRedis(idLibro, similares[:10])
            print(f"Recomendaciones para el libro {idLibro}: {similares[:10]}")
        return True

    def agregarNuevaRecomendacion(self, idLibro: str) -> bool:
        libros = self.obtenerLibroServicio.obtenerLibros()
        ids = []
        textos = []
        for libro in libros:
            ids.append(libro._id)
            contenido = libro.titulo + ' ' + (libro.descripcion or '') + ' ' + ' '.join(libro.tags)
            textos.append(contenido)
        tfidf = TfidfVectorizer(stop_words=self.stopWord)
        tfidfMatrix = tfidf.fit_transform(textos)

        cosenoSim = cosine_similarity(tfidfMatrix, tfidfMatrix) 
        
        if idLibro in ids:
            idx = ids.index(idLibro)
            similares = list(enumerate(cosenoSim[idx]))
            similares = sorted(similares, key=lambda x: x[1], reverse=True) 
            similares = [ids[i] for i, score in similares if ids[i] != idLibro]
            # Guardar lista directamente; el repositorio la serializará como JSON
            self.repoRecomendacion.guardarRecomendacionRedis(idLibro, similares[:10])
            print(f"Recomendaciones para el libro {idLibro}: {similares[:10]}")
            return True
        else:
            print(f"El libro con ID {idLibro} no se encontró en la base de datos.")
            return False
        