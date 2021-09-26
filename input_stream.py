"""
Input Stream. Oh LORD Help me! Thank you Jesus!
https://lisperator.net/pltut/parser/input-stream

funcs:
next() - get next value and remove from stream
peek() - return next char but don't remove it
eof() - return True iff no more chars left
choke() - throw an error
"""


class InputStream:
    def __init__(self, input):
        """Initialize vars"""
        self.input = input
        self.pos = 0
        self.line = 0
        self.col = 0

    # def __str__(self):
    # 	print("<InputStream '{s}'>".format(self.input))

    def next(self) -> str:
        """return next value"""
        try:
            char = self.input[self.pos]
        except IndexError:
            char = ""

        # if we reach a new line char, inc line, reset col. else cont.
        if char == '\n':
            self.line += 1
            self.col = 0
        else:
            self.col += 1

        # move current position
        self.pos += 1

        return char

    def peek(self) -> str:
        """returns next char, keep position"""
        try:
            char = self.input[self.pos]
        except IndexError:
            return ""

        return char

    def eof(self) -> bool:
        """Check if end of file"""
        return self.peek() == "" or self.peek() is None

    def croak(self, msg: str):
        """raises an error"""
        raise Exception(msg + " ({}:{})".format(self.line, self.col))
