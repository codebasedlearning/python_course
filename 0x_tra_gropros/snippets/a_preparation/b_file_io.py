# (C) 2025 Alexander Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet discusses basic file io.

Teaching focus
  - file read, write

There are
- `PurePath`: Pure path manipulation, no I/O operations
- `Path`: Includes I/O operations (inherits from `PurePath`)

Best practice
- Always use forward slashes () in your code `/`
- Let handle the platform-specific conversions `pathlib`
- This makes your code more portable between operating systems
"""

import os
from pathlib import Path

from utils import print_function_header

@print_function_header
def show_io_stats():
    """ show io stats """
    filename = "./data/data9.in"
    dirname = "."

    is_file = os.path.isfile(filename)
    print(f" 1| file '{filename}'? {is_file}")

    is_dir = os.path.isdir(dirname)
    print(f" 2| dir '{dirname}'? {is_dir}")

    files_in_dir = [os.path.join(dirname, f) for f in os.listdir(dirname) if f.endswith(".py")]
    print(f" 3| '*py'-files in dir? {files_in_dir}")


@print_function_header
def show_file_io():
    """ show file io """
    filename = "./data/data9.in"

    print(" 1| content")
    with open(filename, 'r') as file:       # 'with' calls close and closes the file; default utf8
        for line in file:
            print(f" a| {line=}")

    # writing, do not forget '\n'
    # with open(filename.replace(".in", ".out"), 'w') as file:
    #     file.write(f"# comment\n")
    #     file.write(f"data...\n")


@print_function_header
def show_path_io():
    """ show file io with Path """
    filename = "./data/data9.in"
    lines = Path(filename).read_text().splitlines()
    print(f" 1| {lines=}")

    # write with 'write_text'
    #   Path(filename.replace(".in", ".out")).write_text("# comment\ndata...\n")
    # or with 'open' and 'append' mode
    #   with Path(filename.replace(".in", ".out")).open("a") as f:
    #     f.write("Another line\n")


if __name__ == "__main__":
    show_io_stats()
    show_file_io()
    show_path_io()
