import os
import re
import click
from click_default_group import DefaultGroup
from hapy.exector import run2
from hapy.transpiler import transpile
from hapy.importer import all_local_modules, hapy_modules
from pkg_resources import get_distribution
from hapy import __version__ as expected_version
from code import InteractiveConsole
import sys

installed_version = get_distribution("hapy").version

VERSION = expected_version or installed_version or "N/A"

def check_commands(command: str) -> None:
    res = True
    if command == "clear":
        # obviosly put a check here for the current operating system!
        os.system("cls")
    elif command == "show modules":
        # obviosly put a check here for the current operating system!
        local_modules = "\n".join(all_local_modules())
        hapy_builtins = "\n".join(hapy_modules.keys())
        click.echo("""Use `import <module>` to import a Hapy module.
			\nOr `import py_<python module>` for built-in Python modules.""")

        # list Hapy built-ins
        click.secho("\nHapy Built-in Modules:", fg="green")
        click.echo("{}".format(hapy_builtins))

        # print local modules (later including installed ones)
        click.secho("\nLocal Modules:", fg="green")
        click.echo("{}".format(local_modules))
    else:
        res = False

    return res


@click.group(cls=DefaultGroup, default='repl', default_if_no_args=True, invoke_without_command=True)
@click.option('-v', '--version', 'version', is_flag=True, help="Print the Hapy version")
def cli(version):
    """This is the Hapy programming language command-line tool.
	- Hapy CLI can execute .hapy files

	You can contribute to Hapy here https://github.com/hapy-lang/hapy
	"""

    if version:
        click.secho(f"Hapy {VERSION}", fg='green')
        return

    pass


@cli.command()
@click.argument('filename', type=click.Path(exists=True))
@click.option('-c', '--compile-only', 'compile_only', is_flag=True, help="Compiles the Hapy code only,\
	does not execute")
@click.option('-s', '--save', 'save', is_flag=True, help="Should save compiled Python to file")
def run(filename, compile_only, save):
    """Execute Hapy files
	Can either
	1. Compile and return compiled code or
	2. Compile, execute and return output
	"""

    cwd = os.getcwd()
    compiled_python = ""

    click.secho(f'[i]: Compiling {filename.lstrip(".")}...\n', fg="green")

    # check if file ends in `.hapy` if not throw error!
    if not filename.endswith(".hapy"):
        raise click.ClickException("Not a Hapy file :/")

    with open(filename, "r") as file:
        hapy_code = file.read()
        compiled_python = transpile(hapy_code)

    # if user wants to save file!
    if save:
        new_filename = filename.rstrip(".hapy") + ".ha.py"
        click.secho("\n" +"[i]: Saved file as %s" % new_filename + "\n", fg="green")
        with open(new_filename, "w") as py_file:
            py_file.write(compiled_python)

    if compile_only:
        # click.secho("Compiled code:\n", fg="green", underline=True)
        click.secho(compiled_python, bold=True)
    else:
        # execute the compiled code
        run2(compiled_python)

# Inline compilation
@cli.command()
@click.argument('code', type=str)
@click.option('-c', '--compile-only', 'compile_only', is_flag=True, help="Compiles the Hapy code only,\
	does not execute")
def do(code, compile_only):
    """Compile Hapy from line of code"""
    compiled_python = ""

    if code:
        # compile the python or execute!
        compiled_python = transpile(code)
        if compile_only:
            return click.echo(compiled_python, nl=False)
        else:
            try:
                click.echo(eval(compiled_python), nl=False)
            except:
                try:
                    out = exec(compiled_python)
                    if out is not None:
                        click.echo(out, nl=False)
                except Exception as e:
                        click.echo(f"Error: {e}")

@cli.command(context_settings=dict(
    ignore_unknown_options=True,
    allow_extra_args=True
))
@click.pass_context
@click.option('-e', '--english', 'english', is_flag=True, help="Use Hapy English instead of Hausa")
def repl(ctx, english):
    """the Hapy REPL (interactive programming environment)"""

    prompt = f"hapy>"

    lcls = {"sys": sys, "__name__": "__repl__"}
    runner = InteractiveConsole(locals=lcls)

    # join all the arguments
    all_args = " ".join(ctx.args)
    # only match arguments ending in '.hapy' for now
    # thank you Jesus!
    matched = re.findall(r'([a-zA-Z\./]*\.hapy)', all_args)
    # actually, loop through the args and find all applicable arguments/options
    if len(list(matched)) > 0:
        filename = ""
        compile_only = False
        save = False
        for a in ctx.args:
            if a.endswith(".hapy"):
                filename = a
            elif a == "-c" or a == "--compile-only":
                compile_only = True
            elif a == "-s" or a == "--save":
                save = True

        ctx.invoke(run, filename=filename, compile_only=compile_only, save=save)
        return

    click.secho(
        "Welcome to the Hapy REPL!"
        ,fg="green"
    )


    if (english):
        # tell Hapy compiler that it should listen for English vocabulary
        # one way to do that is to change the ENV_VAR
        os.environ["HAPY_LANG"] = "eng"
        click.secho("-- Language is ENGLISH --")
    else:
        os.environ["HAPY_LANG"] = "hausa"
        # TODO: write this is HAUSA
        click.secho("-- Language is HAUSA --")


    click.echo("\nType a command and just dey go!\nUse exit() or Ctrl+C to close")
    click.secho("\n- Type 'show modules' to list all modules you can use.\n", fg="blue")

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

                        runner.push(code_2_run)
                except Exception as e:
                    # NOTE: I'm not sure if this is still useful...

                    # I stopped using eval/exec because of scope and shii
                    # the variables I defined were not staying
                    print(e)

                    # code_2_run = transpile(code)
                    # # print(code)
                    # # exec(code_2_run)
                    # runner.runcode(code_2_run)
                    # # if out is not None:
                    # #     click.echo(out)
            except Exception as e:
                click.echo(f"Error: {e}")
    except KeyboardInterrupt as e:
        click.echo('\nBye! Exiting Hapy...')
