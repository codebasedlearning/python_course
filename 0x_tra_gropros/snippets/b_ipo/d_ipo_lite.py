# (C) Alexander Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet shows a lightweight IPO variant for simple problems.

Teaching focus
  - When the full IPO framework is overkill
  - Function-based IPO as a quick alternative
  - Same mental model, less boilerplate

When to use IPO-lite vs full IPO
  - Use lite when: single input source, one processing step, one output target,
    time pressure (exam), problem is straightforward.
  - Use full when: multiple input files, chained processors, swappable consumers,
    or when the problem complexity justifies the setup cost.

The idea
  - Keep the three-phase mental model (read → process → write) but replace the
    class hierarchy with plain functions and dataclasses. The pipeline function
    ipo_solve() chains them together.
  - You can always upgrade to the full framework later if the problem grows.
"""

from dataclasses import dataclass
from typing import Self

# pylint: disable=too-few-public-methods


# Data - same idea, fewer ceremony #
#####################################


@dataclass
class InputData:
    """ what we read from the source """
    source: str
    lines: list[str]


@dataclass
class ProcessData:
    """ what we compute """
    word_counts: dict[str, int]

    @classmethod
    def of(cls, input_data: InputData) -> Self:
        return cls(word_counts={})


@dataclass
class OutputData:
    """ what we write out """
    source: str
    word_counts: dict[str, int]

    @classmethod
    def of(cls, input_data: InputData, process_data: ProcessData) -> Self:
        return cls(source=input_data.source, word_counts=process_data.word_counts)


# Functions instead of classes #
################################


def read_input(source: str, text: str) -> InputData:
    """ producer: parse raw text into InputData """
    lines = [line.strip() for line in text.strip().splitlines() if line.strip()]
    return InputData(source=source, lines=lines)


def process(input_data: InputData) -> ProcessData:
    """ processor: count words per line """
    result = ProcessData.of(input_data)
    for line in input_data.lines:
        words = line.lower().split()
        for word in words:
            result.word_counts[word] = result.word_counts.get(word, 0) + 1
    return result


def write_output(input_data: InputData, process_data: ProcessData) -> None:
    """ consumer: print the results """
    output = OutputData.of(input_data, process_data)
    top_5 = sorted(output.word_counts.items(), key=lambda kv: kv[1], reverse=True)[:5]
    print(f" a|   source: {output.source}")
    for word, count in top_5:
        print(f" b|   {word:>12}: {count}")


# Pipeline - one function chains them #
########################################


def ipo_solve(source: str, text: str) -> ProcessData:
    """ the lite pipeline: read -> process -> write """
    input_data = read_input(source, text)
    process_data = process(input_data)
    write_output(input_data, process_data)
    return process_data


# Demo #
#########


SAMPLE_TEXT = """\
the quick brown fox jumps over the lazy dog
the fox said hello to the dog
and the dog said hello back to the fox
"""


def solve_lite():
    """ solve a word-count problem with the lite approach """
    print("\nsolve_lite\n==========")

    print(" 1| one-liner pipeline")
    ipo_solve("sample.txt", SAMPLE_TEXT)

    print()
    print(" 2| same phases, called step by step")
    inp = read_input("manual.txt", SAMPLE_TEXT)
    proc = process(inp)
    write_output(inp, proc)


def compare_effort():
    """ show the difference in setup cost """
    print("\ncompare_effort\n==============")

    print(" 1| lite: 3 functions + ipo_solve() → done")
    print("    full: Producer ABC + Processor ABC + Consumer ABC")
    print("          + IPO ABC + IPOProblem base + Problem subclass")
    print("          + concrete Producer + concrete Processor + concrete Consumer")
    print()
    print(" 2| rule of thumb:")
    print("    - exam with one input file, one output file → lite")
    print("    - multiple test cases, swappable strategies  → full")


def upgrade_path():
    """ demonstrate how lite functions map to full-framework classes """
    print("\nupgrade_path\n============")

    print(" 1| lite function     → full framework class")
    print("    read_input()      → Producer.read()")
    print("    process()         → Processor.apply()")
    print("    write_output()    → Consumer.write()")
    print("    ipo_solve()       → IPOProblem.solve()")
    print()
    print(" 2| to upgrade: wrap each function in a class,")
    print("    add ABC inheritance, done.")


if __name__ == "__main__":
    solve_lite()
    compare_effort()
    upgrade_path()
