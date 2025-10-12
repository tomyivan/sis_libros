class ResponseApi:
    @staticmethod
    def exito(msg: str, data=None):
        """Return a success response object.

        Backwards-compatible: many controllers pass a dict as the first
        argument (the payload) and an HTTP code as the second. To be
        tolerant we detect if the first arg is a dict/list and set it as
        `data` while leaving `msg` empty. Otherwise keep original
        behavior where the first arg is a human message and the second
        is the payload.
        """
        if isinstance(msg, (dict, list)):
            return {
                "estado": True,
                "msg": msg,
                "data": data
            }
        return {
            "estado": True,
            "msg": msg,
            "data": data
        }

    @staticmethod
    def error(msg: str, data=None):
        """Return an error response object. Mirrors exito's flexibility."""
        if isinstance(msg, (dict, list)):
            return {
                "estado": False,
                "msg": "",
                "data": msg
            }
        return {
            "estado": False,
            "msg": msg,
            "data": data
        }