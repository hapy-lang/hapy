""" indent this fvcking thing """

"""
Take a string of code and for each newline, check if it's the beginning of a block 
, if so strip line and add indent then increase indent level, if you meet an ext }
, reduce indent level...
"""

def indent(string: str) -> str:
	code = """
	age = 20.0; -\n 0
	if (age > 18.0){\n\tprint("old!"); 1
	if (age < 25.0){print("Not quite adult!")}}
	else {print("YOUNG!")}
	"""

	o = ""

	for line in code.split("\n"):
		line = line.strip()

		for c in line:
			if c == "{":
				o =  ' '*I*indent+line.lstrip().rstrip('{\n')