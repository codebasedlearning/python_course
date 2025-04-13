# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet provides some code snippets for later.

Teaching focus
  - ...
"""

from pathlib import Path
import time
import re


FILE_PATH = '../exercises/data/example.txt'

def read_file_content(file_path: Path) -> str:
    """ read file content and strip whitespace """
    return file_path.read_text().strip()


def read_all_lines(file_path: Path) -> [str]:
    """ read content and split it into lines """
    return read_file_content(file_path).splitlines()


def process_file(file_path: str = FILE_PATH):
    """ read file and work with it """
    print("\nprocess_file\n============")

    filename = Path(file_path)
    print(f" 1| {filename=}")

    block = read_file_content(filename)
    print(f" 2| {block=}")

    lines = read_all_lines(filename)
    print(f" 3| {lines=}")

    # example how to process or map those lines with split
    numbers = [ int(line.split(' ')[1])+10 for line in lines]   # sometimes regex
    print(f" 4| {numbers=}")

    pattern = r"(\w+)\s+(\d+)"
    results = [
        (match.group(1), int(match.group(2))+100)
        for line in lines
        if (match := re.search(pattern, line))
    ]
    print(f" 5| {results=}")


def measure_time():
    print("\nmeasure_time\n============")

    start_time = time.time()
    sum_range = 0
    for i in range(10000000):
        sum_range += i
    elapsed_time = time.time() - start_time
    print(f"sum: {sum_range}, time to load: {int(elapsed_time*1e3)} ms")


def using_iterators():
    print("\nusing_iterators\n===============")

    chars = ['A', 'B', 'C']
    for i, c in enumerate(chars, 1):        # start optional, def. is 0
        print(f"- pos {i} -> '{c}'")


if __name__ == '__main__':
    process_file()
    measure_time()
    using_iterators()
