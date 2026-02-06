# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet is about import and scopes.

Teaching focus
  - import
"""

import pathlib
from platform import python_version


def non_dunder_names(dct):
    return [name for name in dct if not name.startswith('__')]


_filename = pathlib.Path(__file__).stem                 # '_' means 'internal use'

print(f" 1| start of '{_filename}', {__name__=}")

print(f" 2| before import, globals={non_dunder_names(globals())}")

import b_the_module as calc_module                      # known: calc_module.add1, calc_module.one
print(f" 3| after import module, globals={non_dunder_names(globals())}")

from b_the_module import add1                           # known: add1
print(f" 4| after import add1, globals={non_dunder_names(globals())}\n"
      f"    ids {id(add1)=}, {id(calc_module.add1)=}")

# print([it for it in calc_module.__dict__ if "three" in it])  # all vars exist, even __three, just filtered
print(f" 5| calc_module.globals={non_dunder_names(calc_module.__dict__)}")

four = add1(calc_module.one) + calc_module._two         # access protected member, but with a warning

print(f" 6| four={four}")

if __name__ == "__main__":
    print(f" 7| main start of '{_filename}' (python {python_version()})")
