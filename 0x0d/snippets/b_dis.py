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

"""
13           RESUME                   0                     - Python 3.11+ and simply initializes the bytecode evaluation.

 14           LOAD_GLOBAL              1 (dict + NULL)      1. Loads the global function into memory `dict`; - without additional positional arguments
              LOAD_CONST               1 (20)               1. Loads constants onto the stack
              LOAD_CONST               2 (('a',))           1. loads the tuple
              CALL_KW                  1                    1. Calls the `dict()` function, passing as the keyword argument `a=20`
              STORE_FAST               0 (d1)               1. Stores the resulting dictionary `{ 'a': 20 }` in the local variable . `d1`

 15           LOAD_CONST               3 ('b')              1. Loads the constant, key, value
              LOAD_CONST               4 (22)
              BUILD_MAP                1                    1. creates a dictionary with space for exactly 1 key-value pair
              STORE_FAST               1 (d2)               1. Stores the resulting dictionar

### Efficiency Comparison:
1. **`dict(a=20)`**:
    - Calls the function and requires extra LOAD and CALL steps (`LOAD_GLOBAL`, `LOAD_CONST`, `CALL_KW`), adding slight function call overhead. `dict`
    - It's **slower** than a literal.

2. **`{'b': 22}`**:
    - Uses `BUILD_MAP`, `LOAD_CONST`, and `STORE_FAST` to directly create the dictionary.
    - It's **faster and more efficient** because of fewer steps and no function call overhead.

"""

if __name__ == "__main__":
    use_bytecode()
    analyse_bytecode()


"""
https://docs.python.org/3/library/dis.html
https://florian-dahlitz.de/articles/disassemble-your-python-code
"""
