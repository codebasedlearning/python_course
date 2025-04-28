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

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Self, Iterator, Callable, Sequence

# pylint: disable=too-few-public-methods
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

# Data - problem specific #
###########################


@dataclass
class RuntimeArgs:
    debug: bool = False
    # verbosity: int = 0
    # ... etc.


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


# Abstract Components #
#######################


class Producer(ABC):
    @abstractmethod
    def read(self, runtime_args: RuntimeArgs) -> Iterator[InputData]: ...


class Processor(ABC):
    @abstractmethod
    def apply(self, process_data: ProcessData, runtime_args: RuntimeArgs) -> ProcessData: ...


class Consumer(ABC):
    @abstractmethod
    def write(self, output_data: OutputData, runtime_args: RuntimeArgs) -> None: ...


# Abstract Problem #
####################


class IPO(ABC):
    @abstractmethod
    def input(self, producers: Producer | list[Producer]) -> Self: ...

    @abstractmethod
    def process(self, processors: Processor | list[Processor]) -> Self: ...

    @abstractmethod
    def output(self, consumers: Consumer | list[Consumer]) -> Self: ...

    @abstractmethod
    def solve(self, runtime_args: RuntimeArgs) -> list[tuple[Producer,InputData,ProcessData]]: ...


class IPOProblem(IPO):
    """ base implementation for IPO problems """
    def __init__(self) -> None:
        self.producers: list[Producer] = []
        self.processors: list[Processor] = []
        self.consumers: list[Consumer] = []

    def input(self, producers: Producer | list[Producer]) -> Self:
        self.producers = [producers] if isinstance(producers, Producer) else producers
        return self

    def process(self, processors: Processor | list[Processor]) -> Self:
        self.processors = [processors] if isinstance(processors, Processor) else processors
        return self

    def output(self, consumers: Consumer | list[Consumer]) -> Self:
        self.consumers = [consumers] if isinstance(consumers, Consumer) else consumers
        return self

    def solve(self, runtime_args: 'RuntimeArgs'= RuntimeArgs() ) -> list[tuple[Producer,InputData,ProcessData]]:
        results = []
        for producer in self.producers:             # or with 'chain'
            for input_data in producer.read(runtime_args):
                print(f" a| - {f'read from {producer.__class__.__name__}:':<30} {input_data}")

                process_data = ProcessData.of(input_data)
                # process_data = input_data.map_to()
                #process_data = self.process_data_factory(input_data)
                print(f" b| - {'start processing:':<30} {process_data}")
                for processor in self.processors:
                    process_data = processor.apply(process_data, runtime_args)
                    print(f" c| - {f'processed by {processor.__class__.__name__}:':<30} - {process_data}")

                results.append((producer, input_data, process_data))
                output_data = OutputData.of(input_data, process_data)
                #output_data = self.output_data_factory(input_data, process_data)
                for consumer in self.consumers:
                    print(f" d| - {f'write to {consumer.__class__.__name__}:':<30} {output_data}")
                    consumer.write(output_data, runtime_args)
                print()
        return results

    @classmethod
    def create(cls,
               input: Producer | list[Producer],        # pylint: disable=redefined-builtin
               process: Processor | list[Processor],
               output: Consumer | list[Consumer]
    ) -> Self:
        return cls() \
            .input(input) \
            .process(process) \
            .output(output)


class SquareProblem(IPOProblem):
    pass


# Components #
##############


class ConstantProducer(Producer):
    def __init__(self, initial_x: int) -> None:
        self.initial_x = initial_x

    def read(self, runtime_args: RuntimeArgs) -> Iterator[InputData]:
        yield InputData(source = "const", x = self.initial_x)   # would be return without sequences


class SquareProcessor(Processor):
    def apply(self, process_data: ProcessData, runtime_args: RuntimeArgs) -> ProcessData:
        if runtime_args.debug:
            print("======> square, dt=0.005")   # just an example
        return ProcessData(y = process_data.y ** 2)


class Add1Processor(Processor):
    def apply(self, process_data: ProcessData, runtime_args: RuntimeArgs) -> ProcessData:
        if runtime_args.debug:
            print("======> add 1, dt=0.003")
        return ProcessData(y = process_data.y + 1)


class ConsoleConsumer(Consumer):
    def write(self, output_data: OutputData, runtime_args: RuntimeArgs) -> None:
        print(f" A|   - write data to console: '{output_data.x} -> {output_data.y}'")


class LogConsumer(Consumer):
    def write(self, output_data: OutputData, runtime_args: RuntimeArgs) -> None:
        print(f" B|   - write data to log: '{output_data.x} -> {output_data.y}'")


def solve_two_ways():
    """ use the problem class with chaining or with a factory """
    print("\nsolve_two_ways\n==============")

    runtime_args = RuntimeArgs(debug=True)

    print(" 1| constant input, console output, no factory")
    result = SquareProblem() \
        .input(ConstantProducer(initial_x=2)) \
        .process([SquareProcessor(),Add1Processor()]) \
        .output(ConsoleConsumer()) \
        .solve(runtime_args)
    print(f" 2| {result[0][1:]=}")

    print(" 3| with factory")
    result = SquareProblem.create(
        input=ConstantProducer(initial_x=2),
        process=[SquareProcessor(),Add1Processor()],
        output=ConsoleConsumer()
    ).solve(runtime_args)
    print(f" 4| {result[0][1:]=}")


class FastProcessor(Processor):
    def __init__(self) -> None:
        self.square = SquareProcessor()
        self.add1 = Add1Processor()

    def apply(self, process_data: ProcessData, runtime_args: RuntimeArgs) -> ProcessData:
        return ProcessData(y = self.add1.apply(
            self.square.apply(process_data,runtime_args),runtime_args).y
        )


class FileProducer(Producer):
    def __init__(self, source:str) -> None:
        self.source = source

    def read(self, runtime_args: RuntimeArgs) -> Iterator[InputData]:
        yield InputData(source = self.source, x = 3)

class FileConsumer(Consumer):
    def write(self, output_data: OutputData, runtime_args: RuntimeArgs) -> None:
        dest = output_data.source.replace(".in", ".out")
        print(f" C|   - write data to '{dest}': '{output_data.x} -> {output_data.y}'")


class StreamProducer(Producer):
    def __init__(self, seq: Sequence) -> None:
        self.seq = seq

    def read(self, runtime_args: RuntimeArgs) -> Iterator[InputData]:
        for i, item in enumerate(self.seq):
            x = item if isinstance(item,int) else i
            source = item if isinstance(item,str) and item.endswith(".in") else "const"
            yield InputData(source=source, x=x)


def solve_with_file_io_and_streams():
    """ standard workflow with input and output files """
    print("\nsolve_with_file_io_and_streams\n==============================")

    print(" 1| file io, fast")
    SquareProblem.create(
        input=FileProducer(source="data.in"),
        process=FastProcessor(),
        output=FileConsumer()
    ).solve()

    print(" 2| filename stream, fast")
    SquareProblem.create(
        input=StreamProducer(seq=["data1.in","data2.in","data3.in"]),
        process=FastProcessor(),
        output=FileConsumer()
    ).solve()

    print(" 3| number stream, lambda, debug")
    SquareProblem.create(
        input=StreamProducer(seq=range(1,4)),
        process=FastProcessor(),
        output=ConsoleConsumer()
    ).solve()


class LambdaProcessor(Processor):
    def __init__(self, func: Callable[[int], int]):
        self.func = func

    def apply(self, process_data: ProcessData, runtime_args: RuntimeArgs) -> ProcessData:
        return ProcessData(y = self.func(process_data.y))


class DebugProcessor(Processor):
    def apply(self, process_data: ProcessData, runtime_args: RuntimeArgs) -> ProcessData:
        print(f" D|   - debug: {process_data}")
        return process_data


def solve_in_various_combinations():
    """ combine multiple producers, consumers and processors """
    print("\nsolve_in_various_combinations\n=============================")

    print(" 1| multiple inputs and outputs, fast with debug")
    SquareProblem.create(
        input=[ConstantProducer(initial_x=3), ConstantProducer(initial_x=4)],
        process=[FastProcessor(),DebugProcessor()],
        output=[ConsoleConsumer(), LogConsumer()]
    ).solve()

    print(" 2| lambda")
    SquareProblem.create(
        input=ConstantProducer(initial_x=3),
        process=LambdaProcessor(lambda x: x ** 2 + 1),
        output=ConsoleConsumer()
    ).solve()


if __name__ == "__main__":
    solve_two_ways()
    solve_with_file_io_and_streams()
    solve_in_various_combinations()
