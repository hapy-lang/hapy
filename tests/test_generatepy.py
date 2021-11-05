""" Test InputStream class. Thank you Jesus!
"""
import unittest
from hapy.input_stream import InputStream
from hapy.token_stream import TokenStream
from hapy.token_parser import parse
from hapy.generate_py import make_py

# TODO: ADD MORE TESTS OOO! TEST OTHER CONSTRUCTS!
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

        expected = """age = 20;\nage > 10"""

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

        expected = """bola_age = 20;\ntolu_age = 30 - 10"""

        actual = make_py(ast)

        self.assertEqual(expected, actual, "This is a binary operator!")


if __name__ == "__main__":
    unittest.main()
