# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This is a simple 'pythonic' example solution for the task 'Lonely Seafront'.
"""

from pathlib import Path
import time
import textwrap
from collections import defaultdict
from math import prod

def parse_game(line):
    """ parse a single game line into (game_id, list of round dicts) """
    def parse_round(a_round):
        cubes = defaultdict(int)
        for num, color in (block.strip().split() for block in a_round.strip().split(",")):
            cubes[color] += int(num)
        return cubes

    header, _, tail = line.partition(":")
    game_id = int(header.removeprefix("Game "))
    game_data = [parse_round(a_round) for a_round in tail.split(";")]
    return game_id, game_data

def solve_part1(lines):
    """ solve part 1 """
    def is_game_valid(game_data):
        max_cubes = {'red': 12, 'green': 13, 'blue': 14}  # max allowed cubes per color
        return all(num <= max_cubes[color] for round_data in game_data for color, num in round_data.items())

    return sum(game_id for line in lines for game_id, game_data in [parse_game(line)]
               if is_game_valid(game_data))

def solve_part2(lines):
    """ solve part 2 """
    def game_power(game_data):
        return prod(max(a_round.get(color, 0) for a_round in game_data) for color in ['red', 'green', 'blue'])

    return sum(game_power(parse_game(line)[1]) for line in lines)

# if you struggle with finding the data path...
#   import os
#   print(f"current working directory is: {os.getcwd()}")

data_path = "../data"
puzzle = "lonely_seafront"

def input_data(config) -> tuple[list[str], int, int]:
    """ provide input data """

    # (path or test string, part, solution)
    all_configs: dict[str,tuple[str|Path,int,int]] = {
        'e11': (Path(f"./{data_path}/{puzzle}_example1.txt"), 1, 3),    # example 1
        'i1': (Path(f"./{data_path}/{puzzle}_input.txt"), 1, 542),      # long input, part 1
        'e12': (Path(f"./{data_path}/{puzzle}_example1.txt"), 2, 5496), # example 1
        'i2': (Path(f"./{data_path}/{puzzle}_input.txt"), 2, 206969),   # long input, part 2
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

    config = 'i2'
    lines, part, expected = input_data(config)
    print(f" 1| {puzzle=}, {config=}, {part=}, {expected=}")

    start_time = time.time()
    solution = solve_part1(lines) if part == 1 else solve_part2(lines)
    elapsed_time = time.time() - start_time
    print(f" 2| {solution=} in {int(elapsed_time*1e3)} ms"
          f"\n=====> {'OK' if solution == expected else 'NOT OK'}")

if __name__ == '__main__':
    solve_puzzle()
