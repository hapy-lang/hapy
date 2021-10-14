import os
import click
import sys
from click_default_group import DefaultGroup
from hapy.main import do
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
    """This is the Hapy programming language commandline tool.
	- Hapy CLI can execute .hapy files

	You can contribute to Hapy here https://github.com/hapy-lang/hapy
	"""
    pass


@click.command()
@click.argument('filename', type=click.Path(exists=True))
def run(filename):
    """Execute Hapy files"""

    cwd = os.getcwd()
    click.echo(f'Running {filename}! from {cwd}')

    with open(filename, "r") as file:
    	content = file.read()
    	do(content)


@click.command()
# no options for now... thank you Jesus!
def repl():
	"""the Hapy REPL"""

	where = cwd = os.getcwd()
	prompt = f"({where}) hapy>"
	click.echo("Welcome to the Hapy REPL! Type a command and carry on!\n type exit() or Ctrl+C to close.")
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

					if code.endswith("{"):
						# do procedure
						# get the line, ask for more input
						# when the number of open brackets
						# equal the number of closing,
						# then finish loop and return
						# code += _in
						code += "\n" # add this to make it if cond {\n
						open_brackets = 1
						closing_brackets = 0

						while open_brackets != closing_brackets:
							in_2 = input("... ")
							if in_2.endswith("}"):
								code += "\n"
								closing_brackets += 1
							code += in_2
							# check if code ends in 2 \n line brakes

						result = False

					result = check_commands(code)
					print('code => ', repr(code))

					if not result:
						code_2_run = transpile(code)
						print('2-run => ', repr(code_2_run))
						click.echo(eval(code_2_run))
				except:
					# check if _in ends in :
					code_2_run = transpile(_in)
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
