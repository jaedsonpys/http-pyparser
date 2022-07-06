from . import exceptions


class HTTPData(object):
    def __init__(self) -> None:
        self.path = None
        self.status = None
        self.version = None
        self.body = None
        self.headers = None
        self.cookies = None


class HTTPParser(object):
    def __init__(self) -> None:
        self.result = HTTPData()

    def parser(self, http_message: str) -> HTTPData:
        """Parser a HTTP request message.

        All headers will be analyzed and added
        to an instance of the `HTTPData` class,
        which will be returned when everything
        is finished.

        :param http_message: HTTP request message;
        :type http_message: str
        :raises exceptions.InvalidHTTPMessageError:
        Raises exception if message is invalid
        :return: HTTP message data
        :rtype: HTTPData
        """

        msg_parts = http_message.split('\r\n')

        try:
            info = msg_parts.pop(0)
            method, path, version = info.split(' ')
        except (ValueError, IndexError):
            raise exceptions.InvalidHTTPMessageError('Invalid HTTP message')

        self.result.method = method
        self.result.path = path
        self.result.version = version

        return self.result
