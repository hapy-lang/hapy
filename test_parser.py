import unittest
from parser import parse
from input_stream import InputStream
from token_stream import TokenStream

class TestParser(unittest.TestCase):
	"""Test Parser doe"""

	"""
	- Test assignment to variable (string, num)
	"""
	def test_string_assignment(self):
		"""test assignment to variable gives correct AST tree"""

		code = "name = 'Emmanuel'"

		expected = {
		  "type": "prog",
		  "prog": [
		    {
		      "type": "assign",
		      "operator": "=",
		      "left": { "type": "var", "value": "name" },
		      "right": { "type": "str", "value": "Emmanuel" }
		    }
		  ]
		}
		actual = parse(TokenStream(InputStream(code)))

		self.assertEqual(expected, actual, "Expression is a string assignment!")

	def test_num_assignment(self):
		"""test assignment to variable gives correct AST tree"""

		code = "jordan = 23"

		expected = {
		  "type": "prog",
		  "prog": [
		    {
		      "type": "assign",
		      "operator": "=",
		      "left": { "type": "var", "value": "jordan" },
		      "right": { "type": "num", "value": 23.0 }
		    }
		  ]
		}
		actual = parse(TokenStream(InputStream(code)))

		self.assertEqual(expected, actual, "Expression is a number assignment!")

	def test_assignment_with_is(self):
		"""test assignment to variable using 'is' keyword"""

		code = "jordan is 23"

		expected = {
		  "type": "prog",
		  "prog": [
		    {
		      "type": "assign",
		      "operator": "is",
		      "left": { "type": "var", "value": "jordan" },
		      "right": { "type": "num", "value": 23.0 }
		    }
		  ]
		}
		actual = parse(TokenStream(InputStream(code)))

		self.assertEqual(expected, actual, "Expression is a number assignment!")

	def test_binary_2_operands(self):
		"""
		- Test binary operators (comparative and arithmetic)
		"""
		code = "2 + 3"

		expected = {
		  "type": "prog",
		  "prog": [
		    {
		      "type": "binary",
		      "operator": "+",
		      "left": { "type": "num", "value": 2.0 },
		      "right": { "type": "num", "value": 3.0}
		    }
		  ]
		}
		actual = parse(TokenStream(InputStream(code)))

		self.assertEqual(expected, actual, "Expression is a binary of 2 operands!")


	def test_binary_3_operands_ltr(self):
		"""
		Test binary operation with 3 operands in increasing order of operator 
		precedence
		"""
		code = "2 + 3 * 4"

		expected = {
		  "type": "prog",
		  "prog": [
		    {
		      "type": "binary",
		      "operator": "+",
		      "left": { "type": "num", "value": 2.0 },
		      "right": { "type": "binary", "operator": "*",
		       "left": { "type": "num", "value": 3.0 },
		       "right": { "type": "num", "value": 4.0 }}
		    }
		  ]
		}
		actual = parse(TokenStream(InputStream(code)))

		self.assertEqual(expected, actual, "Expression is a binary of 3 operands!")

	def test_binary_3_operands_rtl(self):
		"""
		Test binary operation with 3 operands in decreasing order of operator 
		precedence
		"""
		code = "2 * 3 + 4"

		expected = {
		  "type": "prog",
		  "prog": [
		    {
		      "type": "binary",
		      "operator": "+",
		      "left": { 
		      	"type": "binary", "operator": "*",
			       "left": { "type": "num", "value": 2.0 },
			       "right": { "type": "num", "value": 3.0 }
			    },
		      "right": { "type": "num", "value": 4.0 }
		    }
		  ]
		}
		actual = parse(TokenStream(InputStream(code)))

		self.assertEqual(expected, actual, "Expression is a binary of 3 operands!")

	def test_func_def(self):
		"""
		Test function definition and expressions
		"""
		self.maxDiff = None
		code = """
			def sayHello(name) {
				 2 + 3;
			};"""

		expected = {
		  "type": "prog",
		  "prog": [
		    {
		      "type": "function",
		      "name": {"type": "var", "value": "sayHello"}, # now varnames are proper tokens!
		      "vars": [{"type": "var", "value": "name"}],
		      "body": {
		            "type": "binary",
                    'operator': '+',
		      		"left": {"type": "num", "value": 2},
                    "right": {"type": "num", "value": 3}
					}
		    }
		  ]
		}
		actual = parse(TokenStream(InputStream(code)))

		self.assertEqual(expected, actual, "Expression is a function definition")

	def test_func_call_var(self):
		"""
		Test function call statement
		"""
		code = "sayHello('Emmanuel');"

		expected = {
		  "type": "prog",
		  "prog": [
		    {
		      "type": "call",
		      "func": {"type": "var", "value": "sayHello"},
		      "args": [{"type": "str", "value": "Emmanuel"}]
		    }
		  ]
		}
		actual = parse(TokenStream(InputStream(code)))

		self.assertEqual(expected, actual, "Expression is a function call")

	def test_word_binary(self):
		"""
		Test binary operation using words and, or
		"""
		code = "20 and False"

		expected = {
		  "type": "prog",
		  "prog": [
		    {
		      "type": "binary",
		      "operator": "and",
		      "left": {"type": "num", "value": 20},
		      "right": {"type": "bool", "value": False}
		    }
		  ]
		}
		actual = parse(TokenStream(InputStream(code)))

		self.assertEqual(expected, actual, "Expression is a binary operator using and/or")

	def test_word_binary_arithmetic(self):
		"""
		Test binary operation using words times, plus, minus
		"""
		code = "2 times 3 plus 4"

		expected = {
		  "type": "prog",
		  "prog": [
		     {
		      "type": "binary",
		      "operator": "plus",
		      "left": { 
		      	"type": "binary", "operator": "times",
			       "left": { "type": "num", "value": 2 },
			       "right": { "type": "num", "value": 3 }
			    },
		      "right": { "type": "num", "value": 4 }
		    }
		  ]
		}
		actual = parse(TokenStream(InputStream(code)))

		self.assertEqual(expected, actual, "Expression is a binary arithmetic operator")

	def test_if(self):
		"""
		Test binary operation using words and, or
		"""
		code = """
				if (20 > 10) {
					print('Greater!');
				} else {
					print('Smaller!');
				};
			"""

		expected = {'type': 'prog',
			'prog': [{'type': 'if', 
			'cond': {'type': 'binary', 'operator': '>', 
			'left': {'type': 'num', 'value': 20}, 
			'right': {'type': 'num', 'value': 10}}, 
			'then': {'type': 'call', 'func': {'type': 'var', 'value': 'print'}, 
			'args': [{'type': 'str', 'value': 'Greater!'}]},
			'else': {'type': 'call', 
			'func': {'type': 'var', 'value': 'print'},
			'args': [{'type': 'str', 'value': 'Smaller!'
			}]}}]}
		actual = parse(TokenStream(InputStream(code)))

		self.assertEqual(expected, actual, "Expression is an if statement")

	def test_while(self):
		"""
		Test while loop statement
		"""
		code = """
				while (True) {
					print('true!');
				};
			"""

		expected = {'type': 'prog',
			'prog': [{'type': 'while', 
			'cond': {'type': 'bool', 'value': True}, 
			'then': {'type': 'call', 'func': {'type': 'var', 'value': 'print'}, 
			'args': [{'type': 'str', 'value': 'true!'}]}}]}
		actual = parse(TokenStream(InputStream(code)))

		self.assertEqual(expected, actual, "Expression is a while statement")
	"""
	- test function call
	- test function definition
	- test if statement
	- test diff types of expressions on multiple lines
	"""

if __name__ == '__main__':
	unittest.main()