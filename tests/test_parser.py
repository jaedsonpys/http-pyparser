# This test uses BuPyTest (https://github.com/jaedsonpys/bupytest).
# Follow the documentation to see how to run.

import sys

sys.path.insert(0, './')

import bupytest
import http_pyparser

HTTP_MESSAGE = ('GET /api/user?email=test@gmail.com&age=18 HTTP/1.1\r\n'
                'Host: 127.0.0.1:5200\r\n'
                'Connection: keep-alive\r\n'
                'sec-ch-ua-platform: "Linux"\r\n'
                'User-Agent: Mozilla/5.0 (X11; Linux x86_64) '
                'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36\r\n'
                'Accept: text/html,image/apng,*/*;q=0.8\r\n'
                'Accept-Encoding: gzip, deflate, br\r\n'
                'Accept-Language: pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7\r\n'
                'Cookie: test_cookie=0123456789\r\n\r\n')


class TestParser(bupytest.UnitTest):
    def __init__(self):
        super().__init__()
        self.parser = http_pyparser.HTTPParser()

    def test_parse_message(self):
        parsed_http = self.parser.parser(HTTP_MESSAGE)
        
        self.assert_expected(parsed_http.path, '/api/user')
        self.assert_expected(parsed_http.method, 'GET')
        self.assert_expected(parsed_http.version, 'HTTP/1.1')

        self.assert_expected(parsed_http.cookies, {'test_cookie': '0123456789'})
        self.assert_expected(parsed_http.query, {'email': 'test@gmail.com', 'age': '18'})


if __name__ == '__main__':
    bupytest.this()
