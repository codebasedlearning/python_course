# (C) 2025 Alexander Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet discusses the idea behind the general IPO approach.

Teaching focus
  - IPO idea
  - minimal set of classes to implement

IPO
  - The solution is built according to the IPO pattern (Input-Process-Output'=EVA-Principle').
    This leads to this 'main'
        problem
            .input(producer)            # reads data
            .process(processor)         # processes data aka solves the problem
            .output(consumer)           # writes data
    and variations.

  - Instead of having all the information in a single problem-data object,
    we separate it into InputData, ProcessData and OutputData, with the data specific
    to each step of the IPO approach (information hiding).

    Producers provide InputData, processors work on ProcessData, and consumers get OutputData.

    So this is the flow:
        problem                                         # problem-specific inits
         -> producer.read -> InputData                  # gather InputData
            InputData -> ProcessData                    # InputData != ProcessData
         -> processor.apply(ProcessData) -> ProcessData # create final ProcessData
            ProcessData -> OutputData                   # ProcessData != OutputData
         -> consumer.write(OutputData)                  # write results

  - In this way, each part of the problem can be modeled individually and
    combined according to the problem at hand (strategy pattern for processors).

The Square-Problem
  - This is a simple 'problem' to show how all the parts work together.

Additional Notes
================

  - We use @dataclass for simple data models.
  - We use @abstractmethod for 'interfaces'.
  - We allow for multiple producers, processors and consumers.
  - We go from an abstract producer to a concrete Producer, e.g. a ConstProducer.
"""

from dataclasses import dataclass
from typing import Self, Iterator, Callable, Sequence

from utils import print_function_header

import logging
import sys

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
logging.getLogger('ipo').setLevel(logging.DEBUG)

from contextvars import ContextVar

from gropro import Producer, Processor, Consumer, IPOProblem

# pylint: disable=too-few-public-methods
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

# Data - problem specific #
###########################


@dataclass
class InputData:
    source: str
    x: int


@dataclass
class ProcessData:
    y: int = 0

    @classmethod
    def of(cls, input_data: InputData) -> Self:
        return cls(y=input_data.x)


@dataclass
class OutputData:
    source: str
    x: int
    y: int

    @classmethod
    def of(cls, input_data: InputData, process_data: ProcessData) -> Self:
        return cls(source=input_data.source, x=input_data.x, y=process_data.y)


class SquarePlusOneProblem(IPOProblem[InputData, ProcessData, OutputData]):
    pass


# Components #
##############

class ConstantProducer(Producer[InputData]):
    def __init__(self, initial_x: int) -> None:
        self.initial_x = initial_x

    def read(self) -> Iterator[InputData]:
        yield InputData(source = "const", x = self.initial_x)   # would be return without sequences


class SquarePlusOneProcessor(Processor[ProcessData]):
    def apply(self, process_data: ProcessData) -> ProcessData:
        return ProcessData(y = process_data.y ** 2 + 1)


class ConsoleConsumer(Consumer):
    def write(self, output_data: OutputData) -> None:
        print(f"write '{output_data}' to 'console'")



@print_function_header
def solve_straight():
    """ use the problem class with chaining or with a factory """

    SquarePlusOneProblem.of(
        input=ConstantProducer(initial_x=2),
        process=SquarePlusOneProcessor(),
        output=ConsoleConsumer()
    ).solve()

class SquareProcessor(Processor[ProcessData]):
    def apply(self, process_data: ProcessData) -> ProcessData:
        return ProcessData(y = process_data.y ** 2)

class AddOneProcessor(Processor[ProcessData]):
    def apply(self, process_data: ProcessData) -> ProcessData:
        return ProcessData(y = process_data.y + 1)

class LogConsumer(Consumer):
    def write(self, output_data: OutputData) -> None:
        print(f"write '{output_data}' to 'log'")

@print_function_header
def solve_with_combined_processors():
    """ use the problem class with chaining or with a factory """
    SquarePlusOneProblem.of(
        input=ConstantProducer(initial_x=2),
        process=[SquareProcessor(),AddOneProcessor()],
        output=[ConsoleConsumer(), LogConsumer()]
    ).solve()

class FileProducer(Producer):
    def __init__(self, filename:str) -> None:
        self.filename = filename

    def read(self) -> Iterator[InputData]:
        yield InputData(source = self.filename, x = 3)

class FileConsumer(Consumer):
    def write(self, output_data: OutputData) -> None:
        dest = output_data.source.replace(".in", ".out")
        print(f"write '{output_data}' to '{dest}'")
        #print(f" C|   - write data to '{dest}': '{output_data.x} -> {output_data.y}'")

@print_function_header
def solve_with_file_io():
    """ use the problem class with chaining or with a factory """
    SquarePlusOneProblem.of(
        input=FileProducer(filename="data.in"),
        process=SquarePlusOneProcessor(),
        output=FileConsumer()
    ).solve()

class StreamProducer(Producer):
    def __init__(self, seq: Sequence) -> None:
        self.seq = seq

    def read(self) -> Iterator[InputData]:
        for i, item in enumerate(self.seq):
            x = item if isinstance(item,int) else i
            source = item if isinstance(item,str) and item.endswith(".in") else "const"
            yield InputData(source=source, x=x)

@print_function_header
def solve_with_streams():
    """ standard workflow with input and output files """
    SquarePlusOneProblem.of(
        input=StreamProducer(seq=["data1.in","data2.in","data3.in"]), # or seq=range(1,4)
        process=SquarePlusOneProcessor(),
        output=ConsoleConsumer()
    ).solve()

@print_function_header
def solve_with_multiple_producers():
    """ combine multiple producers, consumers and processors """

    SquarePlusOneProblem.of(
        input=[ConstantProducer(initial_x=3), ConstantProducer(initial_x=4)],
        process=SquarePlusOneProcessor(),
        output=ConsoleConsumer()
    ).solve()

class LambdaProcessor(Processor):
    def __init__(self, func: Callable[[int], int]):
        self.func = func

    def apply(self, process_data: ProcessData) -> ProcessData:
        return ProcessData(y = self.func(process_data.y))

@print_function_header
def solve_with_lambdas():
    """ use the problem class with chaining or with a factory """
    SquarePlusOneProblem.of(
        input=ConstantProducer(initial_x=2),
        process=LambdaProcessor(lambda x: x ** 2 + 1),
        output=ConsoleConsumer()
    ).solve()


@dataclass
class RuntimeArgs:
    dry_run: bool = False

runtime_args_ctx = ContextVar('runtime_args_ctx')

class DryRunConsumer(Consumer[OutputData]):
    def write(self, output_data: OutputData) -> None:
        runtime_args = runtime_args_ctx.get()
        print(f"write {'(dry_run)' if runtime_args.dry_run else ''}: '{output_data}')")

def solve_with_runtime_args():
    """ solver workflow, compare to the workflow before """
    token = runtime_args_ctx.set(RuntimeArgs(dry_run=True))
    try:
        SquarePlusOneProblem.of(
            input=ConstantProducer(initial_x=3),
            process=SquarePlusOneProcessor(),
            output=DryRunConsumer()
        ).solve()
    finally:
        runtime_args_ctx.reset(token)


# def test_ConstantProducer_read():
#     """ test that the producer creates valid InputData """
#     producer = ConstantProducer(initial_x=23)
#     result = list(producer.read())
#     assert len(result) == 1 and result[0].x == 23
#
# class BlackHoleConsumer(Consumer):
#     def write(self, output_data: OutputData) -> None:
#         pass
#
# def test_SquarePlusOneProcessor_results():
#     """ test that the producer creates valid InputData """
#     result = SquarePlusOneProblem.of(
#         input=ConstantProducer(initial_x=3),
#         process=SquarePlusOneProcessor(),
#         output=BlackHoleConsumer()
#     ).solve()
#     assert len(result) == 1 and result[0].process_data.y==10
#
# import pytest


# or: uv run pytest 0x_tra_gropros/snippets/b_ipo/c_ipo_examples.py -v

# def run_tests():
#    pytest.main([__file__, "-v"])

if __name__ == "__main__":
    solve_straight()
    solve_with_combined_processors()
    solve_with_file_io()
    solve_with_streams()
    solve_with_multiple_producers()
    solve_with_lambdas()
    solve_with_runtime_args()
    # run_tests()
