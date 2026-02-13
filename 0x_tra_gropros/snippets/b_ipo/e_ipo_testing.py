# (C) Alexander Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet shows how to test IPO components in isolation.

Teaching focus
  - Test processors with hardcoded data (no file I/O needed)
  - Test the full pipeline with a ConstantProducer
  - Verify each phase independently before combining them

Why test IPO components?
  - The biggest advantage of the IPO split is testability. Each component has
    a clear contract: Producer yields InputData, Processor transforms ProcessData,
    Consumer writes OutputData.
  - In an exam, writing a quick test for your Processor with known input/output
    lets you verify your algorithm before wiring up file I/O.
  - You can run these tests with: python e_ipo_testing.py
    or with pytest:              pytest e_ipo_testing.py -v
"""

from dataclasses import dataclass
from typing import Self, Iterator
from abc import ABC, abstractmethod

# pylint: disable=too-few-public-methods
# pylint: disable=missing-class-docstring


# Minimal framework (same as c_ipo.py, repeated for self-containment) #
########################################################################


@dataclass
class RuntimeArgs:
    debug: bool = False


@dataclass
class InputData:
    source: str
    values: list[int]


@dataclass
class ProcessData:
    total: int = 0
    count: int = 0
    average: float = 0.0

    @classmethod
    def of(cls, input_data: InputData) -> Self:
        return cls(total=0, count=len(input_data.values))


@dataclass
class OutputData:
    source: str
    average: float

    @classmethod
    def of(cls, input_data: InputData, process_data: ProcessData) -> Self:
        return cls(source=input_data.source, average=process_data.average)


class Producer(ABC):
    @abstractmethod
    def read(self, runtime_args: RuntimeArgs) -> Iterator[InputData]: ...


class Processor(ABC):
    @abstractmethod
    def apply(self, process_data: ProcessData, runtime_args: RuntimeArgs) -> ProcessData: ...


class Consumer(ABC):
    @abstractmethod
    def write(self, output_data: OutputData, runtime_args: RuntimeArgs) -> None: ...


# Components to test #
######################


class SumProcessor(Processor):
    """ sums all values """
    def apply(self, process_data: ProcessData, runtime_args: RuntimeArgs) -> ProcessData:
        return process_data                     # sum happens in AverageProcessor


class AverageProcessor(Processor):
    """ computes average from InputData values """
    def apply(self, process_data: ProcessData, runtime_args: RuntimeArgs) -> ProcessData:
        # note: process_data.count was set in ProcessData.of()
        # but we need the actual values — this is the design tension
        # in a real scenario, ProcessData would carry the values too
        return process_data


class StatProcessor(Processor):
    """ computes sum and average in one step (more realistic) """
    def apply(self, process_data: ProcessData, runtime_args: RuntimeArgs) -> ProcessData:
        if process_data.count == 0:
            return ProcessData(total=0, count=0, average=0.0)
        return ProcessData(
            total=process_data.total,
            count=process_data.count,
            average=process_data.total / process_data.count,
        )


class ConstantProducer(Producer):
    def __init__(self, values: list[int]) -> None:
        self.values = values

    def read(self, runtime_args: RuntimeArgs) -> Iterator[InputData]:
        yield InputData(source="test", values=self.values)


class CollectingConsumer(Consumer):
    """ collects output instead of printing — useful for assertions """
    def __init__(self) -> None:
        self.results: list[OutputData] = []

    def write(self, output_data: OutputData, runtime_args: RuntimeArgs) -> None:
        self.results.append(output_data)


# Testing: manual style (no framework needed) #
################################################


def test_processor_with_hardcoded_data():
    """ test the processor in complete isolation """
    print("\ntest_processor_with_hardcoded_data\n==================================")

    processor = StatProcessor()

    # test 1: normal case
    pd = ProcessData(total=15, count=5, average=0.0)
    result = processor.apply(pd, RuntimeArgs())
    assert result.average == 3.0, f"expected 3.0, got {result.average}"
    print(f" 1| normal case:     {pd} -> average={result.average} OK")

    # test 2: single element
    pd = ProcessData(total=42, count=1, average=0.0)
    result = processor.apply(pd, RuntimeArgs())
    assert result.average == 42.0
    print(f" 2| single element:  {pd} -> average={result.average} OK")

    # test 3: empty input
    pd = ProcessData(total=0, count=0, average=0.0)
    result = processor.apply(pd, RuntimeArgs())
    assert result.average == 0.0
    print(f" 3| empty input:     {pd} -> average={result.average} OK")

    print(" 4| all processor tests passed")


def test_producer_yields_correct_data():
    """ test that the producer creates valid InputData """
    print("\ntest_producer_yields_correct_data\n=================================")

    producer = ConstantProducer(values=[10, 20, 30])
    results = list(producer.read(RuntimeArgs()))

    assert len(results) == 1
    assert results[0].values == [10, 20, 30]
    assert results[0].source == "test"
    print(f" 1| producer yields: {results[0]} OK")


def test_data_conversion_chain():
    """ test the InputData -> ProcessData -> OutputData chain """
    print("\ntest_data_conversion_chain\n==========================")

    # step 1: create InputData (as if from a Producer)
    input_data = InputData(source="exam.in", values=[4, 8, 12])
    print(f" 1| InputData:   {input_data}")

    # step 2: convert to ProcessData
    process_data = ProcessData.of(input_data)
    process_data.total = sum(input_data.values)
    print(f" 2| ProcessData: {process_data}")

    # step 3: apply processor
    processor = StatProcessor()
    process_data = processor.apply(process_data, RuntimeArgs())
    print(f" 3| after apply: {process_data}")

    # step 4: convert to OutputData
    output_data = OutputData.of(input_data, process_data)
    print(f" 4| OutputData:  {output_data}")

    # verify the full chain
    assert output_data.average == 8.0
    assert output_data.source == "exam.in"
    print(f" 5| full chain verified: average={output_data.average} OK")


def test_full_pipeline_with_collecting_consumer():
    """ test the full pipeline without printing """
    print("\ntest_full_pipeline_with_collecting_consumer\n============================================")

    # assemble components
    producer = ConstantProducer(values=[2, 4, 6, 8])
    processor = StatProcessor()
    consumer = CollectingConsumer()

    # run the pipeline manually (same logic as IPOProblem.solve)
    for input_data in producer.read(RuntimeArgs()):
        process_data = ProcessData.of(input_data)
        process_data.total = sum(input_data.values)
        process_data = processor.apply(process_data, RuntimeArgs())
        output_data = OutputData.of(input_data, process_data)
        consumer.write(output_data, RuntimeArgs())

    # verify via the collecting consumer
    assert len(consumer.results) == 1
    assert consumer.results[0].average == 5.0
    print(f" 1| pipeline result: {consumer.results[0]} OK")
    print(f" 2| CollectingConsumer captured {len(consumer.results)} result(s)")


# pytest-compatible tests (same logic, pytest conventions) #
############################################################


def test_stat_processor_normal():
    """ pytest: normal case """
    result = StatProcessor().apply(
        ProcessData(total=15, count=5), RuntimeArgs()
    )
    assert result.average == 3.0


def test_stat_processor_empty():
    """ pytest: edge case """
    result = StatProcessor().apply(
        ProcessData(total=0, count=0), RuntimeArgs()
    )
    assert result.average == 0.0


def test_collecting_consumer():
    """ pytest: verify consumer collects """
    consumer = CollectingConsumer()
    consumer.write(OutputData(source="x", average=3.14), RuntimeArgs())
    assert len(consumer.results) == 1
    assert consumer.results[0].average == 3.14


if __name__ == "__main__":
    test_processor_with_hardcoded_data()
    test_producer_yields_correct_data()
    test_data_conversion_chain()
    test_full_pipeline_with_collecting_consumer()
    print("\n\nAll tests passed.")
