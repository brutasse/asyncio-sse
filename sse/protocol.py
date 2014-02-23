import aiohttp.server
import asyncio
import json

from . import exceptions

__all__ = ['SseServerProtocol', 'Response']


class Response(aiohttp.Response):
    def send(self, data, id=None, retry=None, event=None):
        assert data
        if retry is not None:
            self.write('retry: {0}\n'.format(retry).encode('utf-8'))
        if id is not None:
            self.write('id: {0}\n'.format(id).encode('utf-8'))
        if event is not None:
            self.write('event: {0}\n'.format(event).encode('utf-8'))
        if not isinstance(data, str):
            data = json.dumps(data)
        for chunk in data.split('\n'):
            self.write('data: {0}\n'.format(chunk).encode('utf-8'))
        self.write(b'\n')


class SseServerProtocol(aiohttp.server.ServerHttpProtocol):
    def __init__(self, sse_handler=None, **kwargs):
        self.handler_class = sse_handler
        super().__init__(**kwargs)

    @asyncio.coroutine
    def handle_request(self, request, payload):
        handler = self.handler_class(self, request, payload)
        try:
            handler.validate_sse()
        except exceptions.SseException as e:
            response = Response(self.transport, e.status)
            if e.headers:
                for header in e.headers:
                    response.add_header(*header)
            response.send_headers()
            response.write_eof()
            return

        handler.prepare_response()
        yield from handler.handle_request()
        handler.response.write_eof()
