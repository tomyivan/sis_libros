from flask import Response, stream_with_context
import json

from src.app.publicacion_app import PublicacionApp
from src.helpers.redisconn_hlp import redCli


class PublicacionControlador:
    def __init__(self, app: PublicacionApp):
        self.app = app

    def obtenerPublicaciones(self):
        """Return a persistent SSE stream backed by Redis pubsub.

        This generator subscribes to the 'notificacion' channel and yields
        each message as a JSON-formatted SSE event. The connection remains
        open until the client closes it.
        """

        def event_stream():
            pubsub = redCli.pubsub()
            channel = 'notificacion'
            pubsub.subscribe(channel)
            try:
                for mensaje in pubsub.listen():
                    # only handle real message events
                    if mensaje.get('type') != 'message':
                        continue
                    data = mensaje.get('data')
                    # decode bytes if needed
                    if isinstance(data, (bytes, bytearray)):
                        try:
                            data = data.decode('utf-8')
                        except Exception:
                            data = str(data)
                    # ensure it's valid JSON string
                    try:
                        # if data already JSON string, load then dump to normalize
                        payload = json.loads(data)
                        payload_str = json.dumps(payload)
                    except Exception:
                        # fallback: convert to string and json-escape
                        payload_str = json.dumps(str(data))
                    yield f"data: {payload_str}\n\n"
            finally:
                try:
                    pubsub.close()
                except Exception:
                    pass

        response = Response(stream_with_context(event_stream()), mimetype='text/event-stream')
        response.headers['Cache-Control'] = 'no-cache'
        response.headers['X-Accel-Buffering'] = 'no'
        return response
