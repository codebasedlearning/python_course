# (C) Alexander Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

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

from dataclasses import dataclass, field, replace
from typing import Self, Iterator, Callable, Sequence

from gropro.ipo import DiscardConsumer
from utils import print_function_header

import logging
import sys
import time


logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
logging.getLogger('ipo').setLevel(logging.DEBUG)

from contextvars import ContextVar

from gropro import Producer, Processor, Consumer, IPOProblem, Fan, Chain, ipo_context

# pylint: disable=too-few-public-methods
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

# Data - problem specific #
###########################


@dataclass
class InputData:
    source: str = ""
    x: int = 0


@dataclass
class ProcessData:
    x: int = 0
    y: int = 0

    @classmethod
    def of(cls, input_data: InputData) -> Self:
        # init x and also y, so we can work chained (see examples)
        return cls(x=input_data.x,y=input_data.x)


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


# General Components #
######################

class ConstantProducer(Producer[InputData]):
    def __init__(self, initial_x: int) -> None:
        self.initial_x = initial_x

    def read(self, input_data: InputData) -> Iterator[InputData]:
        yield replace(input_data, source="const", x=self.initial_x)


class SquarePlusOneProcessor(Processor[ProcessData]):
    def apply(self, process_data: ProcessData) -> Iterator[ProcessData]:
        y = process_data.x ** 2 + 1
        yield replace(process_data, y=y)


class ConsoleConsumer(Consumer):
    def write(self, output_data: OutputData) -> None:
        print(f"write '{output_data}' to 'console'")

class LogConsumer(Consumer):
    def write(self, output_data: OutputData) -> None:
        print(f"write '{output_data}' to 'log'")



@print_function_header
def solve_straight():
    """ default problem solver """

    print(f" 1| standard")
    SquarePlusOneProblem.of(
        input=ConstantProducer(initial_x=2),
        process=SquarePlusOneProcessor(),
        output=ConsoleConsumer()
    ).solve()

    print(f" 2| multiple input")
    SquarePlusOneProblem.of(
        input=Fan(ConstantProducer(initial_x=2),ConstantProducer(initial_x=3)),
        process=SquarePlusOneProcessor(),
        output=ConsoleConsumer()
    ).solve()

    print(f" 3| multiple output")
    SquarePlusOneProblem.of(
        input=ConstantProducer(initial_x=2),
        process=SquarePlusOneProcessor(),
        output=Fan(ConsoleConsumer(),LogConsumer())
    ).solve()

    print(f" 4| multiple input and output")
    SquarePlusOneProblem.of(
        input=Fan(ConstantProducer(initial_x=2),ConstantProducer(initial_x=3)),
        process=SquarePlusOneProcessor(),
        output=Fan(ConsoleConsumer(),LogConsumer())
    ).solve()


@print_function_header
def solve_with_combined_processors():
    """ use the problem class with chaining; ProcessData is updated, y is initialized with x at start """

    class SquareProcessor(Processor[ProcessData]):
        def apply(self, process_data: ProcessData) -> Iterator[ProcessData]:
            y = process_data.y ** 2         # continue work from y
            yield replace(process_data, y=y)

    class AddOneProcessor(Processor[ProcessData]):
        def apply(self, process_data: ProcessData) -> Iterator[ProcessData]:
            y = process_data.y + 1          # continue work from y
            yield replace(process_data, y=y)

    print(f" 1| chain processors")
    SquarePlusOneProblem.of(
        input=ConstantProducer(initial_x=2),
        process=Chain(SquareProcessor(),AddOneProcessor()),
        output=ConsoleConsumer()
    ).solve()



@print_function_header
def solve_with_file_io():
    """ use the problem class with chaining or with a factory """

    class FileProducer(Producer):
        def __init__(self, filename: str) -> None:
            self.filename = filename

        def read(self, input_data: InputData) -> Iterator[InputData]:
            yield replace(input_data, source=self.filename, x=3)

    class FileConsumer(Consumer):
        def write(self, output_data: OutputData) -> None:
            dest = output_data.source.replace(".in", ".out")
            print(f"write '{output_data}' to '{dest}'")

    print(f" 1| read from file and write to file (simulated)")
    SquarePlusOneProblem.of(
        input=FileProducer(filename="data.in"),
        process=SquarePlusOneProcessor(),
        output=FileConsumer()
    ).solve()


@print_function_header
def solve_with_streams():
    """ standard workflow with input and output files """

    class StreamProducer(Producer):
        def __init__(self, seq: Sequence) -> None:
            self.seq = seq

        def read(self, input_data: InputData) -> Iterator[InputData]:
            for i, item in enumerate(self.seq):
                x = item if isinstance(item, int) else i+1    # for demonstration
                source = item if isinstance(item, str) and item.endswith(".in") else "const"
                yield InputData(source=source, x=x)

    print(f" 1| read files from folder (simulated)")
    SquarePlusOneProblem.of(
        input=StreamProducer(seq=["data1.in","data2.in","data3.in"]),
        process=SquarePlusOneProcessor(),
        output=ConsoleConsumer()
    ).solve()

    print(f" 2| read data from sequence")
    SquarePlusOneProblem.of(
        input=StreamProducer(seq=range(10,12)),
        process=SquarePlusOneProcessor(),
        output=ConsoleConsumer()
    ).solve()


@print_function_header
def solve_with_lambdas():
    """ use the problem class with chaining or with a factory """

    class LambdaProcessor(Processor):
        def __init__(self, func: Callable[[int], int]):
            self.func = func

        def apply(self, process_data: ProcessData) -> Iterator[ProcessData]:
            y = self.func(process_data.x)
            yield replace(process_data, y=y)

    print(f" 1| calc result from lambda")
    SquarePlusOneProblem.of(
        input=ConstantProducer(initial_x=2),
        process=LambdaProcessor(lambda x: x ** 2 + 1),
        output=ConsoleConsumer()
    ).solve()


@dataclass
class RuntimeArgs:
    dry_run: bool = False

runtime_args_ctx: ContextVar[RuntimeArgs] = ContextVar('runtime_args_ctx')

@print_function_header
def solve_with_runtime_args():
    """ solver workflow, compare to the workflow before """

    class DryRunConsumer(Consumer[OutputData]):
        def write(self, output_data: OutputData) -> None:
            runtime_args = runtime_args_ctx.get()
            print(f"write {'(dry_run)' if runtime_args.dry_run else ''}: '{output_data}')")

    # same as:
    # token = runtime_args_ctx.set(RuntimeArgs(dry_run=True))
    # try:
    #     SquarePlusOneProblem.of(
    #         input=ConstantProducer(initial_x=3),
    #         process=SquarePlusOneProcessor(),
    #         output=DryRunConsumer()
    #     ).solve()
    # finally:
    #     runtime_args_ctx.reset(token)

    print(f" 1| solve with context")
    with ipo_context(runtime_args_ctx, RuntimeArgs(dry_run=True)):
        SquarePlusOneProblem.of(
            input=ConstantProducer(initial_x=3),
            process=SquarePlusOneProcessor(),
            output=DryRunConsumer()
        ).solve()


@print_function_header
def solve_with_timing():
    """ measure time """

    # Decorator pattern / Open/Closed principle: wrap any Processor to add a cross-cutting
    # concern (timing) without touching the wrapped processor itself.
    class TimingProcessor(Processor[ProcessData]):
        """ measures and prints the elapsed time of an inner processor """

        def __init__(self, inner: Processor) -> None:
            self.inner = inner

        def apply(self, process_data: ProcessData) -> Iterator[ProcessData]:
            t0 = time.perf_counter()
            yield from self.inner.apply(process_data)
            dt_ms = (time.perf_counter() - t0) * 1000
            print(f"duration ({self.inner.__class__.__name__}): {dt_ms:.4f} ms")

    print(f" 1| measure time")
    SquarePlusOneProblem.of(
        input=ConstantProducer(initial_x=3),
        process=TimingProcessor(SquarePlusOneProcessor()),
        output=ConsoleConsumer()
    ).solve()


@print_function_header
def solve_with_validation():
    """ one-shot test """

    class ValidatingConsumer(Consumer[OutputData]):
        """ asserts OutputData.y matches an expected value """

        def __init__(self, expected_y: int) -> None:
            self.expected_y = expected_y

        def write(self, output_data: OutputData) -> None:
            print(f"validation x={output_data.x} -> ", end='')
            if output_data.y != self.expected_y:
                print(f"ERROR: y={output_data.y}, expected y={self.expected_y}")
            else:
                print(f"PASS:  y={output_data.y}")

    print(f" 1| measure time")
    SquarePlusOneProblem.of(
        input=ConstantProducer(initial_x=3),
        process=SquarePlusOneProcessor(),
        output=ValidatingConsumer(expected_y=10)
    ).solve()


# Chained pipelines: feed the OutputData of one IPOProblem in as the
# InputData of the next via a tiny adapter. The whole framework becomes
# itself composable — that's the moment the abstraction clicks.

# class OutputAdapterProducer(Producer[InputData]):
#     """ feeds the results of a previous .solve() as InputData of the next pipeline """
#
#     def __init__(self, results) -> None:
#         self.results = results
#
#     def read(self) -> Iterator[InputData]:
#         for r in self.results:
#             yield InputData(source=f"{r.input_data.example}->chain", x=r.process_data.y)


# class DoubleProcessor(Processor[ProcessData]):
#     def apply(self, process_data: ProcessData) -> ProcessData:
#         return ProcessData(y=process_data.y * 2)


@print_function_header
def solve_chained_pipeline():
    """ Stage 1: x → x²+1 ;  Stage 2: y → 2·y .  Output of stage 1 becomes input of stage 2. """

    class OutputAdapterProducer(Producer[InputData]):
        """ feed an upstream pipeline's results into a downstream pipeline """

        def __init__(self, upstream_stream):
            self.upstream = upstream_stream

        def read(self, input_data: InputData) -> Iterator[InputData]:
            for result in self.upstream:
                yield replace(input_data, source=result.source, x=result.y)

    class DoubleProcessor(Processor[ProcessData]):
        def apply(self, process_data: ProcessData) -> Iterator[ProcessData]:
            y = process_data.x * 2
            yield replace(process_data, y=y)

    # Stage 1: x = 3 → y = 10
    print(f" 1| stage 1")
    stage1 = SquarePlusOneProblem.of(
        input=ConstantProducer(initial_x=3),
        process=SquarePlusOneProcessor(),
        output=ConsoleConsumer()
    ).stream()
    #print(stage1)

    # Stage 2: x = 10 (from stage 1) → y = 20
    print(f" 2| stage 2")
    SquarePlusOneProblem.of(
        input=OutputAdapterProducer(stage1),
        process=DoubleProcessor(),
        output=ConsoleConsumer()
    ).solve()


@print_function_header
def solve_with_incomplete_pipeline():
    """ default problem solver """

    print(f" 1| standard")
    SquarePlusOneProblem.of(
        #input=ConstantProducer(initial_x=2),
        #process=SquarePlusOneProcessor(),
        output=ConsoleConsumer()
    ).solve()

"""

More ideas:
  - A `GlobFileProducer("data/example_*.txt")`.
    Every GroPro hands you a `data/` folder with 5–20 input files. A two-class component, e.g. 
    `FileProducer` for one file, `GlobFileProducer` for the pattern, both yielding the parsed
    `InputData` folder would serve well.

  - An `ExpectedOutputConsumer`.
    Half the GroPros ship some sort of `data/example_N.in` *and* `data/example_N.out`. 
    Right now there is no built-in way to use the `.out` files except eyeballing diffs. 
    A consumer that, given the source filename, loads the matching `.out`, normalizes 
    whitespace and asserts equality (or pretty-prints the diff on mismatch) turns the 
    official test data into an actual regression suite. 

  - A `BenchmarkRunner` / multi-strategy harness.
    This is for the case writing a baseline solver first and then optimize. A small helper 
    that runs N strategies against the same producer and prints a table 
    (`strategy | size | time | status`) makes the optimization story visible to the grader. 

  - A `ProgressConsumer` decorator.
    When the search runs for 30 seconds on example 3, users panic and abort. A consumer that 
    prints `[3/9] example_3 → solving…` before each input is a 5-line file that prevents that. 
    Pair it with `TimingProcessor` and you have full-pipeline observability for free.

"""

# Test examples

import pytest


def test_ConstantProducer_read():
    """ test that the producer creates valid InputData """
    producer = ConstantProducer(initial_x=23)
    result = list(producer.read(InputData()))
    assert len(result) == 1 and result[0].x == 23


def test_SquarePlusOneProcessor_results():
    """ test that the producer creates valid InputData """
    result = SquarePlusOneProblem.of(
        input=ConstantProducer(initial_x=3),
        process=SquarePlusOneProcessor(),
        output=DiscardConsumer()
    ).solve()
    assert len(result) == 1 and result[0].y==10


def test_subclass_without_type_args_fails():
    """ forgetting [I, P, O] is caught at class-definition time """
    with pytest.raises(TypeError, match="must be parameterized"):
        class BrokenProblem(IPOProblem):       # noqa: F841 — defining the class is the test
            pass


def run_tests():
    """ pytest entry — also: uv run pytest 0x_tra_gropros/snippets/b_ipo/c_examples.py -v """
    pytest.main([__file__, "-v"])


if __name__ == "__main__":
    solve_straight()
    solve_with_combined_processors()
    solve_with_file_io()
    solve_with_streams()
    solve_with_lambdas()
    solve_with_runtime_args()
    solve_with_timing()
    solve_with_validation()
    solve_chained_pipeline()
    solve_with_incomplete_pipeline()
    run_tests()
