from exector import run, run2
from transpiler import transpile
import math

if __name__ == "__main__":
   # Just testing das'all...
   code = """
         import something;

         p = something.Person(name="a", school="v");

         print(p);

         """

   run2(transpile(code))
