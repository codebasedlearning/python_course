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

from dataclasses import dataclass, replace
from typing import Self, Iterator, Callable

from utils import print_function_header

import sys
import time

import logging
logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
logging.getLogger('ipo').setLevel(logging.DEBUG)

from contextvars import ContextVar

from gropro import Producer, Processor, Consumer, IPO, Tee, Merge, Chain, ipo_context

# pylint: disable=too-few-public-methods
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring


# Data - problem specific #
###########################


@dataclass
class SquarePlusOneSpec: # InputData
    source: str = ""
    x: int = 0


@dataclass
class SquarePlusOneSolution: # ProcessData
    x: int = 0
    y: int = 0

    @classmethod
    def of(cls, input_data: SquarePlusOneSpec) -> SquarePlusOneSolution:
        #    # init x and also y, so we can work chained (see examples)
        return cls(x=input_data.x,y=input_data.x)


@dataclass
class SquarePlusOneResult: # OutputData
    source: str
    x: int
    y: int

    @classmethod
    def of(cls, input_data: SquarePlusOneSpec, process_data: SquarePlusOneSolution) -> Self:
        return cls(source=input_data.source, x=input_data.x, y=process_data.y)


class SquarePlusOneProblem(IPO[SquarePlusOneSpec, SquarePlusOneSolution, SquarePlusOneResult]):
    pass


# General Components #
######################

class ConfigData(Producer[SquarePlusOneSpec]):
    def __init__(self, initial_x: int) -> None:
        self.initial_x = initial_x

    def read(self, input_data: SquarePlusOneSpec) -> Iterator[SquarePlusOneSpec]:
        yield replace(input_data, source="const", x=self.initial_x)


class SquarePlusOneProcessor(Processor[SquarePlusOneSolution]):
    def apply(self, process_data: SquarePlusOneSolution) -> SquarePlusOneSolution:
        y = process_data.x ** 2 + 1
        return replace(process_data, y=y)


class Console(Consumer):
    def write(self, output_data: SquarePlusOneResult) -> None:
        print(f"write '{output_data}' to 'console'")


@print_function_header
def solve_straight():
    """ default problem solver """

    print(f" 1| standard")
    SquarePlusOneProblem.of(
        input=ConfigData(initial_x=2),
        process=SquarePlusOneProcessor(),
        output=Console()
    ).solve()


@print_function_header
def solve_with_file_io():
    """ use the problem class with chaining or with a factory """

    class FileData(Producer):
        def __init__(self, filename: str) -> None:
            self.filename = filename

        def read(self, input_data: SquarePlusOneSpec) -> Iterator[SquarePlusOneSpec]:
            yield replace(input_data, source=self.filename, x=3)

    class Resultsfile(Consumer):
        def write(self, output_data: SquarePlusOneResult) -> None:
            dest = output_data.source.replace(".in", ".out")
            print(f"write '{output_data}' to '{dest}'")

    print(f" 1| read from file and write to file (simulated)")
    SquarePlusOneProblem.of(
        input=FileData(filename="data.in"),
        process=SquarePlusOneProcessor(),
        output=Resultsfile()
    ).solve()

    print(f" 2| read files from folder (simulated)")
    class FolderData(Producer):
        def __init__(self, folder: str) -> None:
            self.folder = folder

        def read(self, input_data: SquarePlusOneSpec) -> Iterator[SquarePlusOneSpec]:
            folder_data = ((x+1,self.folder+"/"+filename) for x,filename in enumerate(("data1.in","data2.in","data3.in")))
            for x,filename in folder_data:
                yield SquarePlusOneSpec(source=filename, x=x)

    SquarePlusOneProblem.of(
        input=FolderData(folder="./data"),
        process=SquarePlusOneProcessor(),
        output=Resultsfile()
    ).solve()

@print_function_header
def solve_with_lambdas():
    """ use the problem class with chaining or with a factory """

    class LambdaProcessor(Processor):
        def __init__(self, func: Callable[[int], int]):
            self.func = func
        def apply(self, process_data: SquarePlusOneSolution) -> SquarePlusOneSolution:
            return replace(process_data, y=self.func(process_data.x))

    print(f" 1| use lambda processor")
    SquarePlusOneProblem.of(
        input=ConfigData(initial_x=2),
        process=LambdaProcessor(lambda x: x ** 2 + 1),
        output=Console()
    ).solve()


@print_function_header
def solve_with_decorated_processors():
    """ measure time """

    class TimingProcessor(Processor[SquarePlusOneSolution]):
        """ measures and prints the elapsed time of an inner processor """

        def __init__(self, inner: Processor) -> None:
            self.inner = inner

        def apply(self, process_data: SquarePlusOneSolution) -> SquarePlusOneSolution:
            t0 = time.perf_counter()
            result = self.inner.apply(process_data)
            dt_ms = (time.perf_counter() - t0) * 1000
            print(f"duration ({self.inner.__class__.__name__}): {dt_ms:.4f} ms")
            return result

    print(f" 1| measure time")
    SquarePlusOneProblem.of(
        input=ConfigData(initial_x=3),
        process=TimingProcessor(SquarePlusOneProcessor()),
        output=Console()
    ).solve()

    class Verification(Processor[SquarePlusOneSolution]):
        """ check """

        def __init__(self, inner: Processor, expected_y: int) -> None:
            self.inner = inner
            self.expected_y = expected_y

        def apply(self, process_data: SquarePlusOneSolution) -> SquarePlusOneSolution:
            result = self.inner.apply(process_data)
            check = (result.y == self.expected_y)
            print(f"duration ({self.inner.__class__.__name__}): {check}")
            return result

    print(f" 2| checked")
    SquarePlusOneProblem.of(
        input=ConfigData(initial_x=3),
        process=Verification(SquarePlusOneProcessor(), expected_y=10),
        output=Console()
    ).solve()


@print_function_header
def solve_with_multiple_input_and_output():
    """ default problem solver """

    print(f" 1| multiple output")

    class Logfile(Consumer):
        def write(self, output_data: SquarePlusOneResult) -> None:
            print(f"write '{output_data}' to 'log'")

    SquarePlusOneProblem.of(
        input=ConfigData(initial_x=2),
        process=SquarePlusOneProcessor(),
        output=Tee(Console(), Logfile())
    ).solve()

    class Environment(Producer[SquarePlusOneSpec]):
        def read(self, input_data: SquarePlusOneSpec) -> Iterator[SquarePlusOneSpec]:
            # read data from .env if available
            yield replace(input_data, source=".env", x=3)

    print(f" 2| merged input")
    SquarePlusOneProblem.of(
        input=Merge(ConfigData(initial_x=2), Environment()),
        process=SquarePlusOneProcessor(),
        output=Console()
    ).solve()


@print_function_header
def solve_with_chained_processors():
    """ """
    print(f" 1| chained processors")

    # this needs y to be initialized with x at start (see ProcessData.of)
    class SquareProcessor(Processor[SquarePlusOneSolution]):
        def apply(self, process_data: SquarePlusOneSolution) -> SquarePlusOneSolution:
            return replace(process_data, y=process_data.y ** 2) # continue work from y

    class AddOneProcessor(Processor[SquarePlusOneSolution]):
        def apply(self, process_data: SquarePlusOneSolution) -> SquarePlusOneSolution:
            return replace(process_data, y=process_data.y + 1) # continue work from y

    SquarePlusOneProblem.of(
        input=ConfigData(initial_x=2),
        process=Chain(SquareProcessor(),AddOneProcessor()),
        output=Console()
    ).solve()


@print_function_header
def solve_with_parallel_processors():
    """ parallel processing """

    class Alg1Processor(Processor[SquarePlusOneSolution]):
        def apply(self, process_data: SquarePlusOneSolution) -> SquarePlusOneSolution:
            return replace(process_data, y=process_data.x ** 2 + 1)
    class Alg2Processor(Processor[SquarePlusOneSolution]):
        def apply(self, process_data: SquarePlusOneSolution) -> SquarePlusOneSolution:
            return replace(process_data, y=1 + process_data.x ** 2)

    class Parallel(Processor[SquarePlusOneSolution]):
        def __init__(self, *items: Processor[SquarePlusOneSolution]) -> None:
            if not all(isinstance(item, Processor) for item in items):
                raise TypeError("items must all be Processor")
            self.processors: tuple[Processor[SquarePlusOneSolution], ...] = items

        def apply(self, process_data: SquarePlusOneSolution) -> SquarePlusOneSolution:
            # start all (or in parallel if you want)
            results = [processor.apply(process_data) for processor in self.processors]
            # reduce (for threads, after join)
            y = max((p.y for p in results))
            return replace(process_data, y=y)

    print(f" 1| fan-out processors")
    SquarePlusOneProblem.of(
        input=ConfigData(initial_x=2),
        process=Parallel(Alg1Processor(),Alg2Processor()),
        output=Console()
    ).solve()


@print_function_header
def solve_in_stages():
    """ Stage 1: x → x²+1 ;  Stage 2: y → 2·y .  Output of stage 1 becomes input of stage 2. """

    print(f" 1| standard stream")
    stage1 = SquarePlusOneProblem.of(
        input=ConfigData(initial_x=2),
        process=SquarePlusOneProcessor(),
        output=Console()
    ).stream()

    class Stage1Data(Producer[SquarePlusOneSpec]):
        """ feed an upstream pipeline's results into a downstream pipeline """

        def __init__(self, upstream_stream):
            self.upstream = upstream_stream

        def read(self, input_data: SquarePlusOneSpec) -> Iterator[SquarePlusOneSpec]:
            for result in self.upstream:
                yield replace(input_data, source=result.source, x=result.y)

    class Double(Processor[SquarePlusOneSolution]):
        def apply(self, process_data: SquarePlusOneSolution) -> SquarePlusOneSolution:
            return replace(process_data, y=process_data.x * 2)

    # Stage 2: x = 10 (from stage 1) → y = 20
    print(f" 2| stage 2")
    SquarePlusOneProblem.of(
        input=Stage1Data(stage1),
        process=Double(),
        output=Console()
    ).solve()


@dataclass
class RuntimeArgs:
    dry_run: bool = False

runtime_args_ctx: ContextVar[RuntimeArgs] = ContextVar('runtime_args_ctx')

@print_function_header
def solve_with_runtime_args():
    """ solver workflow, compare to the workflow before """

    class DryRunConsumer(Consumer[SquarePlusOneResult]):
        def write(self, output_data: SquarePlusOneResult) -> None:
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
            input=ConfigData(initial_x=3),
            process=SquarePlusOneProcessor(),
            output=DryRunConsumer()
        ).solve()


@print_function_header
def solve_with_incomplete_pipeline():
    """ default problem solver """

    print(f" 1| standard")
    SquarePlusOneProblem.of(
        input=ConfigData(initial_x=2),
        # process=SquarePlusOneProcessor(),
        # output=Console()
    ).solve()


# Test examples

# import pytest
#
#
# def test_ConstantProducer_read():
#     """ test that the producer creates valid InputData """
#     producer = ConstantProducer(initial_x=23)
#     result = list(producer.read(InputData()))
#     assert len(result) == 1 and result[0].x == 23
#
#
# def test_SquarePlusOneProcessor_results():
#     """ test that the producer creates valid InputData """
#     result = SquarePlusOneProblem.of(
#         input=ConstantProducer(initial_x=3),
#         process=SquarePlusOneProcessor(),
#         output=DiscardConsumer()
#     ).solve()
#     assert len(result) == 1 and result[0].y==10
#
#
# def test_subclass_without_type_args_fails():
#     """ forgetting [I, P, O] is caught at class-definition time """
#     with pytest.raises(TypeError, match="must be parameterized"):
#         class BrokenProblem(IPO):       # noqa: F841 — defining the class is the test
#             pass
#
#
# def run_tests():
#     """ pytest entry — also: uv run pytest 0x_tra_gropros/snippets/b_ipo/c_examples.py -v """
#     pytest.main([__file__, "-v"])


if __name__ == "__main__":
    solve_straight()
    solve_with_file_io()
    solve_with_lambdas()
    solve_with_decorated_processors()
    solve_with_multiple_input_and_output()
    solve_with_chained_processors()
    solve_with_parallel_processors()
    solve_in_stages()
    solve_with_runtime_args()
    solve_with_incomplete_pipeline()
    # run_tests()
