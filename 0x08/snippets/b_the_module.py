# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

""" This is a module description. Pay attention to the tooltip at the import command. """

import pathlib

_filename = pathlib.Path(__file__).stem     # internal
one = 1                                     # public/visible to importer
_two = 2                                    # internal
__three = 3                                 # private


def add1(x):                                # visible
    return x+1


print(f"M1| start of '{_filename}', __name__='{__name__}'")

if __name__ == "__main__":                  # can be run independently
    print(f"M2| main start of '{_filename}'")
