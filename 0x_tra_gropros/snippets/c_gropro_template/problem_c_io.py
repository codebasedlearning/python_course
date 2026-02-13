# (C) 2025 Alexander Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
Here io components for the IPO framework are defined.
"""

from typing import Iterator

# import problem data and IPO framework
from problem_a_data import RuntimeArgs, InputData, OutputData       # ProcessData
from problem_b_ipo import Producer, Consumer                        # IPOSolver, Processor

# pylint: disable=too-few-public-methods
# pylint: disable=missing-class-docstring


class ConstantProducer(Producer):
    def __init__(self, initial_x: int) -> None:
        self.initial_x = initial_x

    def read(self, runtime_args: RuntimeArgs) -> Iterator[InputData]:
        yield InputData(source = "const", x = self.initial_x)   # would be return without sequences


class ConsoleConsumer(Consumer):
    def write(self, output_data: OutputData, runtime_args: RuntimeArgs) -> None:
        print(f" C|   - write data to console: '{output_data.x} -> {output_data.y}'")
