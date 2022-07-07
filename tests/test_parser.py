# This test uses BuPyTest (https://github.com/jaedsonpys/bupytest).
# Follow the documentation to see how to run.

import sys

sys.path.insert(0, './')

import bupytest
import http_pyparser


class TestParser(bupytest.UnitTest):
    def __init__(self):
        super().__init__()
        self.parser = http_pyparser.HTTPParser()


if __name__ == '__main__':
    bupytest.this()
