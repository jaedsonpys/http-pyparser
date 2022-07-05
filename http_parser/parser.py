class HTTPData(object):
    def __init__(
        self,
        path: str,
        status: str,
        body: str = None,
        version: str = None,
        headers: dict = None,
        cookies: dict = None,
    ) -> None:
        self.path = path
        self.status = status
        self.version = version
        self.body = body
        self.headers = headers
        self.cookies = cookies
