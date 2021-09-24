"""
generate the python code from AST tree
AST -> Abstract Syntax Tree... thank you Jesus!
"""

import json
from  token_stream import TokenStream
from input_stream import InputStream
from parser import parse
from exec import run
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

def make_py(token):

	indent_lvl = 0

	def pythonise(token, indent=0):
		indent = indent
		switch = {
		"num": py_atom,
		"str": py_atom,
		"bool": py_atom,
		"var": py_var,
		"binary": py_binary,
		"assign": py_assign,
		"function": py_function,
		"if": py_if,
		"while": py_while,
		"call": py_call,
		"prog": py_prog
		}

		nonlocal indent_lvl

		doer = switch.get(token["type"], None)
		# print('doer',doer)

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
		return "{left} {op} {right}".format(
			**{"left": pythonise(tok["left"]), "op": tok["operator"], 
				"right": pythonise(tok["right"])})

	def py_assign(tok):
		# just return the token
		return py_binary(tok)

	def py_function(tok):
		# just return the token
		return json.dumps(tok["value"])

	def py_if(tok):
		# return python looking function...
		"""
			if cond:
				expressions! thank you Jesus!
		"""
		# global indent_lvl
		# nonlocal indent
		# indent += 1
		# print(indent)
		nonlocal indent_lvl
		indent_lvl += 1
		print("-" * indent_lvl)
		# o = "\nif (" + pythonise(tok["cond"]) + "):\n    "\
		# + pythonise(tok["then"]) + "\n" + ("\nelse:\n    " + pythonise(tok["else"]) if tok.get("else", None) else "")

		
		o = "\nif (" + pythonise(tok["cond"]) + "){"\
		+ pythonise(tok["then"]) + "}" + ("\nelse {" + pythonise(tok["else"]) + "}" if tok.get("else", None) else "")
	

		indent_lvl -= 1
		return o

	def py_while(tok):
		# just return the token
		return json.dumps(tok["value"])

	def py_call(tok):
		# just return the token
		return pythonise(tok["func"]) + "({args})".format(**{"args":
			", ".join(list(map(lambda x:pythonise(x), tok["args"])))
			})

	def py_prog(tok):
		# just return the token
		return ";".join(list(map(lambda x:pythonise(x), tok["prog"])))

	return pythonise(token)

if __name__ == "__main__":
	code = """
			age = 30; # lvl 0
			if(age < 18) { # lvl 0
				print('old!'); # lvl 1
				if (age == 30) { # lvl 1
					print('Not quite adult!')
				}
			} else {
				print('YOUNG!')
			}
			"""
	# code = """
	# 			3 * 2
	# 		"""
	# code = "age is (1 plus 1); name is 'emma'"
	inputs = InputStream(code)
	tokens = TokenStream(inputs)
	ast = parse(tokens)
	python_code = make_py(ast)

	print(python_code)
	run(python_code)