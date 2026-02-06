# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet is about file io and the 'with' statement.

Teaching focus
  - file io
  - with
  - pathlib
"""

from pathlib import Path, PurePath

"""
What are the general issues with IO, especially file IO?
"""


def read_file_version1(filename):                                   # (A) file io
    """ read file version 1 """
    print("\nread_file_version1\n==================")

    # pro/con?
    print(f" 1| open '{filename}'")
    f = open(filename, "r")
    text = f.readlines()                                            # all lines, a max. number can be given
    print(f"    lines: {text}")
    f.close()


def read_file_version2(filename):
    """ read file version 2 """
    print("\nread_file_version2\n==================")

    # pro/con?
    file = None
    text = None
    try:
        print(f" 1| try to open '{filename}'")
        file = open(filename, "r")                                  # or 'open' before, i.e. try-except for 'read' only
        text = file.readlines()
    except OSError as e:
        print(f"    -> IO error: {e}")
    finally:
        if file:
            file.close()
    if text:
        print(f"    lines: {text}")


def read_file_version3(filename):
    """ read file version 3 """
    print("\nread_file_version3\n==================")

    # pro/con?
    text = None
    try:
        print(f" 1| try to open '{filename}'")
        with open(filename, "r") as reader:                         # (B) with
            text = reader.readlines()
        print(f"    reader closed? {reader.closed}")
    except OSError as e:
        print(f"    -> IO error: {e}")
    if text:
        print(f"    lines: {text}")


def read_file_version4(filename):
    """ read file version 4 """
    print("\nread_file_version4\n==================")

    # pro/con?
    try:
        print(f" 1| try to open '{filename}'")
        with open(filename, "r") as reader:
            line = reader.readline()
            print(f"    lines:", end='')
            while line:                                             # EOF is an empty string
                print(f" {line.__repr__()}", end='')
                line = reader.readline()
            print()
    except OSError as e:
        print(f"    -> IO error: {e}")


def change_to_filename_out(filename: str) -> str:                   # (C) pathlib
    """ change filenames """
    print("\nchange_to_filename_out\n======================")

    print(f" 1| manipulate '{filename}'")
    path = PurePath(filename)                                       # Path is PosixPath or WindowsPath
    path_abs = Path(path).absolute()
    print(f" 2| path: '{path}, type: {type(path)}'\n"
          f"    absolut: '{path_abs}'\n"
          f"    parts: {path_abs.parts}\n"
          f"    parent: {path_abs.parent}")

    out_folder = "."
    results_in = (path.parent / out_folder / path.name).with_suffix(".out")  # do not forget the '.'
    print(f" 3| path: '{results_in}'\n")
    return str(results_in)


def write_file(filename):
    """ change filenames """
    print("\nwrite_file\n==========")

    text = """# comment
14
A;B;C
D;E
-> Result: xyz
"""
    try:
        print(f" 1| try to write '{filename}'")
        with open(filename, 'w') as writer:
            writer.write(text)
        print(f"    try to read '{filename}'")

        path = Path(filename)
        with path.open("r") as reader:                              # open from pathlib
            print(f"    content: {reader.readlines()}")
    except OSError as e:
        print(f"    -> IO error: {e}")


if __name__ == "__main__":
    filename_r = "ihk_exam_sample.txt"
    read_file_version1(filename_r)
    read_file_version2(filename_r)
    read_file_version3(filename_r)
    read_file_version4(filename_r)
    filename_w = change_to_filename_out(filename_r)
    # write_file(filename_w)


"""
General IO issues that you must always keep in mind are these, for example:
  - platform dependency
    - (drive), path, filename, extension
    - path notions
    - line endings
    - file mode
    - permissions
  - character encodings

file io
  - The idea is always to consider not only the normal case, but also the 
    failure case (however unlikely). This does not have to come from the 
    system, it can come from the programmer.
    At its core is the management of resources, including those of the 
    operating system.
  - Here, any read error results in exceptions not closing the file, i.e. 
    leaving the file handle internally occupied.
    In other words, we have to make sure that the file is closed under 
    all circumstances, or in general terms, that the resources are returned.

More sources on that topic:
    https://docs.python.org/3/library/functions.html#open
    https://docs.python.org/3/tutorial/inputoutput.html#tut-files
    https://realpython.com/read-write-files-python/
    https://realpython.com/why-close-file-python/

with
From https://realpython.com/python-with-statement/
  - Managing resources properly is often a tricky problem. It requires 
    both a setup phase and a teardown phase.
  - In our case this is done by a ContextManager. This implements 
    functions '__enter__' and '__exit__' and will be presented in the 
    next example.

pathlib
  - Dealing with file paths is tedious. The 'pathlib' library provides 
    a 'PurePath' class that works platform-independently.
  - 'Path', on the other hand, is platform-specific, but can do more, 
    e.g. absolute paths.

From https://docs.python.org/3/library/pathlib.html
  - If you’ve never used this module before or just aren’t sure which class 
    is right for your task, Path is most likely what you need. It instantiates 
    a concrete path for the platform the code is running on.
  - Pure paths are useful in some special cases; for example:
      - If you want to manipulate Windows paths on a Unix machine (or vice versa). 
        You cannot instantiate a WindowsPath when running on Unix, but you can 
        instantiate PureWindowsPath.
      - You want to make sure that your code only manipulates paths without 
        actually accessing the OS. In this case, instantiating one of the 
        pure classes may be useful since those simply don’t have any 
        OS-accessing operations.

See
    https://docs.python.org/3/library/pathlib.html
    https://docs.python.org/3/library/os.path.html#os.path.split
"""
