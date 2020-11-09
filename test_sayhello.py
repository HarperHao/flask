"""
Author   : HarperHao
TIME    ： 2020/10/24
FUNCTION:  测试文件
"""
import unittest
from test import sayhello


class SayHelloTestcase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_sayhello(self):
        rv = sayhello()
        self.assertEqual(rv, 'Hello')

    def test_sayhello_to_somebody(self):
        rv = sayhello(to="Harper")
        self.assertEqual(rv, 'Hello,Harper!')


if __name__ == '__main__':
    unittest.main()
