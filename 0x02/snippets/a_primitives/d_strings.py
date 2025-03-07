# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet discusses strings and string operations.

Teaching focus
  - It is structured like the int-snippet, i.e. first some conversions and
    basic operations, then some special stuff.
  - Common operations, slicing, indexing, split.
  - Bonus: String representation with encoding and decoding.
"""

import textwrap


def using_strings():
    """ string basics """
    print("\nusing_strings\n=============")

    s = "Hello Python!"                                         # a string
    # s: str = "Hello Python!"                                  # with type hint
    print(f" 1| {s=}, {len(s)=}, {type(s)=}")

    print(f" 2| {str(12)=}, {str(34.8)}, {str(True)=}, {str(None)=}")


def common_string_ops():
    """ common string operations """
    print("\ncommon_string_ops\n=================")

    s = "  Simple Text  "
    print(f" 1| {s=}, {len(s)=}")
    print(f" 2| {s.upper()=}, {s.lower()=}")
    print(f" 3| {s.strip()=}, {s.replace('e', '3')=}")
    print(f" 4| {('Tex' in s)=}")


def using_slicing():
    """ string slicing and indexing """
    print("\nusing_slicing\n=============")

    s = "0123456789abcdefghij"
    print(f" 1| {s=}, {len(s)=}")
    print(f" 2| {s[2]=}")                                       # a single character
    print(f" 3| {s[-3]=}")                                      # char at end-pos=length-3
    print(f" 4| {s[2:4]=}")                                     # start- (incl.), end-pos (excl.)
    print(f" 5| {s[:4]=}")                                      # start=0, end-pos (excl.)
    print(f" 6| {s[4:]=}")                                      # start=4, end-pos=length
    print(f" 7| {s[-4:-2]=}")                                   # start=length-4, end-pos=length-2
    print(f" 8| {s[-1:]=}")                                     # start=length-1, end-pos=length
    print(f" 9| {s[3:-2]=}")                                    # start=3, end-pos=-2
    print(f"10| {s[::2]=}")                                     # start=0, end-pos=length, step=2


def using_split():
    """ string splitting """
    print("\nusing_split\n===========")

    s = "Lorem ipsum dolor sit amet"
    print(f" 1| {s=}, {len(s)=}")
    words = s.split()                                           # result is list
    print(f" 2| {words=}, {len(words)=}, {type(words)=}")

    data = """
    Lorem ipsum dolor sit amet, consectetur adipiscing elit, 
    sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. 
      - Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris 
        nisi ut aliquip ex ea commodo consequat. 
    """
    lines = data.split('\n')
    print(f" 3| {lines=}")                                      # not optimal, first line empty, too much indent

    with_indents = textwrap.dedent(data).lstrip().split('\n')   # leading indent gone, inner indent is preserved
    print(f" 4| {with_indents=}")


def string_representation():
    """ string representation """
    print("\nstring_representation\n=====================")

    smile = "smile 😀"                                           # Python 3 uses Unicode to represent strings
    print(f" 1| {smile=}")

    smile_utf8_bytes = smile.encode("utf-8")                    # encode to utf-8
    print(f" 2| {smile_utf8_bytes=}, {type(smile_utf8_bytes)=}")

    smile_str = smile_utf8_bytes.decode("utf-8")                # decode back to string
    print(f" 3| {smile_str=}, {type(smile_str)=}")


if __name__ == "__main__":
    using_strings()
    common_string_ops()
    using_slicing()
    using_split()
    string_representation()


###############################################################################


"""
Summary

Topics
  - strings
  - string operations
  - string slicing and indexing
  - string splitting
  - string representation
  - encoding, decoding

Strings
  - Surprisingly, you can define strings, but also comments, with ''
    instead of "". The choice is free and there is no recommendation.
    Some use "" for strings and '' for regular expressions or keys.
  - There are, of course, countless string operations. It is important to know
    that strings are immutable, i.e. all operations such as '+=', 'replace',
    'upper' etc. always return a new string.

See also
  - https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str
  - https://www.w3schools.com/python/python_strings_methods.asp
"""
