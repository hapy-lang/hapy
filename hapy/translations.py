
kws_source = {
    "in": "if",
    "kokuma": "elif",
    "then": "then",
    "indai": "while",
    "ma": "for",
    # "na": "for", # for now we can only use one
    "karo": "import",
    "iri": "class",
    "yanada": "has",
    # "gado": "inherits",
    "gada": "inherits",
    "anfani": "use",
    # "amfani": "use",
    "wuce": "pass",
    "daga": "from",
    "imbahakaba": "else",
    "cikin": "in",
    "Babu": "None",
    "dawo": "return",
    "aiki": "def",
    "Gaskiya": "True",
    "Karya": "False",
    # TODO: translate these!

}

ops_source = {
    "ba": "not",
    "da": "and",
    "ko": "or",
    "shine": "is",
    "cikin": "in",
    "of": "of",
    "ba cikin": "not in",
    "is equal": "is equal",
    "is not equal": "is not equal",
    "times": "times",
    "hada": "plus",
    "raba": "dividedby",
    "chire": "minus"
}

# TODO: add functions here!
builtin_funcs = {
    "when_created": "when_created",
    "when_printed": "when_printed",
    "when_string": "when_string",
    "printo": "print"
}

keywords = {

}

operator_words = {

}

builtin_functions = {

}

def makeTranslationDicts():
    """make translation dictionaries

    creates dictionaries we need mapping words
    to their translation in both languages

    dict = {
        hausa = {
            stuff...
        },

        eng = {
            stuff...
        }
    }
    """


    # TODO: make all this a dynamic loop!

    keywords["hausa"] = dict((v,k) for k,v in kws_source.items())
    keywords["eng"] = dict((v,v) for k,v in kws_source.items())

    # operator words
    operator_words["hausa"] = dict((v,k) for k,v in ops_source.items())
    operator_words["eng"] = dict((v,v) for k,v in ops_source.items())

    # builtin_functions TEMPORARY!
    builtin_functions["hausa"] = dict((v,k) for k,v in builtin_funcs.items())
    builtin_functions["eng"] = dict((v,v) for k,v in builtin_funcs.items())


makeTranslationDicts()
