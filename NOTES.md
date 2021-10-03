### a roughpaper on ideas, documentation, todos and notes
### can later be used to generate our docs...

things I want ha.py to support... (15/09/21)

This dialect should be able to be used to teach Python. That's it!

- [x] if statements // since version 0.0.1
- [x] WHILE statements
--- okay for now :)
- [ ] for loops
- [ ] lists
- [ ] dicts
- [ ] classes
- [ ] dot notation for accessing object methods
- [ ] accessing iterator elements // list[0]
 not really important:
- [ ] import statements
- [ ] switch statements

```

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