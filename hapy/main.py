from exector import run, run2
from transpiler import transpile

if __name__ == "__main__":
   # Just testing das'all...
    code = """
            import py_math;

            def hello(year, age, name="Emma"){
               print('Hello %s' % name, 'you are %d' % age);
               print('You were born in %d' % year)
            };

            hello(age=20.3, year=1999);
         """

    run(transpile(code))
