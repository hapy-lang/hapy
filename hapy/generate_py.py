"""
generate the python code from AST tree
AST -> Abstract Syntax Tree... thank you Jesus!
"""

import json
from token_stream import TokenStream
from input_stream import InputStream
from token_parser import parse
from exector import run
from importer import get, hapy_modules
"""
function make_js(exp) {
    return js(exp);

    function js(exp) {
        switch (exp.type) {
          case "num"    :
          case "str"    :
          case "bool"   : return js_atom   (exp);
          case "var"    : return js_var    (exp);
          case "binary" : return js_binary (exp);
          case "assign" : return js_assign (exp);
          case "let"    : return js_let    (exp);
          case "lambda" : return js_lambda (exp);
          case "if"     : return js_if     (exp);
          case "prog"   : return js_prog   (exp);
          case "call"   : return js_call   (exp);
          default:
            throw new Error("Dunno how to make_js for " + JSON.stringify(exp));
        }
    }

    // NOTE, all the functions below will be embedded here.
}
"""

indent = "    "

word_ops = {
    "and": "and",
    "or": "or",
    "is": "=",
    "plus": "+",
    "minus": "-",
    "times": "*",
    "dividedby": "/"
}


def handle_operators(op: str) -> str:
    """ convert custom operators to python operators... """
    # check if string, else just return op

    if op.isalpha():
        return word_ops.get(op)
    else:
        return op


def make_py(token, local: bool=False):
    """local is if this file is a local file"""

    indent_lvl = 0

    def pythonise(token, indent=0):
        indent = indent
        switch = {
            "num": py_atom,
            "str": py_atom,
            "bool": py_atom,
            "var": py_var,
            "module": py_var,
            "binary": py_binary,
            "assign": py_assign,
            "access": py_access,
            "function": py_function,
            "import": py_import,
            "if": py_if,
            "list": py_list,
            "while": py_while,
            "call": py_call,
            "prog": py_prog
        }

        nonlocal indent_lvl

        doer = switch.get(token["type"], None)

        if not doer:
            raise Exception("Invalid Hapy code: %s" % json.dumps(token))

        return doer(token)

    # helper functions
    def py_atom(tok):
        # just return the token
        if tok["type"] == "bool":
            return "%s" % tok["value"]
        return json.dumps(tok["value"])

    def py_var(tok):
        # just return the token
        return tok["value"]

    def py_binary(tok):
        # just return the token
        if tok["operator"] == ".":
            return "{left}{op}{right}".format(
         **{"left": pythonise(tok["left"]),
             "op": handle_operators(tok["operator"]),
             "right": pythonise(tok["right"])})
        else:
            return "{left} {op} {right}".format(
             **{"left": pythonise(tok["left"]),
                 "op": handle_operators(tok["operator"]),
                 "right": pythonise(tok["right"])})

    def py_assign(tok):
        # just return the token
        return py_binary(tok)

    def py_access(tok):
        # for dot access stuff... thank you Jesus!
        return py_binary(tok)

    def py_function(tok):
        # just return the token
        # o is output :) thank you Jesus!

        args = " ({args})".format(**{
            "args":
            ", ".join(list(map(lambda x: pythonise(x), tok["vars"])))
        })

        o = "def " + pythonise(tok["name"]) + args + "{"\
        + pythonise(tok["body"]) + "}"

        return o

    def py_list(tok):
        # just return the token
        # o is output :) thank you Jesus!

        o = " [{args}]".format(**{
            "args":
            ",".join(list(map(lambda x: pythonise(x), tok["elements"])))
        })

        return o

    def py_if(tok):
        # return python looking function...
        nonlocal indent_lvl
        indent_lvl += 1
        print("-" * indent_lvl)
        # o = "\nif (" + pythonise(tok["cond"]) + "):\n    "\
        # + pythonise(tok["then"]) + "\n" + ("\nelse:\n    " +
        # pythonise(tok["else"]) if tok.get("else", None) else "")

        o = "if (" + pythonise(tok["cond"]) + "){\n"\
        + pythonise(tok["then"]) + "}" + ("\nelse {\n" + pythonise(tok["else"]) +\
         "}" if tok.get("else", None) else "")

        indent_lvl -= 1
        return o

    def py_while(tok):
        """while loop, returns python while loop!"""

        o = "while (" + pythonise(tok["cond"]) + "){"\
        + pythonise(tok["then"]) + "}"

        return o

    def py_call(tok):
        # just return the token
        return pythonise(tok["func"]) + "({args})".format(**{
            "args":
            ", ".join(list(map(lambda x: pythonise(x), tok["args"])))
        })

    def py_import(tok):
        """paste import statement in code
        Importing in Hapy. You can import:
        - Another .hapy "module"
        - A "custom" builtin module, see popo and test lol
        - Actual Python builtin modules, no restrictions for now!

        It was challenging at first, but thank God we achieved it.
        :)
        """

        status, imp_type, result = get(tok["module"]["value"], is_local=local)

        if status and imp_type in (1, 2):
            # this means it's a hapy builtin or
            # another local module
            # this adds a statement that makes that module available in the code
            # I haven't tested it for multiple embedded imports. I'm afraid :]

            o = result + "\n"
        elif status and imp_type == 3:
            # this means it's neither a Hapy module nor a local module...
            # and it starts with 'py_*' this is how we differentiate Python
            # modules in Hapy. For now...
            o = "import {module}\n".format(**{"module": result})
        elif not status:
            # this module is neither a hapy builtin, custom local module
            # or even a python module that starts with 'py_'
            # return an error!
            o = "# !!! Hapy cannot import {module}. Sorry :/ !!!\n".\
            format(**{"module": tok["module"]["value"]})

        return o

    def py_prog(tok):
        # just return the token
        # TODO: maybe add closing ; at the end of the program? DISCUSS IT
        return ";\n".join(list(map(lambda x: pythonise(x), tok["prog"])))

    return pythonise(token)

if __name__ == "__main__":
   #  code = """
			# age = 30; # lvl 0
			# if(age<18){ # lvl 0
			# 	print('old!'); # lvl 1
			# 	if(age == 30) { # lvl 1
			# 		print('Not quite adult!')
			# 	};

			# 	while(True){
			# 		print('popoooo!')
			# 	};
			# }else{
			# 	print('YOUNG!');
			# }
			# """

    code = """
    		import math;
            import test; # THIS IS A CUSTOM MODULEEE!!!
            import something; # THIS IS A LOCAL MODULE
            print(math.pi);
            print(test.__name__);
            print(test.func1());
            print(something.do_something)
    		"""
    # code = "age is (1 plus 1); name is 'emma';print(age)"
    inputs = InputStream(code)
    tokens = TokenStream(inputs)
    ast = parse(tokens)
    python_code = make_py(ast)

    print(python_code)
    run(python_code)
