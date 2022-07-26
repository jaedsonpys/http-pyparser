import sys

sys.path.insert(0, './')

import bupytest
import http_pyparser

HTTP_MESSAGE = ('GET /api/user?email=test@gmail.com&age=18 HTTP/1.1\r\n'
                'Host: 127.0.0.1:5200\r\n'
                'Connection: keep-alive\r\n'
                'sec-ch-ua-platform: Linux\r\n'
                'Accept-Encoding: gzip, deflate, br\r\n'
                'Content-Type: application/json\r\n'
                'Cookie: test_cookie=0123456789\r\n\r\n')


class TestParser(bupytest.UnitTest):
    def __init__(self):
        super().__init__()
        self.parser = http_pyparser.HTTPParser()

    def test_parse_message(self):
        parsed_http = self.parser.parser(HTTP_MESSAGE)
        
        self.assert_expected(parsed_http.path, '/api/user')
        self.assert_expected(parsed_http.real_path, '/api/user?email=test@gmail.com&age=18')

        self.assert_expected(parsed_http.method, 'GET')
        self.assert_expected(parsed_http.version, 'HTTP/1.1')

        self.assert_expected(parsed_http.body, None)
        self.assert_expected(parsed_http.cookies, {'test_cookie': '0123456789'})
        self.assert_expected(parsed_http.query, {'email': 'test@gmail.com', 'age': '18'})

        # headers
        self.assert_expected(
            value=parsed_http.headers,
            expected={
                'Host': '127.0.0.1:5200',
                'Connection': 'keep-alive',
                'sec-ch-ua-platform': 'Linux',
                'Accept-Encoding': ['gzip', 'deflate', 'br'],
                'Content-Type': 'application/json'
            }
        )


class TestResponse(bupytest.UnitTest):
    def __init__(self):
        super().__init__()
        self.response = http_pyparser.Response(
            body='Hello, world!',
            content_type='text/plain'
        )

        self.response.set_cookie('myAuth', '123')
        self.response.set_cookie('myLocal', 'Brazil', secure=True, path='/echo')
        self.response.set_header('Server', 'MyServer')

    def test_make_response(self):
        response = http_pyparser.make_response(self.response)
        expected_response = ('HTTP/1.1 200\r\n'
                             'Content-Type: text/plain\r\n'
                             'Server: MyServer\r\n'
                             'Set-Cookie: myAuth=123\r\n'
                             'Set-Cookie: myLocal=Brazil; Path=/echo; Secure\r\n\r\n'
                             'Hello, world!')
        
        self.assert_expected(response, expected_response)


if __name__ == '__main__':
    bupytest.this()
