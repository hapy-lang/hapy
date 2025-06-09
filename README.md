![Hapy Logo](https://i.ibb.co/XW5pQG1/hapy-logo-1-1.jpg)

# Hapy - Write Python in Hausa with braces!

_pronounced like ha·pee like "Happy"_

Hapy is a simple programming language that uses Hausa vocabulary and compiles to Python. Originally as a final year school project.

## Installation

Hapy can be installed using pip (pre-release versions)

**note:** Hapy is still in development so it might change _a lot_ before full release. You can still join us for the ride!

```
pip install hapy
```

> If you have installation problems on Windows, try [installing Python](https://python.org/downloads) from the Python website gan and not Microsoft Store.

Check if Hapy is accessible globally, open a new Command-line/terminal and run `hapy --help`. If you're not seeing Hapy your Python packages directory may not be in PATH or some other pip/python issue. We noticed all problems disappear when we get Python from their website.

## Usage

All these commands are to be run in the command line:

`hapy --help` - prints the help message

`hapy --version` or `hapy -v` - prints the installed Hapy version

`hapy` or `hapy repl` - launches the REPL. Exit via `exit()`, or `Ctrl-C`. Pass `--english` to use Hapy english vocabulary.

`hapy <filename>` - execute a script. Hapy uses `.hapy` file extension. For example: `hapy lagbaja.hapy`. Pass `--compile-only` to just print the compiled script or you can pass `--save` to save the compiled Python in a file.

`hapy run <filename>` - same as above.

`hapy do "<code to evaluate>"` - compiles and executes Hapy code as a string. Pass `--compile-only` to skip execution or pass `--english`/`-e` to use Hapy english vocabulary.

More options on the way :)

## Example

> Let's say 'ayyana' is `def` keyword in Hausa and 'buga' is the `print` keyword.
> Sample Hapy code

```python
    # example.hapy

    # wannan sharhi ne
    ayyana muje(){
        nuna("Let's Goooooo");
    };

    muje();
```

Python output after running `hapy example.hapy --save`

```python
    # example.ha.py

    # wannan sharhi ne
    def muje():
        print("Let's Goooooo")

    muje()
    >>> "Let's Goooooo"
```

## Contributing

OH MY GOSH 😂😭, WE'RE SO DESPERATE FOR CONTRIBUTIONS THAT WE'RE LITERALLY BEGGING FOR PULL REQUESTS 🙏🏼💻! WE'RE SERIOUSLY ABOUT TO START CRYING OVER HERE. PLEASE, PLEASE, PLEASE SEND A PR AND MAKE OUR DAY. WE'LL LOVE YOU FOREVER AND EVER ❤️🤗.

## Documentation

on it's way...

### Hausa -> English Dictionary

`key (Hausa): value (English)`

```python
keywords = {
     "in": "if",
    "kokuma": "elif",
    "then": "then",
    "indai": "while",
    "ma": "for",
    "karo": "import",
    "tsarin": "class",  #Changed from irin to tsarin(structure) in 0.5.0
    "yanada": "has",
    "gada": "inherits",
    "anfani": "use",
    "wuce": "pass",
    "daga": "from",
    "imbahakaba": "else",
    "cikin": "in",
    "Babu": "None",
    "dawo": "return",
    "ayyana": "def",
    "Gaskiya": "True",
    "Karya": "False",
    "nuna": "print"
}

operators_words = {
    "ba": "not",
    "da": "and",
    "ko": "or",
    "shine": "=",
    "cikin": "in",
    "of": "of",
    "ba cikin": "not in",
    "is equal": "is equal",
    "is not equal": "is not equal",
    "times": "*",
    "hada": "+",
    "raba": "/",
    "chire": "-"
}

builtin_functions = {
    "__farada__": "__init__",
    "__donnunawa__": "__repr__",
    "nuna": "print",
    "iri": "type",
    "tsakanin": "range",
    "kirga": "len",
    "rubuta": "input",
    "duka": "all",
    "tace": "filter",
    "koyar": "help",
    "id": "id",
    "lissafta": "eval",
}

```

## Goals

- Be able to write code in Hausa
- Support some Python constructs
- Have a limited set of custom modules :)
- Be able to upload and install other snippets (called _bites_) online [soon...]

## Non-goals / Limitations

- Hapy won't try to support all Python _things_.
- Error messages are not the best currently and won't be translated
- No multi-file Hapy packages, only single file modules (called _bites_)
- Performance has not been measured yet

## Differences with Python syntax

- For design and implementation reasons, Hapy uses braces :-)
- I'm not exactly sure _why_ but Hapy requires semi-colons at the end of statements :-(
- We have some arithmetic word operators such as `plus`, `times`
- Classes are _different_. More details in the (soon to come) docs

## Standard library

On it's way...

## Noticed something wrong with Hapy or have a suggestion?

SEND A PR MY BROTHA/SISTA or create an issue on the [github](https://github.com/hapy-lang/hapy/issues/new)

## Other projects

On it's way...

### Credits and inspiration

- (heavily) inspired by this great, easy-to-follow [tutorial on programming languages](https://lisperator.net/pltut)
- The REPL is based on this nice [article](https://dev.to/amal/building-the-python-repl-3468)
- We use [Click](https://click.palletsprojects.com/en/8.0.x/) for the CLI
- [Tutorial](https://medium.com/nerd-for-tech/how-to-build-and-distribute-a-cli-tool-with-python-537ae41d9d78) on distributing Pypi packages
- Some code from [Bython](https://github.com/mathialo/bython) is used in our indent module

## Similar projects

- [Yorlang](https://anoniscoding.github.io/yorlang/docs/doc.html): Yoruba language programming language (Nodejs/Javascript)
- [Enkelt](https://enkelt.io/): Swedish language programming language Enkelt (Python)

## License

Hapy is released under the [MIT License](https://opensource.org/licenses/MIT)

## Reference

If you found Hapy useful enought to cite, please cite using the following BibTeX:
```
@software{segunlean2021,
  author = {Segun-Lean, Emmanuel and Wuta, Shugaba},
  title = {Hapy: Hausa Programming Language},
  month = December,
  year = 2021,
  url = {https://github.com/hapy-lang/hapy}
}
