""" Test InputStream class. Thank you Jesus!
"""
import unittest
from input_stream import InputStream
from token_stream import TokenStream
from parser import parse
from generate_py import make_py


class TestGeneratePy(unittest.TestCase):
    def test_binary_ops_1(self):
        """ test the binary ops bro """
        code = """
				age = 20;
				age > 10;
				"""

        inputs = InputStream(code)
        tokens = TokenStream(inputs)
        ast = parse(tokens)

        expected = """age = 20;age > 10;"""

        actual = make_py(ast)

        self.assertEqual(expected, actual, "This is a binary operator!")

    def test_binary_ops_words(self):
        """ test the binary ops bro """
        code = """
				bola_age is 20;
				tolu_age is 30 minus 10;
				"""

        inputs = InputStream(code)
        tokens = TokenStream(inputs)
        ast = parse(tokens)

        expected = """bola_age = 20;tolu_age = 30 - 10;"""

        actual = make_py(ast)

        self.assertEqual(expected, actual, "This is a binary operator!")


if __name__ == "__main__":
    unittest.main()
