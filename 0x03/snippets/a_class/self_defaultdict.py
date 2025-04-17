# (C) 2025 Alexander Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet discusses the defaultdict class from the collections module.
"""

from collections import defaultdict


def using_defaultdict():
    """ test the defaultdict class """
    print("\nusing_defaultdict\n=================")

    frequency:defaultdict = defaultdict(int)    # defaultdict with int (default value is 0)

    # count words; note that a missing key automatically generates a (key,0) entry
    words = ['apple', 'banana', 'apple', 'orange', 'banana', 'apple']
    for word in words:
        frequency[word] += 1
    print(f" 1| {frequency=}")


if __name__ == "__main__":
    using_defaultdict()


###############################################################################


"""
Summary
  - A `defaultdict` is a subclass of Python's built-in `dict` that provides 
    a convenient way to handle missing keys by automatically supplying 
    a default value for those keys.
  - Normally, if you try to access a key in a regular dictionary that doesn’t 
    exist, Python raises a `KeyError`. With a `defaultdict`, however, 
    it automatically creates a default value for the missing key using 
    a function (called a `default_factory`) that you specify when creating 
    the `defaultdict`.

See also
  - https://docs.python.org/3/library/collections.html#collections.defaultdict
"""
