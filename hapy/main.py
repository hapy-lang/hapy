from exector import run, run2
from transpiler import transpile

if __name__ == "__main__":
   # Just testing das'all...
    code = """
            import py_math;

            def hello(age, name="Emma"){
               print('Hello %s' % name, 'you are %d' % age)
            };

            hello(20.3);
         """

    run(transpile(code))
