"""
I'm thinking of gathering all the things into one function...
"""
from .input_stream import InputStream
from .token_stream import TokenStream
from .token_parser import parse
from .generate_py import make_py
from .indent import indent
from .exector import run


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
    if (True) {
    print('True')
}
    """

    print(transpile(code, no_indent=False))
