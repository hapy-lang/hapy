"""
I'm thinking of gathering all the things into one function...
"""
from input_stream import InputStream
from token_stream import TokenStream
from token_parser import parse
from generate_py import make_py
from indent import indent
from exector import run


def transpile(code: str, local: bool = False, no_indent=False) -> str:
    """transpile .hapy code to python code from string"""
    inputs = InputStream(code)
    tokens = TokenStream(inputs)
    ast = parse(tokens)
    unindented_code = make_py(ast, local)
    # indent python code here...
    if no_indent:
        return unindented_code

    python_code = indent(unindented_code)

    return python_code


if __name__ == '__main__':
    #  code = """
    # if (n < 5) {
    #   print("Printed ", n);
    #   n = n + 1;
    #   print("inside if => ", n);
    # if (n == 1) {
    # print('N is one!')
    # } else {
    #       print('N is not one!')
    #   }
    #  };
    #          """
    code = """
    class Rectangle {
    has length;
    has width;

    def when_created() {};

    def area() {
        return self.length * self.width;
    };

    def perimeter() {
        return 2 * self.length + 2 * self.width;
    };

};

class Square inherits Rectangle {
    has length;

    use Rectangle(length, length);

    def when_created() {};
};

sq = Square(4);

print(sq.area());

class Cube inherits Square {

    def surface_area() {
        face_area = super().area();
        return face_area * 6;
    };

    def volume() {
        face_area = super().area();
        return face_area * self.length;
    };
};

c = Cube(3);

print(c.surface_area());
    """

    print(transpile(code, no_indent=False))
