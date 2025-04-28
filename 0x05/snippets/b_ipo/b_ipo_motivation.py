# (C) 2025 Alexander Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet discusses the idea behind the general IPO approach.

Teaching focus
  - IPO idea

Model problem:
  - Calculate x^2+1 for a given x
"""

from dataclasses import dataclass
from typing import Self

# pylint: disable=too-few-public-methods


def solve_square_add1_step_by_step():
    """ solver workflow """
    print("\nsolve_square_add1_step_by_step\n==============================")

    """
    note the order of operations and the data flow
    """

    print(" 1| read data...", end='')
    input_data = ("data.in",3)                      # read()
    print(f" -> read x={input_data[1]} from '{input_data[0]}'")

    print(" 2| process data...", end='')
    process_data = input_data[1]                    # select
    process_data = process_data * process_data      # process in steps
    process_data = process_data + 1
    print(f" -> solve for x={input_data[1]}... -> y={process_data}")

    print(" 3| write data...", end='')
    output_data = (input_data[0].replace(".in",".out"), input_data[1], process_data)       # select
    print(f" -> write '{output_data[1]} -> {output_data[2]}' to '{output_data[0]}'")


@dataclass
class InputData:
    """ all data extracted from a source (Producer, e.g., a file) """
    source: str
    x: int

@dataclass
class ProcessData:
    """ all data needed to process (solve) a problem """
    y: int = 0

@dataclass
class OutputData:
    """ all data needed for a final output (Consumer, e.g., a file) """
    source: str
    x: int
    y: int

class Producer:
    """ produce InputData """
    def __init__(self, source: str):
        self.source = source

    def read(self) -> InputData:
        """ read data from a source """
        x = 3
        print(f" -> read x={x} from '{self.source}'")
        return InputData(source=self.source, x=x)

class Processor:
    """ process ProcessData """

    def apply(self, process_data: ProcessData) -> ProcessData:
        """ solve the problem and return the result/next ProcessData """
        print(f" -> solve for x={process_data.y}...")
        y = process_data.y ** 2 + 1
        return ProcessData(y=y)

class Consumer:
    """ consume OutputData """

    def write(self, output_data: OutputData) -> None:
        """ write it to a destination """
        dest = output_data.source.replace(".in", ".out")
        print(f" -> write '{output_data.x} -> {output_data.y}' to '{dest}'")

def solve_square_add1_with_objects():
    """ solver workflow, compare to the workflow before """
    print("\nsolve_square_add1_with_objects\n==============================")

    print(" 1| read data...", end='')
    input_data = Producer(source="data.in").read()

    # general idea: producer, processor, and consumer need to know only
    # the data they need, not everything; so this form of 'information hiding'
    # comes at a cost in the form of intermediate data objects and copying

    print(" 2| process data...", end='')
    process_data = ProcessData(y=input_data.x)
    process_data = Processor().apply(process_data)

    print(" 3| write data...", end='')
    output_data = OutputData(source=input_data.source, x=input_data.x, y=process_data.y)
    Consumer().write(output_data)


class SquareAdd1ProblemIPO:
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
            print(" 1| read data...", end='')
            input_data = self.producer.read()

            # convert input to process as start data, then work on this
            print(" 2| process data...", end='')
            process_data = ProcessData(y=input_data.x)
            process_data = self.processor.apply(process_data)

            # same here, prepare output from input and process data
            print(" 3| write data...", end='')
            output_data = OutputData(source=input_data.source, x=input_data.x, y=process_data.y)
            self.consumer.write(output_data)

def solve_square_add1_with_ipo():
    """ solver workflow, compare to the workflow before """
    print("\nsolve_square_add1_with_ipo\n==========================")

    SquareAdd1ProblemIPO() \
        .input(Producer(source="data.in")) \
        .process(Processor()) \
        .output(Consumer()) \
        .solve()

if __name__ == "__main__":
    solve_square_add1_step_by_step()
    solve_square_add1_with_objects()
    solve_square_add1_with_ipo()


"""
What could be improved here, perhaps with a view to SOLID?

Single Responsibility: 
    Class does too many things: input, process, and output all mixed.
Open/Closed: 
    Hard to extend without modifying the existing class (e.g., change input format, new output destination).
Liskov Substitution: 
    No way to substitute for part of the behavior (e.g., alternative solvers, or new processing steps).
Interface Segregation: 
    No interfaces at all; client code (the main) is tied to the big bloated methods.
Dependency Inversion: 
    Depends directly on low-level details (how it reads, how it writes, how it computes), not abstractions.
"""
