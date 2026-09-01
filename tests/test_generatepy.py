""" Test InputStream class.
"""
import unittest
from hapy.input_stream import InputStream
from hapy.token_stream import TokenStream
from hapy.token_parser import parse
from hapy.generate_py import make_py

class TestGeneratePy(unittest.TestCase):
    def test_binary_ops_1(self):
        """test the binary ops bro"""
        code = """
				age = 20;
				age > 10;
				"""

        inputs = InputStream(code)
        tokens = TokenStream(inputs)
        ast = parse(tokens)

        expected = """age = 20;\n(age > 10)"""

        actual = make_py(ast)

        self.assertEqual(expected, actual, "This is a binary operator!")

    def test_binary_ops_words(self):
        """test the binary ops bro"""
        code = """
        #! lang=eng
				bola_age is 20;
				tolu_age is 30 minus 10;
				"""

        inputs = InputStream(code)
        tokens = TokenStream(inputs)
        ast = parse(tokens)

        expected = """bola_age = 20;\ntolu_age = (30 - 10)"""

        actual = make_py(ast)

        self.assertEqual(expected, actual, "This is a binary operator!")

    def test_while_loop_body_is_generated(self):
        """regression test: py_while used to drop its body entirely due to
        a missing line-continuation in a string concatenation"""
        code = """
        #! lang=eng
                while (True) {
                    print('true!');
                };
            """

        inputs = InputStream(code)
        tokens = TokenStream(inputs)
        ast = parse(tokens)

        actual = make_py(ast)

        self.assertIn("print(\"true!\")", actual,
                       "the while loop's body must appear in generated code")

    def test_elif_and_else(self):
        """elif/else branches should all appear in the generated code"""
        code = """
        #! lang=eng
                if (1 > 2) {
                    print('a');
                } elif (2 > 1) {
                    print('b');
                } else {
                    print('c');
                };
            """

        inputs = InputStream(code)
        tokens = TokenStream(inputs)
        ast = parse(tokens)

        actual = make_py(ast)

        self.assertIn("print(\"a\")", actual)
        self.assertIn("elif (", actual)
        self.assertIn("print(\"b\")", actual)
        self.assertIn("else {", actual)
        self.assertIn("print(\"c\")", actual)

    def test_floordiv_and_pow_do_not_crash(self):
        """regression test: '//' and '**' used to be tokenizable but had
        no PRECEDENCE entry, so parsing them raised a raw KeyError"""
        code = """
        #! lang=eng
                a = 10 // 3;
                b = 2 ** 3;
            """

        inputs = InputStream(code)
        tokens = TokenStream(inputs)
        ast = parse(tokens)

        actual = make_py(ast)

        self.assertIn("//", actual)
        self.assertIn("**", actual)

    def test_dict_with_non_key_value_entries_is_a_syntax_error(self):
        """regression test: {1,2,3} used to silently parse as a 'dict'
        instead of raising a clear syntax error"""
        code = """
        #! lang=eng
                a = {1,2,3};
            """

        inputs = InputStream(code)
        tokens = TokenStream(inputs)

        with self.assertRaises(Exception):
            parse(tokens)


if __name__ == "__main__":
    unittest.main()
