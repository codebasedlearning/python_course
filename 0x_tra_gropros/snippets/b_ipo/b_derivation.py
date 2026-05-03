# (C) 2025 Alexander Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet discusses the idea behind the general IPO approach.

Teaching focus
  - IPO idea

Model problem:
  - Calculate the root x0 for a given linear equation ax+b=0,
    given by the coefficients a, b.
"""

from dataclasses import dataclass
from typing import Self, Iterator #, Callable, Sequence

from utils import print_function_header

import logging
import sys

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
logging.getLogger('ipo').setLevel(logging.DEBUG)


# pylint: disable=too-few-public-methods

# solving algorithm

def root_solver(a, b):
    if abs(a) < 1e-12:
        raise ValueError("a=0, no solution")
    return (-b) / a


@print_function_header
def solve_step_by_step():
    """ solver workflow """

    """
    note the order of operations and the data flow
    """

    # input step: read input from any source, e.g., constant, file, database, stream, console

    print(" 1| read data...   ", end='')
    # collect input data for further processing, here: source, a, b
    input_data = ("data.in", 3, 4.5)
    print(f" -> {input_data=}")

    # process (solve) step: solve problem based on input data

    # a) extract process data from input data, here: a, b
    process_data = (input_data[1], input_data[2], 0.0)

    # b) solve the problem and update process data, here: x0
    print(f" 2| process data...", end='')
    a, b = process_data[0], process_data[1]
    x0 = root_solver(a, b)
    process_data = (a, b, x0)
    print(f" -> {process_data=}")

    # output step: write output to any destination, e.g., file, database, stream, console

    # a) extract output data from input and process data, here: source, dest, a, b, x0
    output_data = (
        input_data[0], input_data[0].replace(".in",".out"),
        process_data[0], process_data[1], process_data[2]
    )
    # b) write output data to destination
    print(" 3| write data...  ", end='')
    print(f" -> {output_data=}")


@dataclass
class InputData:
    """ all data extracted from a source by a Producer """
    source: str
    a: float
    b: float

@dataclass
class ProcessData:
    """ all data needed to process (solve) a problem by a Processor """
    a: float
    b: float
    x0: float

    @classmethod
    def of(cls, input_data: InputData) -> Self:
        return cls(a=input_data.a, b=input_data.b, x0=0.0)


@dataclass
class OutputData:
    """ all data needed for a final output for a Consumer """
    source: str
    #dest: str
    a: float
    b: float
    x0: float

    @classmethod
    def of(cls, input_data: InputData, process_data: ProcessData) -> Self:
        return cls(
            source=input_data.source,
            #dest=input_data.source.replace(".in",".out"),
            a=process_data.a, b=process_data.b, x0=process_data.x0)

class SampleProducer:
    """ produce InputData """
    def __init__(self, source: str):
        self.source = source

    def read(self) -> InputData:
        """ read data from a source """
        # read a,b from source
        return InputData(source=self.source, a=3, b=4.5)

class SampleProcessor:
    """ process ProcessData """

    def apply(self, process_data: ProcessData) -> ProcessData:
        """ solve the problem and return the result/next ProcessData """
        a, b = process_data.a, process_data.b
        x0 = root_solver(a, b)
        process_data = ProcessData(a=a, b=b, x0=x0)
        return process_data # ProcessData(a=a, b=b, x0=x0)

class SampleConsumer:
    """ consume OutputData """

    def write(self, output_data: OutputData) -> None:
        """ write it to a destination """
        dest = output_data.source.replace(".in", ".out")
        print(f"    -> write to '{dest}'")

@print_function_header
def solve_with_objects():
    """ solver workflow, compare to the workflow before """

    print(" 1| read data...   ", end='')
    input_data = SampleProducer(source="data.in").read()
    print(f" -> {input_data=}'")

    # general idea: producer, processor, and consumer need to know only
    # the data they need, not everything; so this form of 'information hiding'
    # comes at a cost in the form of intermediate data objects and copying

    process_data = ProcessData.of(input_data)
    print(f" 2| process data...", end='')
    process_data = SampleProcessor().apply(process_data)
    print(f" -> {process_data=}")

    print(" 3| write data...  ", end='')
    output_data = OutputData.of(input_data, process_data)
    print(f" -> write '{output_data=} ")
    SampleConsumer().write(output_data)

class SimpleIPO:
    """ problem solver """

    def __init__(self):
        self.producer = None
        self.processor = None
        self.consumer = None

    # 'input', 'process', and 'output' simply collect
    # the real components; 'run' does the work

    def input(self, producer) -> Self:
        """ collect a Producer """
        self.producer = producer
        return self

    def process(self, processor) -> Self:
        """ collect a Processor """
        self.processor = processor
        return self

    def output(self, consumer) -> Self:
        """ collect a Consumer """
        self.consumer = consumer
        return self

    def solve(self):
        """ take all components and call them in a chain """

        # simplified approach: work only when all components are in place
        if self.producer and self.processor and self.consumer:
            print(" 1| read data...   ", end='')
            input_data = self.producer.read()
            print(f" -> {input_data=}'")

            # convert input to process as start data, then work on this
            print(" 2| process data...", end='')
            process_data = ProcessData.of(input_data)
            process_data = self.processor.apply(process_data)
            print(f" -> {process_data=}")

            # same here, prepare output from input and process data
            print(" 3| write data...  ", end='')
            output_data = OutputData.of(input_data, process_data)
            print(f" -> write '{output_data=} ")
            self.consumer.write(output_data)

@print_function_header
def solve_with_simple_ipo():
    """ solver workflow, compare to the workflow before """
    SimpleIPO() \
        .input(SampleProducer(source="data.in")) \
        .process(SampleProcessor()) \
        .output(SampleConsumer()) \
        .solve()


# use IPO

from gropro import Producer, Processor, Consumer, IPOProblem

class RootProblem(IPOProblem[InputData, ProcessData, OutputData]):
    pass

class ConstantProducer(Producer[InputData]):
    def __init__(self, source: str, initial_a: float, initial_b: float):
        self.source = source
        self.initial_a = initial_a
        self.initial_b = initial_b

    def read(self) -> Iterator[InputData]:
        yield InputData(source=self.source, a=self.initial_a, b=self.initial_b)

class AlgebraicProcessor(Processor[ProcessData]):
    def apply(self, process_data: ProcessData) -> ProcessData:
        return ProcessData(
            a = process_data.a,
            b = process_data.b,
            x0 = root_solver(process_data.a, process_data.b)
        )

class ConsoleConsumer(Consumer[OutputData]):
    def write(self, output_data: OutputData) -> None:
        print(f"write '{output_data}' to 'console'")

@print_function_header
def solve_with_ipo():
    """ solver workflow, compare to the workflow before """
    RootProblem.of(
        input=ConstantProducer(source="data.in", initial_a=3, initial_b=4.5),
        process=AlgebraicProcessor(),
        output=ConsoleConsumer()
    ).solve()


if __name__ == "__main__":
    solve_step_by_step()
    solve_with_objects()
    solve_with_simple_ipo()
    solve_with_ipo()

