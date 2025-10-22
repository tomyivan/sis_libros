from src.infrastuctura.repositorio.interaccion_rep import InteraccionRepositorio
from src.dominio.servicios.interaccion.interaccion_srv import InteraccionServicio
from src.app.interaccion_app import InteraccionApp


# Wiring de dependencias para Interacciones (Redis-only)
interaccion_repositorio = InteraccionRepositorio()
interaccion_servicio = InteraccionServicio(interaccion_repositorio)
interaccion_app = InteraccionApp(interaccion_servicio)
