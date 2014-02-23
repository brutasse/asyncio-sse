import asyncio

from .protocol import SseServerProtocol

__all__ = ['serve']


@asyncio.coroutine
def serve(sse_handler, host=None, port=None, *, klass=SseServerProtocol,
          **kwargs):
    return (yield from asyncio.get_event_loop().create_server(
        lambda: klass(sse_handler), host, port, **kwargs))
