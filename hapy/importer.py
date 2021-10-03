import sys
import glob  # noqa: E401, F401
from importlib import util  # noqa: E401

# NOTE: these are just test hapy builtins lol
# but this is how we will define them...
hapy_modules = {
    "test": "modules/test_module.py",
    "popo": "modules/popo_module.py"
    }

def is_local_module(mod_name: str):
    """
    check if mod_name is the name of a file in the current directory
    TODO: set current working dir to the dir of the executed file!!!
    if we are excuting a file of course...
    """
    all_hapyfiles = list(map(lambda x: x.rstrip('.hapy'), glob.glob("*.hapy")))

    return mod_name in all_hapyfiles

def make_module(code: str, module_name: str):
    """
    this creates a python module named module_name from code string
    and returns the 'import' statement for that module that makes
    the module accessible in the file that imported it, you get?
    """

    my_spec = util.spec_from_loader(module_name, loader=None)
    my_module = util.module_from_spec(my_spec)

    """
    THANK YOU JESUS! THIS THING SAVED THIS CODE!

    the challenge: adding sys to globals :/
    """
    my_module.__dict__["sys"] = sys

    exec(code, my_module.__dict__)

    sys.modules[module_name] = my_module

    # this makes this imported module available as a variable
    # in the host file...
    return """# --- import ---\n{m} = sys.modules["{m}"];\n# --- import ---"""\
        .format(** {"m": module_name})


def get(module_name: str, is_local: bool = False) -> str:
    """import a built in module"""

    # is_local is to prevent local files from importing
    # other local files two levels deep :) [deprecated]
    """
    1. first check if the module is built-in,
        - if so, load the code and module
    2. if not buillt-in search the local system for it
        - if found, fetch the code and transpile it to python
        - then load module as normal
    3. then conclude that it's a Python built-in module and return
        the plain import statement
    """
    code = ""
    import_result = ""

    if module_name in hapy_modules.keys():
        module_file = hapy_modules.get(module_name)
        with open(module_file, "r") as file:
            code = file.read()

            # format for import_result => (status: bool, type: [1,2,3,4],
            # result: import_string | module_name)

            import_result = (True, 1, make_module(code, module_name))

    elif is_local_module(module_name):
        from transpiler import transpile
        # transpile local module and all...
        # TODO: we are assuming the file exists! WRONG!
        module_file = module_name + ".hapy"
        with open(module_file, "r") as file:
            code = file.read()
            # nonlocal transpile
            # now we have to transpile this code to python!
            pyc = transpile(code, local=True)

            import_result = (True, 2, make_module(pyc, module_name))
    elif module_name.startswith("py_"):
        # if the module name starts with this, its a python module
        # just remove the py_ and import normally, else it's an error!

        import_result = (True, 3, module_name.lstrip("py_"))
    else:
        import_result = (False, 4, None)

    # TODO: we're assuming the file exists!

    return import_result
