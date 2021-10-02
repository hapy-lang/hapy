from exector import run, run2
from transpiler import transpile

if __name__ == "__main__":
   # Just testing das'all...
    code = """
            import py_math;
            # import test; # THIS IS A CUSTOM MODULEEE!!!
            import something; # THIS IS A LOCAL MODULE
            # import hello;
            # print(math.pi);
            # print(test.__name__);
            # print(test.func1());
            # print(something);
            # print(dir(something));
            # print(something);
            # something.sayHello('David');
         """

    run(transpile(code))
