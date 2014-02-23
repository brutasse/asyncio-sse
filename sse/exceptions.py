__all__ = ['SseException', 'MethodNotAllowed', 'NotAcceptable']


class SseException(Exception):
    status = 404
    headers = None


class MethodNotAllowed(SseException):
    status = 405
    headers = (
        ('Allow', 'GET'),
    )


class NotAcceptable(SseException):
    status = 406
