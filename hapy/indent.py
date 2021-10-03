""" indent this blessed thing """
"""
Take a string of code and for each newline, check if it's the beginning of a block
, if so strip line and add indent then increase indent level, if you meet an ext }
, reduce indent level...

indent function taken from Bython package https://github.com/mathialo/bython
"""
import re


def indent(code: str) -> str:
    indentation_level = 0
    indentation_sign = "    "

    # Read file to string
    infile_str_raw = ""
    for line in code:
        infile_str_raw += line

    # Add 'pass' where there is only a {}.
    #
    # DEPRECATED FOR NOW. This way of doing
    # it is causing a lot of problems with {} in comments. The feature is removed
    # until I find another way to do it.

    # infile_str_raw = re.sub(r"{[\s\n\r]*}", "{\npass\n}", infile_str_raw)

    # Fix indentation
    infile_str_indented = ""
    for line in infile_str_raw.split("\n"):
        # Search for comments, and remove for now. Re-add them before writing to
        # result string
        m = re.search(r"[ \t]*(#.*$)", line)

        # Make sure # sign is not inside quotations. Delete match object if it is
        if m is not None:
            m2 = re.search(r"[\"'].*#.*[\"']", m.group(0))
            if m2 is not None:
                m = None

        if m is not None:
            add_comment = m.group(0)
            line = re.sub(r"[ \t]*(#.*$)", "", line)
        else:
            add_comment = ""

        # skip empty lines:
        if line.strip() in ('\n', '\r\n', ''):
            infile_str_indented += indentation_level * indentation_sign + add_comment.lstrip(
            ) + "\n"
            continue

        # remove existing whitespace:
        line = line.lstrip()

        # Check for reduced indent level
        for i in list(line):
            if i == "}":
                indentation_level -= 1

        # Add indentation
        for i in range(indentation_level):
            line = indentation_sign + line

        # Check for increased indentation
        for i in list(line):
            if i == "{":
                indentation_level += 1

        # print(line)
        # print(indentation_level)

        # Replace { with : and remove }
        # So this makes {} even in strings disapper. We have to fix that.
        line = re.sub(r"[\t ]*{[ \t]*", ":", line)
        line = re.sub(r"}[ \t]*", "", line)
        line = re.sub(r"\n:", ":", line)

        infile_str_indented += line + add_comment + "\n"

    # Support for extra, non-brace related stuff
    infile_str_indented = re.sub(r"else\s+if", "elif", infile_str_indented)
    infile_str_indented = re.sub(r";\n", "\n", infile_str_indented)

    # # Change imported names if necessary
    # if change_imports is not None:
    #     for module in change_imports:
    #         infile_str_indented = re.sub("(?<=import\\s){}".format(module),
    # "{} as {}".format(change_imports[module], module), infile_str_indented)
    #         infile_str_indented = re.sub("(?<=from\\s){}(?=\\s+import)".format(module), change_imports[module], infile_str_indented)

    # outfile.write(infile_str_indented)
    return infile_str_indented


if __name__ == '__main__':
    #     code = """
    #     if (n < 5) {
    #     print("Printed ", n);
    #     n = n + 1;
    #     print("inside if => ", n);
    #   if (n == 1) {
    #   print('N is one!')
    #   } else {
    #         print('N is not one!')
    #     }
    # };
    #            """

    #     code = """
    #    if (n < 5){
    # print("Printed ", n);
    # n = n + 1;
    # print("inside if => ", n);
    # if (n == 1){
    # print("N is one!")}
    # else {
    # print("N is not one!")}}
    #     """
    code = """
    if (True) {
    print(2);
    }
    """
    print(repr(indent(code)))

    # n = 0;
    # if (n < 5):
    #     print("Printed ", n)
    #     n = n + 1
    #     print("inside if => ", n)
    #     if (n == 1):
    #         print('N is one!')
    #     else:
    #         print('N is not one!')