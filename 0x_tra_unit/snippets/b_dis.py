# (C) A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet is about Python's disassembler (dis).

Teaching focus
  - dis

Summary
  Efficiency Comparison:
  1. ``dict(a=20)`` calls the function and requires extra LOAD and CALL steps
     (LOAD_GLOBAL, LOAD_CONST, CALL_KW), adding slight function call overhead.
     It is slower than a literal.
  2. ``{'b': 22}`` uses BUILD_MAP, LOAD_CONST, and STORE_FAST to directly create
     the dictionary. It is faster and more efficient because of fewer steps and
     no function call overhead.

References
  - https://docs.python.org/3/library/dis.html
  - https://florian-dahlitz.de/articles/disassemble-your-python-code
"""

import dis

from utils import print_function_header


def dicts():
    d1 = dict(a=20)                         # What is better?
    d2 = {'b': 22}
    return d1['a'] + d2['b']

@print_function_header
def use_bytecode():
    """ ... """

    print(f" 1| bytecode 'dicts'")
    bytecode = dis.Bytecode(dicts)
    print(dis.code_info(dicts))
    print(f" 2| eval bytecode: {eval(bytecode.codeobj)}")


@print_function_header
def analyse_bytecode():
    """ ... """

    print(f" 1| dis 'dicts'")
    dis.dis(dicts)


if __name__ == "__main__":
    use_bytecode()
    analyse_bytecode()
