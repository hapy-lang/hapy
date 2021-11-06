"""
Input Stream. Oh LORD Help me! Thank you Jesus!
https://lisperator.net/pltut/parser/input-stream

funcs:
next() - get next value and remove from stream
peek() - return next char but don't remove it
eof() - return True iff no more chars left
choke() - throw an error
"""
from .translations import keywords, operator_words
import os
class InputStream:
    def __init__(self, input):
        """Initialize vars"""
        self.input = input
        self.pos = 0
        self.line = 0
        self.col = 0
        self.first_line = input.strip().split("\n", 1)[0]
        self.settings = {
            "lang": "hausa"
        }

        # First check the ENV VARS tho
        LANG = os.getenv('HAPY_LANG')
        if LANG:
            self.settings["lang"] = LANG.strip()

        if self.first_line and self.first_line.startswith("#!"):
            # ignore the '#!'
            settings_pairs = self.first_line[2:].split()

            for s in settings_pairs:
                d = s.split("=")
                # if key is lang and is not eng, make it hausa
                self.settings[d[0]] = d[1]

        self.settings["lang"] = self.settings["lang"] if self.settings["lang"] == "eng" else "hausa"

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
