# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet provides a simple pattern to tackle the tasks.

Teaching focus
  - get data, transform data, process data
"""

from pathlib import Path
import time
import re
import textwrap


# if you struggle with finding the data path...
#   import os
#   print(f"current working directory is: {os.getcwd()}")

def solve_problem():
    """ read data, transform data, process data """
    print("\nprocess_file\n============")

    # test examples (choose 'source', all read for simplicity)
    day = 0
    data_path = "./data"
    examples = [
        Path(f"{data_path}/day{day:02}_input.txt").read_text(),     # source = 0
        Path(f"{data_path}/day{day:02}_example1.txt").read_text(),  # = 1, ...
        """
        line 11
        line 12
        line 13
        line 14
        line 15
        """,
        """
        line 21
        line 22
        line 23
        line 24
        line 25
        """,
    ]

    # real data from file (here 0,1) or small examples from above (here >1)
    source = 0
    # input data as one text block according to 'source';
    # 'dedent' removes the leading whitespaces (from examples)
    input_block = textwrap.dedent(examples[source]).strip()
    print(f" 1| {input_block=}")

    # if data is given in lines, split the block
    input_lines = input_block.splitlines()
    print(f" 2| {input_lines=}")

    # from here, 'input_lines' is our master text input; usually, we need to transform it
    # into data structures we can better work with

    # example, how to process or map those lines with split;
    # note, in the list comprehension we use the expansive part 'line.split' only once
    process_data1 = [
        (words[0].strip(), int(words[1].strip()) + 1)
        for line in input_lines if (words := line.split(' '))           # walrus + condition
    ]
    print(f" 3| {process_data1=}")

    # or use regular expressions (w.o. explanation), here with grouping (word and number);
    # note, in the list comprehension we use the expansive part 're.search' only once
    # and use the fact that it returns 'None' (=False) if the line does not match
    # btw., designing a regex according to a pattern is a good task for generative AI, just
    # feed it with what you have (line example) and what you need (group of text and int)
    pattern = r"(\w+)\s+(\d+)"
    process_data2 = [
        (match.group(1), int(match.group(2)) + 2)
        for line in input_lines if (match := re.search(pattern, line))  # walrus + condition
    ]
    print(f" 4| {process_data2=}\n")

    # part 1

    start_time = time.time()
    # solve it
    time.sleep(0.2)
    solution_part1 = sum(value for _, value in process_data1)   # in fact, this is a generator...
    elapsed_time = time.time() - start_time
    print(f" 5| part 1, sum: {solution_part1}, time to load: {int(elapsed_time*1e3)} ms")

    # part 2

    start_time = time.time()
    # solve it
    time.sleep(0.3)
    solution_part2 = sum(value for _, value in process_data2)
    elapsed_time = time.time() - start_time
    print(f" 6| part 2, sum: {solution_part2}, time to load: {int(elapsed_time*1e3)} ms")


if __name__ == '__main__':
    solve_problem()
