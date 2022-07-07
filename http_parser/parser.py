from . import exceptions


class HTTPData(object):
    def __init__(self) -> None:
        self.path = None
        self.status = None
        self.version = None
        
        self.host = None
        self.user_agent = None
        self.accept = None

        self.body = None
        self.headers = None
        self.cookies = None


class HTTPParser(object):
    def __init__(self) -> None:
        self.result = HTTPData()

    def _parser_cookies(self, cookies: str) -> dict:
        parsed_cookies = {}
        cookie_split = cookies.split(';')

        for cookie in cookie_split:
            cookie = cookie.strip()
            key, value = cookie.split('=')
            parsed_cookies[key] = value

        return parsed_cookies

    def _parser_headers(self, headers: str) -> dict:
        parsed_headers = {}

        for header in headers:
            if header:
                name, value = header.split(':', maxsplit=1)
                value = value.strip()

                if ';' in value and ',' in value:
                    sub_values = value.split(',')
                    filtered_values = []

                    for sv in sub_values:
                        sv = sv.strip()
                        filtered_values.append(sv)

                    parsed_headers[name] = filtered_values
                else:
                    if name == 'Cookie':
                        self.result.cookies = self._parser_cookies(value)
                    else:
                        parsed_headers[name] = value

        return parsed_headers

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

        headers = self._parser_headers(msg_parts)
        
        self.result.host = headers.get('Host')
        self.result.user_agent = headers.get('User-Agent')
        self.result.accept = headers.get('Accept')

        return self.result
