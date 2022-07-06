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
