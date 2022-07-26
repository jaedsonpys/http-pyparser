import json
from typing import Union


class Response(object):
    """This class is used to create HTTP message data store.
    You can use the `make_response` function to generate an HTTP message.
    """

    def __init__(
        self,
        body: Union[str, dict, list, int, float],
        status: int = 200,
        content_type: str = 'text/html',
    ) -> None:
        """Create a response.

        :param body: Body.
        :type body: Union[str, dict, list, int, float]
        :param status: HTTP status code, defaults to 200
        :type status: int, optional
        :param content_type: Response content type, defaults to 'text/html'
        :type content_type: str, optional
        """

        self.body: Union[str, dict, list, int, float] = body
        self.status: int = status
        self.content_type: str = content_type

        self.cookies = []
        self.headers = {}

    def set_cookie(
        self, name: str, value: str,
        max_age: int = None, path: str = None,
        secure: bool = False, http_only: bool = False
    ) -> None:
        """Set a cookie"""

        self.cookies.append({
            'name': name,
            'value': value,
            'attributes': {
                'Max-Age': max_age,
                'Path': path,
                'Secure': secure,
                'HttpOnly': http_only
            }
        })

    def set_header(self, name: str, value: str) -> None:
        """Set a header"""
        self.headers[name] = value

    def __repr__(self) -> str:
        return f'Response(body={self.body}, status={self.status}, content_type={self.content_type}, '\
               f'cookies={self.cookies}, headers={self.headers})'


def make_response(response: Response) -> str:
    """Create an HTTP message from the
    Response object.

    :param response: Response object.
    :type response: Response
    :raises TypeError: If the body's data type is not 
    "str", "float", "int", "dict" or "list".
    :return: Returns the HTTP message
    :rtype: str
    """

    http = list()
    used_headers = list()

    # set default headers
    http.append(f'HTTP/1.1 {response.status}')

    # if the body is a JSON
    if type(response.body) in (dict, list):
        body_data = json.dumps(response.body)
        content_type = 'application/json'
    elif type(response.body) in (str, int, float):
        body_data = str(response.body)
        content_type = 'text/html'
    else:
        # body type not accepted
        raise TypeError(f'The body argument can be "dict", "list", "int", '
                        f'"float", and "str", but not {type(response.body)}')

    if response.content_type != 'text/html':
        http.append(f'Content-Type: {response.content_type}')
    elif response.headers.get('Content-Type'):
        http.append(f'Content-Type: {response.headers.get("Content-Type")}')
    else:
        http.append(f'Content-Type: {content_type}')

    for key, value in response.headers.items():
        if key not in used_headers:
            header_str = f'{key}: {value}'
            used_headers.append(key)
            http.append(header_str)

    if response.cookies:
        for cookie in response.cookies:
            name = cookie['name']
            value = cookie['value']

            cookie_header = f'Set-Cookie: {name}={value}; '

            for attr_name, attr_value in cookie['attributes'].items():
                if type(attr_value) == bool and attr_value:
                    cookie_header += f'{attr_name}; '
                elif attr_value is not False and attr_value is not None:
                    cookie_header += f'{attr_name}={attr_value}; '

            http.append(cookie_header[:-2])

    # defining the body of the response
    http.append('')
    http.append(body_data)

    http_message = '\r\n'.join(http)

    return http_message
