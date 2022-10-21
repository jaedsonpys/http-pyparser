from . import exceptions


class HTTPData(object):
    def __init__(self) -> None:
        self.real_path = None

        self.path = None
        self.method = None
        self.version = None
        
        self.host = None
        self.user_agent = None
        self.accept = None

        self.body = None
        self.headers = None
        self.cookies = None
        self.query = None

    def __repr__(self) -> str:
        return (f'HTTPData(real_path="{self.real_path}", path="{self.path}", method="{self.method}", '
                f'version="{self.version}", host="{self.host}", user_agent="{self.user_agent}", '
                f'accept="{self.accept}", body={self.body}, headers={self.headers}, '
                f'cookies={self.cookies}, query={self.query})')


class HTTPParser(object):
    def __init__(self) -> None:
        self.result = HTTPData()

    def _parser_query_string(self, path: str) -> dict:
        parsed_query = {}

        try:
            query_start = path.index('?')
        except ValueError:
            return {}

        self.result.path = path[0:query_start]

        query_string = path[query_start + 1::]
        query_list = query_string.split('&')

        for q in query_list:
            try:
                key, value = q.split('=')
            except ValueError:
                return None

            parsed_query[key] = value

        return parsed_query

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

                if ',' in value or ';' in value and name != 'Cookie':
                    sub_values = value.split(',')
                    filtered_values = []

                    for sv in sub_values:
                        sv = sv.strip()
                        filtered_values.append(sv)

                    parsed_headers[name] = filtered_values
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

        if msg_parts[-1]:
            self.result.body = msg_parts[-1]

        msg_parts.pop()
        msg_parts.pop()

        self.result.method = method
        self.result.path = path
        self.result.version = version

        self.result.real_path = self.result.path
        self.result.query = self._parser_query_string(path)
        self.result.headers = self._parser_headers(msg_parts)

        self.result.host = self.result.headers.get('Host')
        self.result.user_agent = self.result.headers.get('User-Agent')
        self.result.accept = self.result.headers.get('Accept')

        cookies = self.result.headers.get('Cookie')

        if cookies:
            self.result.cookies = self._parser_cookies(cookies)
            self.result.headers.pop('Cookie')

        return self.result

    def __repr__(self) -> str:
        return f'HTTPParser(result={self.result})'
