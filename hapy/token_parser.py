"""
parser
from: https://lisperator.net/pltut/parser/the-parser
"""
import json
from .token_stream import TokenStream
from .input_stream import InputStream
from .translations import keywords, operator_words, builtin_functions

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
        "=": 1,
        ":": 1,
        operator_words[input.settings["lang"]]["is"]: 1,
        operator_words[input.settings["lang"]]["or"]: 2,
        operator_words[input.settings["lang"]]["and"]: 3,
        "<": 7,
        ">": 7,
        "<=": 7,
        ">=": 7,
        "==": 7,
        "!=": 7,
        operator_words[input.settings["lang"]]["not"]: 7,
        "+": 10,
        "-": 10,
        operator_words[input.settings["lang"]]["plus"]: 10,
        operator_words[input.settings["lang"]]["minus"]: 10,
        "*": 20,
        "/": 20,
        "%": 20,
        operator_words[input.settings["lang"]]["times"]: 20,
        operator_words[input.settings["lang"]]["dividedby"]: 20,
        # because self.name is one of the strongest bonds
        operator_words[input.settings["lang"]]["in"]: 20,
        ".": 30,
    }
    expecting_non_dict_block = False

    # the program first level! thank you Jesus!

    def block_kw(operation: str):
        nonlocal expecting_non_dict_block
        if operation.lower() == "get":
            return expecting_non_dict_block
        elif operation.lower() == "set":
            expecting_non_dict_block = True

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
            input.croak(f"Expecting operator got: \"{op}\"")

    def unexpected(msg="unexpected token: %s "):
        input.croak(msg % json.dumps(input.peek()))

    def maybe_binary(left, my_prec):
        tok = is_op(None)  # thank you Jesus :]
        # tbh, I'm not 100% sure what's going on here, but I'll find out!
        binary_type = {  # noqa: F841
            operator_words[input.settings["lang"]]["is"]: "assign",
            "=": "assign",
            ".": "access",
            operator_words[input.settings["lang"]]["in"]: "membership",
            ":": "dict-elem"  # Wuta added this line.
        }
        if tok:
            their_prec = PRECEDENCE[tok["value"]]
            if their_prec > my_prec:
                input.next()

                return maybe_binary(
                    {
                        "type":
                        binary_type.get(tok["value"], "binary"),
                        "operator":
                        tok["value"],
                        "left" if tok["value"] != ":" else "key":
                        left,
                        "right" if tok["value"] != ":" else "value":
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
        """sumary_line

        Keyword arguments:
        argument -- description
        Return: return_description
        """

        block_kw("set")
        skip_kw(keywords[input.settings["lang"]]["if"])
        cond = parse_expression()
        # if (!is_punc("{")) skip_kw("then"); REASON: no then in python :]
        # sha, I can add it tho...
        then = parse_expression()
        ret = {"type": "if", "cond": cond, "then": then}

        ret["elifs"] = []

        while is_kw(keywords[input.settings["lang"]]["elif"]):
            block_kw("set")
            skip_kw(keywords[input.settings["lang"]]["elif"])
            elif_cond = parse_expression()
            elif_then = parse_expression()
            elif_tok = {"type": "elif", "cond": elif_cond, "then": elif_then}
            ret["elifs"].append(elif_tok)

        if is_kw(keywords[input.settings["lang"]]["else"]):
            block_kw("set")
            # TODO: this should be skip_kw("else") :)
            # but I'm afraid it might cause problems :(

            input.next()
            ret["else"] = parse_expression()

        # TODO: look into `else_if/elif`
        # if is_kw("else_if"):
        #   input.next()
        #   ret["else"] = parse_expression()

        return ret

    def parse_while():
        """ parse while"""
        block_kw("set")

        '''Thank you Jesus!!!
        Basically this creates a block of code. However a dictionary sysntax is quite similar "{}".
        So once it sees a block, it should set expecting_non_dict_block to True and the next '{}' is called as a block.

        Lean khan I have done it!!!!!
        '''
        block_kw("set")

        skip_kw(keywords[input.settings["lang"]]["while"])

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
        block_kw("set")

        skip_kw(keywords[input.settings["lang"]]["for"])

        header = parse_expression()  # the iterator...

        body = parse_expression()

        ret = {"type": "for", "header": header, "body": body}

        return ret

    def parse_function():
        """stuff"""
        block_kw("set")

        skip_kw(keywords[input.settings["lang"]]["def"])

        function_name = parse_varname()

        ret = {"name": function_name}

        class_special_methods = [
            builtin_functions[input.settings["lang"]]["__startwith__"],
            builtin_functions[input.settings["lang"]]["__toshow__"],
            # builtin_functions[input.settings["lang"]]["__string__"]
        ]

        if function_name["value"] in class_special_methods:
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

        skip_kw(keywords[input.settings["lang"]]["class"])

        # next, get the class name
        classname = parse_varname()

        ret = {"type": "class", "name": classname}

        # if the next token is 'inherits' then get parent class name!...
        # thank you Jesus!
        if is_kw(keywords[input.settings["lang"]]["inherits"]):
            skip_kw(keywords[input.settings["lang"]]["inherits"])
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
            # this is to initialize the parent class
            elif e["type"] == "use_class":
                ret["init_parent"] = e
                # make sure classes are the same!
                if ret["init_parent"]["func"]["value"] != ret["inherits"][
                        "value"]:
                    input.croak("Parent class not initialized!")

        return ret

    def parse_modulename():
        name = input.next()
        if name["type"] != "var":
            input.croak("Expecting module name")
        return {"type": "module", "value": name["value"]}

    def parse_import():
        """
        should see an import statement and get the name of the imported
        module and return it. That's all for now...
        """
        skip_kw(keywords[input.settings["lang"]]["import"])

        return {"type": "import", "module": parse_modulename()}

    def parse_return():
        """
        should see an import statement and get the name of the imported
        module and return it. That's all for now...
        """
        skip_kw(keywords[input.settings["lang"]]["return"])

        return {"type": "return", "expression": parse_expression()}

    def parse_class_use():
        """returns the attributes that this class uses"""

        skip_kw(keywords[input.settings["lang"]]["use"])

        d = parse_atom()

        d["type"] = "use_class"

        return d

    def parse_classprop():
        """
        reads 'has prop_name'
        """
        skip_kw(keywords[input.settings["lang"]]["has"])

        ret = {"type": "class_property"}

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
        return {"type": "bool", "value": input.next()["value"] == keywords[input.settings["lang"]]["True"]}

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
                if block_kw("get"):
                    return parse_prog()
                return parse_dict()
            # Python already has a 'dict' function,
            #  no need for us to reimplement the functionality.

            # if is_kw("dict"):
            #     input.next()
            #     skip_punc("(")
            #     exp = parse_dict()
            #     skip_punc(")")
            #     return exp
            # parse lists here...
            if is_punc("["):
                return parse_list()
            if is_kw(keywords[input.settings["lang"]]["if"]):
                return parse_if()
            if is_kw(keywords[input.settings["lang"]]["while"]):
                return parse_while()
            if is_kw(keywords[input.settings["lang"]]["for"]):
                return parse_forloop()
            if is_kw(keywords[input.settings["lang"]]["class"]):
                return parse_class()
            if is_kw(keywords[input.settings["lang"]]["import"]):
                return parse_import()
            if is_kw(keywords[input.settings["lang"]]["return"]):
                return parse_return()
            if is_kw(keywords[input.settings["lang"]]["has"]):
                return parse_classprop()
            if is_kw(keywords[input.settings["lang"]]["use"]):
                return parse_class_use()
            if is_kw(keywords[input.settings["lang"]]["True"]) or is_kw(keywords[input.settings["lang"]]["False"]):
                return parse_bool()
            if is_kw(keywords[input.settings["lang"]]["def"]):
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

    def parse_dict():
        # TODO: if a user types {1,2,3} we should handle it corretly,
        # tell them it's a syntax error!
        elem = delimited("{", "}", ",", parse_expression)
        return {"type": "dict", "content": elem}

    def parse_prog():
        nonlocal expecting_non_dict_block
        expecting_non_dict_block = False
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
        return {"type": "prog", "prog": prog, "settings": input.settings}

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
    # code = """name=45;
    #     def hello(name){
    #        print('Hello %s', 67)# % name)
    #     };

    #     hello();
    # """
    code = """
            #! lang=hausa
        in (Gaskiya) {
            print(2);
        }
         """
    inputs = InputStream(code)
    tokens = TokenStream(inputs)
    ast = parse(tokens)

    print(ast)
