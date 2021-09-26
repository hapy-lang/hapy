""" Test InputStream class. Thank you Jesus!
"""
import unittest
from input_stream import InputStream


class TestInputStream(unittest.TestCase):
    def test_next(self):
        """Test input.next()"""

        st = "Hello"
        stream = InputStream(st)
        expected = "H"
        actual = stream.next()

        self.assertEqual(expected, actual, "Next char is 'H'")

    def test_location_change(self):
        """Test if the location props change properly"""

        st = "Hello"
        stream = InputStream(st)
        stream.next()
        stream.next()
        stream.next()

        # line should be 0, pos = 3, col = 3
        expected = (0, 3, 3)

        actual = (stream.line, stream.pos, stream.col)

        self.assertEqual(expected, actual, "Stream location is (0,3,3)")

    def test_peek(self):
        """Test input.peek()"""

        st = "Hello"
        stream = InputStream(st)
        stream.next()  # change current char to next value

        stream.peek()  # peek should not change position of current character

        expected = "e"

        actual = stream.peek()

        self.assertEqual(expected, actual, "Current char is 'e'")

    def test_eof(self):
        """Test input.eof()"""

        st = "wow!"
        stream = InputStream(st)
        stream.next()  # o
        stream.next()  # w
        stream.next()  #!
        stream.next()  # nothing...

        stream.peek()  # peek should be empty or None

        self.assertTrue(stream.eof(), "At end of stream!")


if __name__ == "__main__":
    unittest.main()
