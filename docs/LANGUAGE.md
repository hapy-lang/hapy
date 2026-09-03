# Hapy Language Reference

A syntax cheatsheet for Hapy, compiled from the parser/tokenizer source and
the test suite. See the [README](../README.md) for installation and CLI
usage; this doc is about the language itself.

## Pipeline

```
source text
  -> InputStream      (chars, tracks line/col, reads #!lang= and HAPY_LANG)
  -> TokenStream       (chars -> tokens: num / str / kw / var / op / punc)
  -> token_parser.parse (tokens -> AST)
  -> generate_py.make_py (AST -> Python source string)
  -> exector.run2       (exec the generated Python)
```

## Choosing a language

Hapy has two vocabularies for every keyword/operator/builtin: Hausa
(default) and English. Pick one with either:

```hapy
#! lang=eng
```

as the very first line of a file, or by setting the `HAPY_LANG` environment
variable (`eng` for English, anything else falls back to Hausa). The CLI's
`--english`/`-e` flag sets this for you.

All examples below are in English for readability; every keyword has a
Hausa equivalent (table below).

## Keywords

| Hausa        | English  | Meaning                          |
|--------------|----------|-----------------------------------|
| `in`         | `if`     | conditional                       |
| `kokuma`     | `elif`   | else-if branch                    |
| `then`       | `then`   | (reserved, not required in blocks)|
| `indai`      | `while`  | while loop                        |
| `ma`         | `for`    | for loop                          |
| `karo`       | `import` | import a module                   |
| `tsarin`     | `class`  | class definition                  |
| `yanada`     | `has`    | declare a class property          |
| `gada`       | `inherits` | class inheritance                |
| `anfani`     | `use`    | forward a property to parent's init |
| `wuce`       | `pass`   | no-op statement                   |
| `daga`       | `from`   | (reserved; `from X import Y` is not supported) |
| `imbahakaba` | `else`   | else branch                       |
| `cikin`      | `in`     | membership (also an operator word, see below) |
| `Babu`       | `None`   | null value                        |
| `dawo`       | `return` | return from a function             |
| `ayyana`     | `def`    | function/method definition        |
| `Gaskiya`    | `True`   | boolean true                      |
| `Karya`      | `False`  | boolean false                     |

## Operators

Symbolic operators are the same in both languages: `> < == != >= <= - + / * ** // % . = :`

Word-form operators (translated, and each wired to a Python equivalent by
`generate_py.py`'s `word_ops` table):

| Hausa      | English (source word) | Compiles to |
|------------|------------------------|-------------|
| `da`       | `and`                  | `and`       |
| `ko`       | `or`                   | `or`        |
| `shine`    | `is`                   | `=` (assignment, see below) |
| `ba`       | `not`                  | `!=`        |
| `cikin`    | `in`                   | `in`        |
| `hada`     | `plus`                 | `+`         |
| `chire`    | `minus`                | `-`         |
| `times`    | `times`                | `*`         |
| `raba`     | `dividedby`            | `/`         |

> `of`, `not in`, `is equal`, and `is not equal` exist in the translation
> tables but aren't usable operators today. It's not just a missing dict
> entry: the tokenizer only ever reads one word at a time, so a two-word
> phrase like `is equal` comes out as two separate tokens (`is`, `equal`)
> rather than one operator token - `age is equal 10` currently compiles to
> nonsense (`age = equal 10`). Supporting these needs multi-word lookahead
> in `TokenStream`, a small lexer feature, not a quick dict fix. `of` is
> additionally unclear in intent - it's been an untranslated placeholder
> since the very first commit, possibly meant for a possessive/genitive
> construct (`age of person`), but nothing in the codebase confirms that.

Assignment can be written with `=` or the word `is` - both produce the same
AST shape, just tagged with a different operator:

```hapy
age = 20;
age is 20;      # equivalent
```

## Builtin functions

| Hausa        | English (`py_`-callable name) |
|--------------|-------------------------------|
| `nuna`       | `print`                       |
| `iri`        | `type`                        |
| `tsakanin`   | `range`                       |
| `kirga`      | `len`                         |
| `rubuta`     | `input`                       |
| `duka`       | `all`                         |
| `tace`       | `filter`                      |
| `koyar`      | `help`                        |
| `id`         | `id`                          |
| `lissafta`   | `eval`                        |
| `ni`         | `self` (inside class methods) |
| `__farada__` | `__startwith__` (maps to Python's `__init__`) |
| `__donnunawa__` | `__toshow__` (maps to Python's `__repr__`) |

## Syntax reference

Blocks are always `{ ... }` (no Python-style indentation), and a statement
that ends in a block is itself terminated with a trailing `;`.

### Conditionals

```hapy
if (20 > 10) {
    print('Greater!');
} elif (10 > 20) {
    print('Also checked');
} else {
    print('Smaller!');
};
```

### While loop

```hapy
while (True) {
    print('true!');
};
```

### For loop

```hapy
for (n in [1, 2, 3]) {
    print(n);
};
```

The `n in [1, 2, 3]` header is itself a first-class "membership" expression
- the same node type you'd get from writing `n in [1,2,3]` outside a loop.

### Lists and dicts

```hapy
nums = [1, 2, '3', [20]];   # lists can nest and mix types
empty = [];

person = {"name": "Ada", "age": 30};   # dict entries must be key: value pairs
```

Indexing works on both, chains, and can be an assignment target:

```hapy
nums = [10, 20, 30];
first = nums[0];        # 10
nums[1] = 99;            # in-place update
grid = [[1, 2], [3, 4]];
grid[1][0];              # 3, chained indexing

person = {"name": "Ada"};
person["name"];          # "Ada"
```

### Dot access

```hapy
'hello'.isalpha();
```

`.` is parsed as a regular binary operator (highest precedence), so
method-chaining falls out of the normal expression grammar rather than a
special case.

### Functions

```hapy
def sayHello(name) {
    print(name);
};

sayHello('Emmanuel');
```

### Classes

```hapy
class Woman {
    has height;
    has age = 22;         # supports default values

    def greet() {
        print('hi');
    }
}

class Child inherits Woman {
    has height;
    has age = 22;

    use Woman(height);     # forwards `height` to the parent's __init__
                            # (age is NOT duplicated as a plain self.age = age)

    def __startwith__() {  # -> Python's __init__
        print('constructed!');
    };

    def __toshow__() {     # -> Python's __repr__
        return "Representation!";
    };
}
```

### Imports

```hapy
import py_os;        # a Python builtin module (the `py_` prefix is stripped)
import places;        # a Hapy builtin module (see hapy/importer.py:hapy_modules)
import helpers;        # a local `helpers.hapy` file in the same directory
```

- No `from X import Y` syntax.
- No packages - local modules are single files resolved relative to the
  directory of the file being run.

### Comments

```hapy
# runs to end of line
```

## Known limitations

- Error messages are not localized and are generally minimal.
- No multi-file packages; local modules are single `.hapy` files ("bites").
- `of`, `not in`, `is equal`, `is not equal` are reserved but not
  implemented as usable operators (see the Operators table above).
- Performance has not been measured or optimized.

## Where things live

- `hapy/translations.py` - the Hausa/English word tables (source of truth
  for the tables above).
- `hapy/input_stream.py` - raw character stream, language selection.
- `hapy/token_stream.py` - tokenizer.
- `hapy/token_parser.py` - recursive-descent parser, produces the AST.
- `hapy/generate_py.py` - AST -> Python source.
- `hapy/importer.py` - resolves builtin/local/Python module imports.
- `tests/` - the executable spec for all of the above; when in doubt about
  exact behavior, the tests are more precise than this document.
