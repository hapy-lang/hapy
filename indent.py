""" indent this blessed thing """
"""
Take a string of code and for each newline, check if it's the beginning of a block
, if so strip line and add indent then increase indent level, if you meet an ext }
, reduce indent level...
"""


def indent() -> str:
    code = """
	age = 20.0; # 0
	if (age > 18.0){print("old!"); # 1
	if (age < 25.0){print("Not quite adult!")}}
	else {print("YOUNG!")}
	"""
    """
	take a string of code and loop through each line and character, if you reach ';' add
	"""

    indent_lvl = 0
    I = 4
    o = ""

    for line in code.split("\n"):
        line = line.strip()

        for c in line:
            if c == ";":
                print(line)
                o += line.strip(";") + "\n"

            if c == "{":
                print(line)
                o += ' ' * I * indent_lvl + line.replace(
                    "{", ":\n").lstrip().rstrip('{\n')
                indent_lvl += 1
                print(indent_lvl)
            if c == "}":
                o += ' ' * I * indent_lvl + line.lstrip().rstrip('}\n')
                indent_lvl -= 1
                print(indent_lvl)

    print(o)


if __name__ == '__main__':
    indent()
