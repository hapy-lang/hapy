"""
execute python from string! thank you Jesus!
"""

import sys
import traceback
import code as _code
from io import StringIO

codeOut = StringIO()
codeErr = StringIO()


# I'm not sure if we need this still. I know sha that we need a way
# to set the exec know what module is running...
def run2(source: str, file=False):
    lcls = {"sys": sys, "__name__": "__main__"}
    interpreter = _code.InteractiveInterpreter(locals=lcls)
    # here, we are saying this guy come's from the main_string
    interpreter.runsource(source, '<main_string>', 'exec')


def run(code: str):
    sys.stdout = codeOut
    sys.stderr = codeErr

    try:
        exec(code)
    except Exception as e:
        err = e
        traceback.print_exc()

    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__

    err = codeErr.getvalue()

    if err:
        print("error: \n%s\n" % err)

    s = codeOut.getvalue()

    print("output: \n%s" % s)

    codeOut.close()
    codeErr.close()


if __name__ == '__main__':
    code = """
                if (20 > 10) {
                    print('Greater!');
                } else {
                    print('Smaller!');
                };
            """
    run(code)
