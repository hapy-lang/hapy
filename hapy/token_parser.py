"""
parser
from: https://lisperator.net/pltut/parser/the-parser
"""
import json
from token_stream import TokenStream
from input_stream import InputStream

FALSE = {"type": "bool", "value": False}
PASS = {"type": "var", "value": "pass"}


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
        "=": 1, # not 100% sure why this has 1 precedence :p
        "or": 2,
        "and": 3,
        "<": 7,
        ">": 7,
        "<=": 7,
        ">=": 7,
        "==": 7,
        "!=": 7,
        "+": 10,
        "-": 10,
        "plus": 10,
        "minus": 10,
        "*": 20,
        "/": 20,
        "%": 20,
        "times": 20,
        "dividedby": 20,
        # because self.name is one of the strongest bonds
        "is": 20,
        "in": 20,
        ".": 30,
    }

    # the program first level! thank you Jesus!

    def is_punc(ch):
        tok = input.peek()
        return tok and tok["type"] == "punc" and (not ch or tok["value"]
                                                  == ch) and tok

    def is_kw(kw):
        tok = input.peek()
        return tok and tok["type"] == "kw" and (not kw
                                                or tok["value"] == kw) and tok

    def is_op(op):
        tok = input.peek()
        return tok and tok["type"] == "op" and (not op
                                                or tok["value"] == op) and tok

    def skip_punc(ch):
        if is_punc(ch):
            input.next()
        else:

            # if the punc we are meant to skip is ';' then there's probs
            # something wrong with the syntax :|
            if ch == ";":
                return unexpected(
                    "Check your syntax! You might have made an error at %s")

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

    def unexpected(msg="unexpected token: %s "):
        input.croak(msg % json.dumps(input.peek()))

    def maybe_binary(left, my_prec):
        tok = is_op(None) # thank you Jesus :]
        # tbh, I'm not 100% sure what's going on here, but I'll find out!

        binary_type = {  # noqa: F841
            "is": "assign",
            "=": "assign",
            ".": "access",
            "in": "membership"
        }

        if tok:
            their_prec = PRECEDENCE[tok["value"]]
            if their_prec > my_prec:
                input.next()

                return maybe_binary(
                    {
                        "type": binary_type.get(tok["value"], "binary"),
                        "operator":
                        tok["value"],
                        "left":
                        left,
                        "right":
                        maybe_binary(parse_atom(), their_prec)
                    }, my_prec
                )  # made a mistake here initially, put their_prec instead :|

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
        return {"type": "var", "value": name["value"]}

    def parse_if():
        skip_kw("if")
        cond = parse_expression()
        # if (!is_punc("{")) skip_kw("then"); REASON: no then in python :]
        # sha, I can add it tho...
        then = parse_expression()
        ret = {"type": "if", "cond": cond, "then": then}
        if is_kw("else"):
            input.next()
            ret["else"] = parse_expression()

        # TODO: look into `else_if/elif`
        # if is_kw("else_if"):
        #   input.next()
        #   ret["else"] = parse_expression()

        return ret

    def parse_while():
        """ this is literally the same as parse_if but I keep seperate just in case """

        skip_kw("while")

        cond = parse_expression()

        then = parse_expression()

        ret = {
            "type": "while",
            "cond": cond,
            "then":
            then  # TODO: probably rename this to 'body' to match functions
        }

        return ret

    def parse_forloop():
        """ read a for-loop expression """

        skip_kw("for")

        header = parse_expression() # the iterator...

        body = parse_expression()

        ret = {
            "type": "for",
            "header": header,
            "body": body
        }

        return ret

    def parse_function():
        # skip the 'def' keyword!

        skip_kw("def")

        function_name = parse_varname()

        ret = {"name": function_name}

        if function_name["value"].startswith("when_"):
            # meaning this is a class special method
            # like __init__ in python...
            ret["type"] = "class_special_method"
        else:
            ret["type"] = "function"

        ret = {
              # get variable name, that should be the next thing! Thank you Jesus
            # we are using parse_expression because the args could actually
            # be expressions like assingment def foo(b=1) {...}
            **ret,
            "vars": delimited("(", ")", ",", parse_expression),
            "body": parse_expression()
        }

        return ret

    def parse_class():
        """
        read a class definition.
        1. Look for the classname
        2. Check if there is an inherited class. Only get the first one!
        3. Look for instance methods.
        4. Look for instance properties.
        5. Look for special class methods... constructor, etc...
        5. Collect all and send back dict...

        thank you Jesus!
        """
        # skip 'class' first! Thank you Jesus!

        skip_kw("class")

        # next, get the class name
        classname = parse_varname()

        ret = {
            "type": "class",
            "name": classname
        }

        # if the next token is 'inherits' then get parent class name!...
        # thank you Jesus!
        if is_kw("inherits"):
            skip_kw("inherits")
            # get parent class name...
            parent_classname = parse_varname()
            ret["inherits"] = parent_classname
        # then get the class body expressions...

        expressions = delimited("{", "}", ";", parse_expression)

        # check if there are no expressions. If so, just return pass
        if len(expressions) == 0:
            # just for things that are not class stuff...
            ret["body"] = {"type": "var", "value": "pass"}

        ret["class_properties"] = []
        ret["class_special_methods"] = []
        ret["class_methods"] = []

        # now find all attributes, class_functions and methods
        for e in expressions:
            """
            for every expression,
            1. if type == 'class_property' put in properties array
            2. if type == 'class_special_method' put in class special functions array
            3. if type == 'function' put in class methods array
            """
            if e["type"] == "var" or e["type"] == "assign":
                ret["class_properties"].append(e)
            elif e["type"] == "class_special_method":
                ret["class_special_methods"].append(e)
            elif e["type"] == "function":
                ret["class_methods"].append(e)

        return ret

    def parse_modulename():
        name = input.next()
        if name["type"] != "var":
            input.croak("Expecting variable name")
        return {"type": "module", "value": name["value"]}

    def parse_import():
        """
        should see an import statement and get the name of the imported
        module and return it. That's all for now...
        """
        skip_kw("import")

        return {
        "type": "import",
        "module": parse_modulename()
        }

    def parse_return():
        """
        should see an import statement and get the name of the imported
        module and return it. That's all for now...
        """
        skip_kw("return")

        return {
        "type": "return",
        "expression": parse_expression()
        }

    def parse_classprop():
        """
        reads 'has prop_name'
        """
        skip_kw("has")

        ret = {
            "type": "class_property"
        }

        # get the name or expression...
        p = maybe_binary(parse_atom(), 0)

        # if its somn like 'has age = 1'
        if p["type"] == "assign":
            # ret["value"] = p["left"]["value"]
            # ret["default_value"] = p["right"]["value"]
            ret = {**ret, **p}
        elif p["type"] == "var":
            ret = {**ret, **p}
        # TODO: maybe throw an error here...

        return p


    def parse_bool():
        return {"type": "bool", "value": input.next()["value"] == "True"}

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
            # parse lists here...
            if is_punc("["):
                return parse_list()
            if is_kw("if"):
                return parse_if()
            if is_kw("while"):
                return parse_while()
            if is_kw("for"):
                return parse_forloop()
            if is_kw("class"):
                return parse_class()
            if is_kw("import"):
                return parse_import()
            if is_kw("return"):
                return parse_return()
            if is_kw("has"):
                return parse_classprop()
            if is_kw("True") or is_kw("False"):
                return parse_bool()
            if is_kw("def"):
                return parse_function()

            # NOTE: If you don't handle tokens they will raise an error

            tok = input.next()

            if (tok["type"] == "var") or (tok["type"] == "num") or (tok["type"]
                                                                    == "str"):
                return tok

            unexpected()

        return maybe_call(doer)

    def parse_list():
        # TODO: I need to work on this for Python! Thank you Jesus!
        elems = delimited("[", "]", ",", parse_atom)
        return {"type": "list", "elements": elems}

    def parse_prog():
        # TODO: I need to work on this for Python! Thank you Jesus!
        prog = delimited("{", "}", ";", parse_expression)
        if len(prog) == 0:
            # return FALSE # TODO: maybe just return pass;
            return PASS
        if len(prog) == 1:
            return prog[0]
        return {"type": "prog", "prog": prog}

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
    #           if (20 > 10) {
    #               print('Greater!');
    #           if (True) {
    #           print('bbs')
    # }
    #           } else {
    #               print('Smaller!');
    #           };
    #       """
    code = """
       class Cow {
        has name;
        has color = "green";
       }
    """
    inputs = InputStream(code)
    tokens = TokenStream(inputs)
    ast = parse(tokens)

    print(ast)
