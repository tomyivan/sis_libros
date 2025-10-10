class ResponseApi:
    @staticmethod
    def exito(message: str, data=None):
        return {
            "estado": True,
            "msg": message,
            "data": data
        }

    @staticmethod
    def error(message: str, data=None):
        return {
            "estado": False,
            "msg": message,
            "data": data
        }