### a roughpaper on ideas, documentation, todos and notes
### can later be used to generate our docs...

things I want ha.py to support... (15/09/21)

This dialect should be able to be used to teach Python. That's it!

- [x] if statements // since version 0.0.1
- [x] WHILE statements
--- okay for now :)
- [x] for loops
- [x] lists
- [ ] dicts
- [x] classes
- [x] dot notation for accessing object methods
- [ ] accessing iterator elements // list[0] # maybe we'll just use a special function :]
# Like list.get(2) ...
 not really important:
- [x] import statements # not _fully_ tested yet :]
- [ ] switch statements # hmm...

```

### NOTES
- 1. Always check if token_stream recognizes the new keyword you added by
including it in the list of keywords... 
- 2. I noticed `return self.name * 2;` this returned the wrong thing. The precendence should be like this
 `return (self.name) * 2` - has been fixed btw

While is like if

IF COND {
	EXPRESSION(S)
}

WHILE COND {
	EXPRESSION(S)
}

--- structure of a for loop

FOR ( var in collection ) {
	EXPRESSIONA(S)
}

```

### THIS SHOULD BE PART OF A CHANGELOG!

`parse_varname` now returns `var` tokens :) instead of plain strings. Adjust accordingly :p

<!-- PYTHON SUBLIME TEXT SETTINGS
{
	"ensure_newline_at_eof_on_save": true,
	"rulers": [
		72, 79
	],
	"tab_size": 4,
	"translate_tabs_to_spaces": false,
	"trim_trailing_white_space_on_save": true,
}
-->

## dots
something like this "'hello friend'.uppercase()" should have these tokens:
- a str token
- a punc token
- a call token

maybe we can treat '.' as a binary operator?

## imports

```python
import py_os; # imports the 'os' builtin module from python
import places # imports a builtin hapy module named 'places'
import custom_module # imports a user defined custom module from the same directory

# usage is the same
- Does not support `from bla import foo` syntax, sorry :p
- other notes to be added...
```

I created some `.hapy` files for testing.
Try importing a built-in module or another hapy module and then importing it in `main.py` then
run main... `python main.py`

## for loops

so apparently, this is invalid syntax in Python:

```python
for (n in range(10)): # brackets not allowed in the header of forloops?
	print(n)
```

```python
for n in range(10): # this is fine... but it works for while loops and ifs
	print(n)
```

## Classes

```text
class ClassName inherits ParentClass {
	# these are just expressions. Maybe I should loop through and rearrange them
	# from [{random tokens}] to {"properties", "class_funcs", "methods"}
	has name;
	has age = 0;

	use ParentClass(name);

	def when_created() { # special constructor function (i don't want it to start with 'def o!)
		print('Initialized!');
	};

	def when_string() { # special constructor function
		print('Initialized!');
	};

	def when_printed() { # special constructor function
		print('Initialized!');
	};

	def greet() { # i think just a regular function definition makes sense?
		# we pass self for you!
		print('Hello! my name is => ', self.name);
	}
}

```

```python
class ClassName(ParentClass):
	# we'll add support for docstring later

	def __init__(self, name, age = 0):
		# for parent class stuff...
		super().__init__(name)

		self.age = age

		print('Initialized!')

	def __str__(self): # special constructor function
		print('Initialized!')

	def __repr__(self): # special constructor function
		print('Initialized!')

	def greet(self): # i think just a regular function definition makes sense?
		# we pass self for you!
		print('Hello! my name is => ', self.name)
```