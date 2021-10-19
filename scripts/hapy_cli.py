from io import open_code
import os
import click
import sys
from click_default_group import DefaultGroup
from hapy.exector import run, run2
from hapy.transpiler import transpile
from hapy.importer import all_local_modules, hapy_modules


def check_commands(command: str) -> None:
    res = True
    if command == "clear":
        # obviosly put a check here for the current operating system!
        os.system("cls")
    elif command == "see modules":
        # obviosly put a check here for the current operating system!
        locs = "\n".join(all_local_modules())
        haps = "\n".join(hapy_modules.keys())
        click.echo("""Type `import <module>` to import a module.
			\nOr `import py_<python module>` for Python modules.
			\nHapy Modules:\n{}
			\nLocal Modules:\n{}""".format(haps, locs))
    else:
        res = False

    return res


@click.group(cls=DefaultGroup, default='run', default_if_no_args=True)
def cli():
    """This is the Hapy programming language command-line tool.
	- Hapy CLI can execute .hapy files

	You can contribute to Hapy here https://github.com/hapy-lang/hapy
	"""
    pass


@click.command()
@click.argument('filename', type=click.Path(exists=True))
@click.option('-c', '--compile-only', 'compile_only', is_flag=True, help="Compiles the Hapy code only,\
	does not execute")
@click.option('-s', '--save', 'save', is_flag=True, help="Should save compiled Python to file")
def run(filename, compile_only, save, inline):
    """Execute Hapy files
	Can either
	1. Compile and return compiled code or
	2. Compile, execute and return output
	"""

    cwd = os.getcwd()
    compiled_python = ""

    click.echo(f'Running {filename}! from {cwd}')

    with open(filename, "r") as file:
        hapy_code = file.read()
        compiled_python = transpile(hapy_code)

    if inline:
        # compile the python or execute!
        compiled_python = transpile(hapy_code)
        if compile_only:
            return click.echo(compiled_python)
        else:
            return run2(compiled_python)

    # if user wants to save file!
    if save:
        new_filename = filename.rstrip(".hapy") + ".ha.py"
        click.echo("\n\n" +"Saving file in same folder as %s" % new_filename + "\n\n")
        with open(new_filename, "w") as py_file:
            py_file.write(compiled_python)

    if compile_only:
        click.echo(compiled_python)
    else:
        # execute the compiled code
        run2(compiled_python)


# Inline compilation
@click.command()
@click.argument('code', type=str)
@click.option('-c', '--compile-only', 'compile_only', is_flag=True, help="Compiles the Hapy code only,\
	does not execute")
# @click.option('-s', '--save', 'save', is_flag=True, help="Should save compiled Python to file")
def inline(code, compile_only):
    """Compile Hapy from line of code"""
    compiled_python = ""

    if code:
        # compile the python or execute!
        compiled_python = transpile(code)
        if compile_only:
            return click.echo(compiled_python)
        else:
            return run2(compiled_python)


@click.command()
# no options for now... thank you Jesus!
def repl():
    """the Hapy REPL"""

    prompt = f"hapy >"
    click.echo(
        "Welcome to the Hapy REPL! Type a command and carry on!\n type exit() or Ctrl+C to close."
    )
    try:
        while True:
            try:
                _in = input(f'{prompt} ')
                # check for REPL commands...
                # How do we support block statements?
                # check if the last character is { then
                # ask for more input...
                try:
                    result = False
                    code = _in
                    open_brackets = 0
                    closing_brackets = 0

                    if code.endswith("{"):
                        # do procedure
                        # get the line, ask for more input
                        # when the number of open brackets
                        # equal the number of closing,
                        # then finish loop and return
                        # code += _in
                        code += "\n"  # add this to make it if cond {\n
                        open_brackets += 1
                        # closing_brackets = 0

                        while open_brackets != closing_brackets:
                            in_2 = input("... ")
                            # TODO: find a better way of checking if line ends in
                            # "}" or "};"
                            if in_2.endswith("}") or in_2.endswith("};"):
                                code += "\n"
                                closing_brackets += 1
                            # if there are more brackets...
                            if in_2.endswith("{"):
                                code += "\n"
                                open_brackets += 1
                            code += in_2

                            # check if code ends in 2 \n line brakes

                        result = False
                    result = check_commands(code)
                    # print('code => ', repr(code))

                    if not result:
                        code_2_run = transpile(code)
						# maybe only transpile then exec?
                        # print('2-run => ', repr(code_2_run))
                        click.echo(eval(code_2_run))
                except Exception as e:
                    # check if _in ends in :

                    code_2_run = transpile(code)
                    # print(code)
                    out = exec(code_2_run)
                    if out is not None:
                        click.echo(out)
            except Exception as e:
                click.echo(f"Error: {e}")
    except KeyboardInterrupt as e:
        click.echo('\nBye! Exiting Hapy...')


# assign commands to the cli command group...
cli.add_command(run)
cli.add_command(repl)
cli.add_command(inline)
