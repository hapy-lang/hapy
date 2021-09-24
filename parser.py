"""
parser
from: https://lisperator.net/pltut/parser/the-parser
"""
import json
from  token_stream import TokenStream
from input_stream import InputStream
# py"import os from OS"

FALSE = { "type": "bool", "value": False }

def any_fulfill(collection, condition):
	"""checks if any element of collection returns true for condition """
	a = False
	index = 0
	while not a and index < len(collection):
		a = condition(collection[index])
		index += 1
	return a



def parse(input: TokenStream):
	"""parse input to AST tokens"""

	PRECEDENCE = {
		"=": 1, "is": 1,
		"or": 2,
		"and": 3,
		"<": 7, ">": 7, "<=": 7, ">=": 7, "==": 7, "!=": 7,
		"+": 10, "-": 10, "plus": 10, "minus": 10,
		"*": 20, "/": 20, "%": 20, "times": 20, "dividedby": 20
	}

	# the program first level! thank you Jesus!

	def is_punc(ch):
		tok = input.peek()
		return tok and tok["type"] == "punc" and (not ch or tok["value"] == ch) and tok

	def is_kw(kw):
		tok = input.peek()
		return tok and tok["type"] == "kw" and (not kw or tok["value"] == kw) and tok

	def is_op(op):
		tok = input.peek()
		return tok and tok["type"] == "op" and (not op or tok["value"] == op) and tok    

	def skip_punc(ch):
		if is_punc(ch):
			input.next()
		else:

			# if the punc we are meant to skip is ';' then there's probs
			# something wrong with the syntax :|
			if ch == ";":
				return unexpected("Check your syntax! You might have made an error at %s")

			input.croak(f"Expecting punctuation got: \"{ch}\"")

	def skip_kw(kw):
		if is_kw(kw):
			input.next()
		else:
			input.croak(f"Expecting keyword got: \"{kw}\"")

	def skip_op(op):
		if is_op(op):
			input.next()
		else:
			input.croak(f"Expecting punctuation got: \"{op}\"")

	def unexpected(msg = "unexpected token: %s "):
		input.croak(msg % json.dumps(input.peek()))

	def maybe_binary(left, my_prec):
		tok = is_op(None)
	
		if tok:
			their_prec = PRECEDENCE[tok["value"]]
			if their_prec > my_prec:
				input.next()
				return maybe_binary({
					"type": "assign" if tok["value"] == "=" or tok["value"] == "is" else "binary",
					"operator": tok["value"],
					"left": left,
					"right": maybe_binary(parse_atom(), their_prec)
				}, my_prec) # made a mistake here initially, put their_prec instead :|

		return left

	def delimited(start, stop, separator, parser):
		""" get all the args for example """
		args, first = [], True

		skip_punc(start)
		while not input.eof():
			if is_punc(stop):
				break
			if first:
				first = False
			else:
				skip_punc(separator)
			if is_punc(stop):
				break
			args.append(parser())
		skip_punc(stop)
		return args

	def parse_call(func):
		return {
		"type": "call",
		"func": func,
		"args": delimited("(", ")", ",", parse_expression)
		}

	def parse_varname():
		name = input.next()
		if name["type"] != "var":
			input.croak("Expecting variable name")
		return name["value"]

	def parse_if():
		skip_kw("if")
		cond = parse_expression()
		# if (!is_punc("{")) skip_kw("then"); REASON: no then in python :]
		# sha, I can add it tho...
		then = parse_expression()
		ret = {
			"type": "if",
			"cond": cond,
			"then": then
		}
		if is_kw("else"):
			input.next()
			ret["else"] = parse_expression()

		# TODO: look into `else_if/elif`
		# if is_kw("else_if"):
		# 	input.next()
		# 	ret["else"] = parse_expression()

		return ret

	def parse_while():
		""" this is literally the same as parse_if but I keep seperate just in case """

		skip_kw("while")

		cond = parse_expression()
		
		then = parse_expression()

		ret = {
			"type": "while",
			"cond": cond,
			"then": then
		}
		
		return ret

	def parse_function():
		return {
			"type": "function",
			"name": parse_varname(), # get variable name, that should be the next thing! Thank you Jesus
			"vars": delimited("(", ")", ",", parse_varname),
			"body": parse_expression()
		}

	def parse_bool():
		return {
			"type": "bool",
			"value": input.next()["value"] == "True"
		}

	def maybe_call(expr):
		expr = expr()
		return parse_call(expr) if is_punc("(") else expr


	def parse_atom():
		""" success, thank you Jesus! """
		def doer():

			if is_punc("("):
				input.next()
				exp = parse_expression()
				skip_punc(")")
				return exp
			if is_punc("{"):
				return parse_prog()
			if is_kw("if"):
				return parse_if()
			if is_kw("while"):
				return parse_while()
			if is_kw("True") or is_kw("False"):
				return parse_bool()
			if is_kw("def"):
				input.next()
				return parse_function()
			
			tok = input.next()

			if (tok["type"] == "var") or (tok["type"] == "num") or (tok["type"] == "str"):
				return tok

			unexpected()

		return maybe_call(doer)

	def parse_prog():
		# TODO: I need to work on this for Python! Thank you Jesus!
		prog = delimited("{", "}", ";", parse_expression)
		if len(prog) == 0:
			return FALSE
		if len(prog) == 1:
			return prog[0]
		return { "type": "prog", "prog": prog }

	def parse_expression():
		def doer():
			nonlocal maybe_binary
			nonlocal parse_atom
			return maybe_binary(parse_atom(), 0)

		return maybe_call(doer)

	def parse_toplevel():
		prog = []
		while not input.eof():
			prog.append(parse_expression())
			if not input.eof():
				# this means that there are still expressions to run!
				# but of course, if it doesn't make sense it won't work.
				# the next token may not be ;...
				skip_punc(";")
		return {"type": "prog", "prog": prog}

	# the first thing...
	return parse_toplevel()

if __name__ == "__main__":
	# code = """
	# 			if (20 > 10) {
	# 				print('Greater!');
	# 			if (True) {
		#  			print('bbs')
	# }
	# 			} else {
	# 				print('Smaller!');
	# 			};
	# 		"""
	# code = """
	# 		biggest+smallest = 50
	# 		"""
	# code = "age is (1 plus 1); name is 'emma'"
	inputs = InputStream(code)
	tokens = TokenStream(inputs)
	print(tokens)
	ast = parse(tokens)

	print(ast)
	# unexpected()