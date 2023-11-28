import os
from unittest import main, mock, TestCase

from hapy.input_stream import InputStream
from hapy.token_stream import TokenStream

class TestTokenStream(TestCase):
    # TODO: doesn't work idk why. You have to set Env Variables yourself
    @mock.patch.dict(os.environ, {"HAPY_LANG": "eng"})
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

        self.assertEqual(
            expected, actual, "the stream is a comment, whitespace & string"
        )

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

        stream1 = InputStream(">=")

        ts1 = TokenStream(stream1)

        expected1 = {"type": "op", "value": ">="}

        actual1 = ts1.read_next()

        # test multi character operator: => //
        stream2 = InputStream("and")

        ts2 = TokenStream(stream2)

        expected2 = {"type": "op", "value": "and"}

        actual2 = ts2.read_next()

        self.assertEqual(
            [expected1, expected2], [actual1, actual2], "the stream is a operation char"
        )

    def test_read_punctuation(self):
        """test identifier function to identify variable names"""

        stream = InputStream('{"cow": "animal"}')

        ts = TokenStream(stream)

        expected = {"type": "punc", "value": "{"}

        actual = ts.read_next()

        self.assertEqual(expected, actual, "the stream is a punctuation mark")

    def test_read_dot(self):
        """test identifier function to identify dot operator"""
        # we are treating the '.' as a binary operator in a sense

        stream = InputStream('"hello".upper()')

        ts = TokenStream(stream)

        expected = {"type": "op", "value": "."}

        ts.read_next()  # first token
        actual = ts.read_next()  # 2nd...

        self.assertEqual(expected, actual, "Expected a dot token")

    def test_import_statement_1(self):
        """test token stream reading import tokens"""

        stream = InputStream("import names;")

        ts = TokenStream(stream)

        expected = [
            {"type": "kw", "value": "import"},
            {"type": "var", "value": "names"},
        ]

        actual = [ts.read_next(), ts.read_next()]  # 2nd...

        self.assertEqual(expected, actual, "Expected import and names keywords")

    def test_forloop_statement_1(self):
        """test token stream reading forloop statement"""

        stream = InputStream("for (a in b) {\n print(a); };")

        ts = TokenStream(stream)

        expected = {"type": "kw", "value": "for"}

        actual = ts.read_next()

        self.assertEqual(expected, actual, "Expected for loop keyword")


if __name__ == "__main__":
    # NOTE: You have to set the env to "set HAPY_LANG=eng" if you want to
    # test these in english.

    # we should probably create a Hausa version of the tests :)
    main()
