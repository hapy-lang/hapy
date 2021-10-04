from exector import run, run2
from transpiler import transpile

if __name__ == "__main__":
   # Just testing das'all...
    code = """
            # def hello(name="Emma"){
            def hello(name){
               print('Hello %s' % name);
            };

            hello();
         """

    run(transpile(code))
