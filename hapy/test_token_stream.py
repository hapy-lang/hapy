import unittest

from input_stream import InputStream
from token_stream import TokenStream


class TestTokenStream(unittest.TestCase):
    def test_read_next_number(self):
        """test read number function"""

        stream = InputStream("30.034")

        ts = TokenStream(stream)

        expected = {"type": "num", "value": 30.034}
        actual = ts.read_next()

        self.assertEqual(expected, actual, "the stream is a number")

    def test_read_next_string(self):
        """test read number function"""

        stream = InputStream('"Thank you Jesus"')

        ts = TokenStream(stream)

        expected = {"type": "str", "value": "Thank you Jesus"}
        actual = ts.read_next()

        self.assertEqual(expected, actual, "the stream is a string")

    def test_skip_comment(self):
        """test read number function"""

        stream = InputStream('#this is a comment!\n"Hello my friend!"')

        ts = TokenStream(stream)

        expected = {"type": "str", "value": "Hello my friend!"}
        actual = ts.read_next()

        self.assertEqual(expected, actual,
                         "the stream is a comment, whitespace & string")

    def test_read_identifier_keywords(self):
        """test identifier function"""

        stream = InputStream('return "goat"')

        ts = TokenStream(stream)

        expected = {"type": "kw", "value": "return"}
        actual = ts.read_next()

        self.assertEqual(expected, actual, "the stream is a keyword")

    def test_read_identifier_varnames1(self):
        """test identifier function to identify variable names"""

        stream = InputStream('cow = "animal"')

        ts = TokenStream(stream)

        expected = {"type": "var", "value": "cow"}
        actual = ts.read_next()

        self.assertEqual(expected, actual, "the stream is an identifier")

    def test_read_operator(self):
        """test identifier function"""

        stream1 = InputStream('>=')

        ts1 = TokenStream(stream1)

        expected1 = {"type": "op", "value": ">="}

        actual1 = ts1.read_next()

        # test multi character operator: => //
        stream2 = InputStream('and')

        ts2 = TokenStream(stream2)

        expected2 = {"type": "op", "value": "and"}

        actual2 = ts2.read_next()

        self.assertEqual([expected1, expected2], [actual1, actual2],
                         "the stream is a operation char")

    def test_read_punctuation(self):
        """test identifier function to identify variable names"""

        stream = InputStream('{"cow": "animal"}')

        ts = TokenStream(stream)

        expected = {"type": "punc", "value": "{"}

        actual = ts.read_next()

        self.assertEqual(expected, actual, "the stream is a punctuation mark")

    def test_read_dot(self):
        """test identifier function to identify dot operator"""
        # we are treeating the '.' as a binary operator in a sense

        stream = InputStream('"hello".upper()')

        ts = TokenStream(stream)

        expected = {"type": "op", "value": "."}

        ts.read_next() # first token
        actual = ts.read_next() # 2nd...

        self.assertEqual(expected, actual, "Expected a dot token")


if __name__ == "__main__":
    unittest.main()
