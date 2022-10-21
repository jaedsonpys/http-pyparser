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

        self.cookies: dict = {}
        self.headers: dict = {}

    def set_cookie(self, name: str, value: str) -> None:
        """Set a cookie"""
        self.cookies[name] = value

    def set_header(self, name: str, value: str) -> None:
        """Set a header"""
        self.headers[name] = value

    def __repr__(self) -> str:
        return f'Response(body={self.body}, status={self.status}, content_type={self.content_type}, '\
               f'cookies={self.cookies}, headers={self.headers})'
