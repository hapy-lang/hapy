"""
execute python from string! thank you Jesus!
"""

import sys
from io import StringIO

codeOut = StringIO()
codeErr = StringIO()

def run(code: str):
	sys.stdout = codeOut
	sys.stderr = codeErr

	exec(code)

	sys.stdout = sys.__stdout__
	sys.stderr = sys.__stderr__

	s = codeErr.getvalue()

	print("error: \n%s\n" % s)

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