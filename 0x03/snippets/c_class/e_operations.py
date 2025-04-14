# (C) 2025 Alexander Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet discusses some functions from the data model.

Teaching focus
  - What do we need to implement a dictionary-like class with logging?
  - Focus on element access.
"""


class LoggingDict:
    """ the logging dict class """

    def __init__(self):                                         # skip all other ways to initialize
        self.log_dict = {}

    def __getitem__(self, key):
        print(f" a|   getitem, key={key}")
        return self.log_dict[key]

    def __setitem__(self, key, value):      # also __delitem__
        print(f" b|   setitem, key={key}, value={value}")
        self.log_dict[key] = value

    def __delitem__(self, key):
        print(f" c|   delitem, key={key}")
        del self.log_dict[key]

    def __len__(self):
        print(" d|   len")
        return self.log_dict.__len__()

    def __iter__(self):
        return iter(self.log_dict)

    def __contains__(self, key):
        print(" f|   in")
        return key in self.log_dict

    def __repr__(self):
        return f"({self.log_dict})"

    def items(self):                        # same for keys(), values()
        """ forward items """
        return self.log_dict.items()

    def get(self, key, default=None):
        """ forward get """
        return self.log_dict.get(key, default)


def test_logging_dicts():
    """ test our class """
    print("\ntest_logging_dicts\n==================")

    ld = LoggingDict()
    print(f" 1| {ld=}")

    ld[1] = "one"
    ld["two"] = 2
    ld[(1,2)] = 3
    print(f" 2| ld={ld}, len={len(ld)}, {ld[1]=}, {ld.get(2,-1)=}")

    print(f" 3| {1 in ld=}, {2 in ld=}")

    del ld[(1,2)]
    print(f" 4| ld={ld}")

    print(" 5| keys:", end='')
    for key in ld.log_dict:                 # same as keys()
        print(f" {key=}", end='')
    print()

    print(" 6| keys:", end='')
    for key in ld:                          # calls __iter__
        print(f" {key=}", end='')
    print()

    print(" 7| items:", end='')
    for k, v in ld.items():
        print(f" ({k},{v})", end='')
    print()

    print(" 8| enumerate:", end='')
    for i, item in enumerate(ld.items()):   # no, item
        print(f" {i}|{item}", end='')
    print()


if __name__ == "__main__":
    test_logging_dicts()


###############################################################################


"""
Summary

Topics
  - __getitem__, __setitem__, __delitem__
  - __len__, __iter__
  - __contains__

Operations
  - Python allows you to define special functions for index access, deletion
    etc. These are __getitem__, __setitem__, __delitem__, __contains__.
  - Moreover, we additionally can define an iterator by implementing __iter__.
    This will be discussed in a later unit.
   
See also 
    https://docs.python.org/3/reference/datamodel.html
"""
