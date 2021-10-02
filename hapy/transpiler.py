"""
I'm thinking of gathering all the things into one function...
"""
from input_stream import InputStream
from token_stream import TokenStream
from token_parser import parse
from generate_py import make_py

def transpile(code: str, local: bool = False) -> str:
   """transpile .hapy code to python code from string"""
   inputs = InputStream(code)
   tokens = TokenStream(inputs)
   ast = parse(tokens)
   python_code = make_py(ast, local)

   return python_code
