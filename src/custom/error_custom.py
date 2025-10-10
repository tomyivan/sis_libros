# Manejo de errores personalizados

class APIError(Exception):

    def __init__(self, message, code=400):
        super().__init__(message)
        self.message = message
        self.code = code


class NotFoundError(APIError):
    def __init__(self, message="Recurso no encontrado"):
        super().__init__(message, code=404)


class UnauthorizedError(APIError):
    def __init__(self, message="No autorizado"):
        super().__init__(message, code=401)
