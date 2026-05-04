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

from dataclasses import dataclass
from typing import Self, Iterator, Callable, Sequence

from utils import print_function_header

import logging
import sys

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
logging.getLogger('ipo').setLevel(logging.DEBUG)

from contextvars import ContextVar

from gropro import Producer, Processor, Consumer, IPOProblem, ipo_context

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

runtime_args_ctx: ContextVar[RuntimeArgs] = ContextVar('runtime_args_ctx')

class DryRunConsumer(Consumer[OutputData]):
    def write(self, output_data: OutputData) -> None:
        runtime_args = runtime_args_ctx.get()
        print(f"write {'(dry_run)' if runtime_args.dry_run else ''}: '{output_data}')")

@print_function_header
def solve_with_runtime_args():
    """ solver workflow, compare to the workflow before """

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

    with ipo_context(runtime_args_ctx, RuntimeArgs(dry_run=True)):
        SquarePlusOneProblem.of(
            input=ConstantProducer(initial_x=3),
            process=SquarePlusOneProcessor(),
            output=DryRunConsumer()
        ).solve()


# Decorator pattern: wrap any Processor to add a cross-cutting concern
# (timing, here) without touching the wrapped processor itself. Open/Closed
# principle made physical.
import time

class TimingProcessor(Processor[ProcessData]):
    """ measures and prints the elapsed time of an inner processor """

    def __init__(self, inner: Processor) -> None:
        self.inner = inner

    def apply(self, process_data: ProcessData) -> ProcessData:
        t0 = time.perf_counter()
        result = self.inner.apply(process_data)
        dt_ms = (time.perf_counter() - t0) * 1000
        print(f"duration ({self.inner.__class__.__name__}): {dt_ms:.4f} ms")
        return result


@print_function_header
def solve_with_timing():
    """ wrap a real Processor in TimingProcessor — same pipeline, free timing """
    SquarePlusOneProblem.of(
        input=ConstantProducer(initial_x=5),
        process=TimingProcessor(SquarePlusOneProcessor()),
        output=ConsoleConsumer()
    ).solve()


# Bridges the IPO framework and the testing world: the consumer becomes
# the assertion. Useful for golden-output / regression tests.

class ValidatingConsumer(Consumer[OutputData]):
    """ asserts OutputData.y matches an expected value """

    def __init__(self, expected_y: int) -> None:
        self.expected_y = expected_y

    def write(self, output_data: OutputData) -> None:
        if output_data.y != self.expected_y:
            raise AssertionError(
                f"expected y={self.expected_y}, got y={output_data.y} "
                f"(input x={output_data.x} from {output_data.source!r})"
            )
        print(f"validation: PASS (y={output_data.y})")


@print_function_header
def solve_with_validation():
    """ ValidatingConsumer turns the pipeline into a one-shot test """
    SquarePlusOneProblem.of(
        input=ConstantProducer(initial_x=3),
        process=SquarePlusOneProcessor(),
        output=ValidatingConsumer(expected_y=10)   # 3^2 + 1 = 10
    ).solve()


# Chained pipelines: feed the OutputData of one IPOProblem in as the
# InputData of the next via a tiny adapter. The whole framework becomes
# itself composable — that's the moment the abstraction clicks.

class OutputAdapterProducer(Producer[InputData]):
    """ feeds the results of a previous .solve() as InputData of the next pipeline """

    def __init__(self, results) -> None:
        self.results = results

    def read(self) -> Iterator[InputData]:
        for r in self.results:
            yield InputData(source=f"{r.input_data.example}->chain", x=r.process_data.y)


class DoubleProcessor(Processor[ProcessData]):
    def apply(self, process_data: ProcessData) -> ProcessData:
        return ProcessData(y=process_data.y * 2)


@print_function_header
def solve_chained_pipeline():
    """ Stage 1: x → x²+1 ;  Stage 2: y → 2·y .  Output of stage 1 becomes input of stage 2. """

    # Stage 1: x = 3 → y = 10
    stage1 = SquarePlusOneProblem.of(
        input=ConstantProducer(initial_x=3),
        process=SquarePlusOneProcessor(),
        output=ConsoleConsumer()
    ).solve()

    # Stage 2: x = 10 (from stage 1) → y = 20
    SquarePlusOneProblem.of(
        input=OutputAdapterProducer(stage1),
        process=DoubleProcessor(),
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
    result = list(producer.read())
    assert len(result) == 1 and result[0].x == 23


class BlackHoleConsumer(Consumer):
    def write(self, output_data: OutputData) -> None:
        pass


def test_SquarePlusOneProcessor_results():
    """ test that the producer creates valid InputData """
    result = SquarePlusOneProblem.of(
        input=ConstantProducer(initial_x=3),
        process=SquarePlusOneProcessor(),
        output=BlackHoleConsumer()
    ).solve()
    assert len(result) == 1 and result[0].process_data.y==10


def test_solve_rejects_missing_slots():
    """ solve() refuses to run on a half-wired pipeline """
    with pytest.raises(RuntimeError, match="missing"):
        SquarePlusOneProblem().solve()                          # nothing wired
    with pytest.raises(RuntimeError, match="process, output"):
        SquarePlusOneProblem().input(ConstantProducer(1)).solve()


def test_subclass_without_type_args_fails():
    """ forgetting [I, P, O] is caught at class-definition time """
    with pytest.raises(TypeError, match="must be parameterized"):
        class BrokenProblem(IPOProblem):       # noqa: F841 — defining the class is the test
            pass


def test_subclass_inherits_data_classes():
    """ subclassing a parameterized problem without re-stating [I, P, O] is OK """
    class FasterSquare(SquarePlusOneProblem):
        pass
    assert FasterSquare.process_data_class is ProcessData


def run_tests():
    """ pytest entry — also: uv run pytest 0x_tra_gropros/snippets/b_ipo/c_examples.py -v """
    pytest.main([__file__, "-v"])


if __name__ == "__main__":
    solve_straight()
    solve_with_combined_processors()
    solve_with_file_io()
    solve_with_streams()
    solve_with_multiple_producers()
    solve_with_lambdas()
    solve_with_runtime_args()
    solve_with_timing()
    solve_with_validation()
    solve_chained_pipeline()
    run_tests()
