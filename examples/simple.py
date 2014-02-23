import asyncio
import logging.config
import sse

logger = logging.getLogger(__name__)

logging.basicConfig(level='INFO', format='%(message)s')


class WaitHandler(sse.Handler):
    @asyncio.coroutine
    def handle_request(self):
        yield from asyncio.sleep(2)
        self.send('foo')
        yield from asyncio.sleep(2)
        self.send("bar", event='wakeup')


if __name__ == '__main__':
    host, port = 'localhost', 8888
    loop = asyncio.get_event_loop()
    start_server = sse.serve(WaitHandler, host, port)
    loop.run_until_complete(start_server)
    logger.info("Server listening on {0}:{1}".format(host, port))
    loop.run_forever()
