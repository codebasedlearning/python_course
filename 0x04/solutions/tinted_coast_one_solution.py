# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This is a simple 'pythonic' example solution for the task 'Tinted Coast'.
"""

from pathlib import Path
import time
import textwrap

def solve_part1(lines):
    """ solve part 1 """

    def extract_digits(line):
        digits = [c for c in line if c.isdigit()]
        return int(digits[0] + digits[-1]) if digits else 0

    return sum([extract_digits(line) for line in lines])
    # return sum(extract_digits(line) for line in lines)

def solve_part2(lines):
    """ solve part 2 """

    words = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    # some like this: words = "zero one two three four five six seven eight nine".split()
    word_to_digit = {w: str(i) for i, w in enumerate(words)}

    def digit_at(line, i):
        c = line[i]
        if c.isdigit():
            return c
        for word, digit in word_to_digit.items():
            if line.startswith(word, i):
                return digit
        return None

    def extract_digits(line):
        digits = [d for i in range(len(line)) if (d := digit_at(line, i))]
        return int(digits[0] + digits[-1]) if digits else 0

    return sum(extract_digits(line) for line in lines)


# if you struggle with finding the data path...
#   import os
#   print(f"current working directory is: {os.getcwd()}")

data_path = "../data"
puzzle = "tinted_coast"

def input_data(config) -> tuple[list[str], int, int]:
    """ provide input data """

    # (path or test string, part, solution)
    all_configs: dict[str,tuple[str|Path,int,int]] = {
        'e1': (Path(f"./{data_path}/{puzzle}_example1.txt"), 1, 222),   # example 1
        'i1': (Path(f"./{data_path}/{puzzle}_input.txt"), 1, 44161),    # long input, part 1
        'e2': (Path(f"./{data_path}/{puzzle}_example2.txt"), 2, 61),    # example 2
        'i2': (Path(f"./{data_path}/{puzzle}_input.txt"), 2, 51119),    # long input, part 2
        't1': ( """
                abcde
                1xy2
                x34y
                x5y
                6
                """, 1, 167),   # test case 1
        't2': ( """
                x1y2
                twone2oneight
                """, 2, 40)     # test case 2
    }

    current_config = all_configs[config]
    return (
        (textwrap.dedent(current_config[0]) if isinstance(current_config[0], str) else current_config[0].read_text())
            .strip().splitlines(),
        current_config[1],
        current_config[2]
    )

def solve_puzzle():
    """ solve the puzzle """
    print("\nsolve_puzzle\n============")

    config = 'i1'
    lines, part, expected = input_data(config)
    print(f" 1| {puzzle=}, {config=}, {part=}, {expected=}")

    start_time = time.time()
    solution = solve_part1(lines) if part == 1 else solve_part2(lines)
    elapsed_time = time.time() - start_time
    print(f" 2| {solution=} in {int(elapsed_time*1e3)} ms"
          f"\n=====> {'OK' if solution == expected else 'NOT OK'}")

if __name__ == '__main__':
    solve_puzzle()
