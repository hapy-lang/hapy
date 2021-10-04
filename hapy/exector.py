"""
execute python from string! thank you Jesus!
"""

import sys, traceback
import code as _code
from io import StringIO

codeOut = StringIO()
codeErr = StringIO()


# I'm not sure if we need this still. I know sha that we need a way
# to set the exec know what module is running...
def run2(source: str, file=False):
    interpreter = _code.InteractiveInterpreter()
    interpreter.runsource(source, '<main>', 'exec')


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
