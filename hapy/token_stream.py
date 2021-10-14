"""
Tokean Stream, converts each char from InputStream to a token for our AST
e.g {type: 'var', value: 'name'}
There are diff types of Tokens,
variables, digits, operators, keywords, strings etc
"""
from typing import Any, Callable
from .input_stream import InputStream

"""
stuff = { "english_name": "how_we_use_it" }
e.g {"if": "if"} // {"if": "hausa_if"}
"""

keywords = {
    "if": "if",
    "then": "then",
    "while": "while",
    "for": "for",
    "import": "import",
    "class": "class",
    "has": "has",
    "inherits": "inherits",
    "use": "use",
    "pass": "pass",
    "from": "from",
    "else": "else",
    "in": "in",
    "None": "None",
    "return": "return",
    "def": "def",
    "list": "list",
    "True": "True",
    "False": "False"
}

operator_words = {
    "not": "not",
    "and": "and",
    "or": "or",
    "is": "is",
    "in": "in",
    "of": "of",
    "not in": "not in",
    "is equal": "is equal",
    "is not equal": "is not equal",
    "times": "times",
    "plus": "plus",
    "dividedby": "dividedby",
    "minus": "minus"
}

operators = [">", "<", "==", "!=", ">=", "<=", "-", "+", "/", "*", "**", "//",
"%", ".", "="]

# TODO: consider why '//' exists

class TokenStream(InputStream):
    def __init__(self, _input: InputStream):
        super().__init__(_input.input)
        self.current = None
        self.input = _input

        # these keywords would go somewhere else!
        # NOTE! Wow! Removing a callable kw from keywords removed a bug! thank
        # you Jesus
        # self.keywords = " if then while import from else in None return def
        # list True\
        # False "
        self.keywords = keywords
        self.operator_words = operator_words
        self.operators = operators

        # self.operators = " > < >= <= && || "

    def is_keyword(self, ch: str) -> bool:
        """Check if input is a part of keywords List"""
        return ch in self.keywords.values()

    def is_digit(self, ch: str) -> bool:
        """Check if char is a digit"""

        return ch.isdigit()

    def is_id_start(self, ch: str) -> bool:
        """Check if char is a start of a variable name (identifier)"""

        return ch.isalpha() or ch in "_"

    def is_id(self, ch: str):
        """return True iff char is valid Python identifier"""

        return self.is_id_start(ch) or ch.isidentifier() or ch.isdigit()

    def is_op_char(self, ch: str) -> bool:
        """return True iff operational characterer"""

        return ch in "+-*/%=<>!&|."

    def read_op(self):
        """ read operator """

        op = self.read_while(self.is_op_char)

        if op in self.operators:
            return op
        else:
            self.input.croak("Can't handle character: \"%s\"" % op)
            return False

    def is_punc(self, ch: str) -> bool:
        """return True iff is punctuation character"""

        return ch in ":,;(){}[]"

    def is_whitespace(self, ch: str) -> bool:
        """check if ch is whitespace character"""

        return ch.isspace()

    def read_while(self, predicate: Callable[[str], str]) -> str:
        """ read while """

        string = ""

        while (not self.input.eof()) and predicate(self.input.peek()):
            string += self.input.next()
        return string

    def read_number(self) -> bool:
        """ read number """

        has_dot = False

        def function(c: str):
            if c == ".":
                nonlocal has_dot
                if has_dot: return False
                has_dot = True
                return True
            return self.is_digit(c)

        number = self.read_while(function)

        return {
            "type": "num",
            "value": int(number) if ("." not in number) else float(number)
        }

    def read_identifier(self):
        """ read identifier """
        word = self.read_while(self.is_id)

        if word in self.operator_words.values():
            return {"type": "op", "value": word}

        return {
            "type": "kw" if self.is_keyword(word) else "var",
            "value": word
        }

    def read_escaped(self, end: Any):
        """ read escaped """
        escaped, string = False, ""
        self.input.next()
        while not self.input.eof():
            ch = self.input.next()
            if escaped:
                string += ch
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch in end:
                break
            else:
                string += ch

        return string

    def read_string(self):
        """return string token"""

        return {
            "type": "str",
            "value": self.read_escaped(('"', '\'', "'"))
        }

    def skip_comment(self):
        """skip comment"""

        # lambda function since unnamed, used once and returns value simply
        self.read_while(lambda ch: ch != "\n")
        self.input.next()

    def read_next(self):
        """ read next value"""

        self.read_while(self.is_whitespace)

        if self.input.eof():
            return None

        ch = self.input.peek()

        if ch == "#":
            self.skip_comment()
            return self.read_next()

        if ch == '"' or ch == '\'':
            return self.read_string()

        if self.is_digit(ch):
            return self.read_number()

        if self.is_id_start(ch):
            return self.read_identifier()

        if self.is_punc(ch):
            return {"type": "punc", "value": self.input.next()}

        if self.is_op_char(ch):
            return {"type": "op", "value": self.read_op()}

        self.input.croak("Can't handle character: \"%s\"" % ch)

    def peek(self):
        """peek returns the current token"""
        if not self.current:
            self.current = self.read_next()

        return self.current

    def next(self):
        """get next char"""

        tok = self.current
        self.current = None
        return tok or self.read_next()

    def eof(self):
        """check if end of file"""
        
        return self.peek() == "" or self.peek() is None

    def croak(self, msg: str):
        """raises an error"""
        raise Exception(msg +
                        " ({}:{})".format(self.input.line, self.input.col))
