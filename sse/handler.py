import asyncio

from . import exceptions
from .protocol import Response

__all__ = ['Handler']


class Handler:
    def __init__(self, protocol, request, payload):
        self.transport = protocol.transport
        self.request = request
        self.payload = payload

    def prepare_response(self):
        response = Response(self.transport, 200)
        response.add_header('Content-Type', 'text/event-stream')
        response.add_header('Cache-Control', 'no-cache')
        response.add_header('Connection', 'keep-alive')
        response.send_headers()
        self.response = response

    def send(self, *args, **kwargs):
        return self.response.send(*args, **kwargs)

    def validate_sse(self):
        if self.request.method.upper() != 'GET':
            raise exceptions.MethodNotAllowed()

        for header, value in self.request.headers:
            if header.upper() == 'ACCEPT':
                options = value.split(';')
                for option in options:
                    accept = option.strip()
                    if accept in ['*', '*/*']:
                        return True
                    elif accept == 'text/event-stream':
                        return True
        raise exceptions.NotAcceptable()

    @asyncio.coroutine
    def handle_request(self):
        raise NotImplementedError
