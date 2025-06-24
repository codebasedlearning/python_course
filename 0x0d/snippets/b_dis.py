# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet is about pythons disassembler (dis).

Teaching focus
  - dis
"""

import dis


def dicts():
    d1 = dict(a=20)                         # What is better?
    d2 = {'b': 22}
    return d1['a'] + d2['b']

def use_bytecode():
    """ ... """
    print("\nuse_bytecode\n============")

    print(f" 1| bytecode 'dicts'")
    bytecode = dis.Bytecode(dicts)
    print(dis.code_info(dicts))
    print(f" 2| eval bytecode: {eval(bytecode.codeobj)}")


def analyse_bytecode():
    """ ... """
    print("\nanalyse_bytecode\n================")

    print(f" 1| dis 'dicts'")
    dis.dis(dicts)


if __name__ == "__main__":
    use_bytecode()
    analyse_bytecode()


"""
https://docs.python.org/3/library/dis.html
https://florian-dahlitz.de/articles/disassemble-your-python-code
"""
