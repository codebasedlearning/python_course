# (C) 2025 Alexander Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
Here the IPO framework is defined.
"""

from abc import ABC, abstractmethod
from typing import Self, Iterator

# import problem data instead of making IPO generic (which is out of scope here)
from problem_a_data import RuntimeArgs, InputData, ProcessData, OutputData

# pylint: disable=too-few-public-methods
# pylint: disable=missing-function-docstring


class Producer(ABC):
    """ a producer such as a file reader """
    @abstractmethod
    def read(self, runtime_args: RuntimeArgs) -> Iterator[InputData]: ...


class Processor(ABC):
    """ component to solve the original problem or parts of it """
    @abstractmethod
    def apply(self, process_data: ProcessData, runtime_args: RuntimeArgs) -> ProcessData: ...


class Consumer(ABC):
    """ a consumer such as a file writer """
    @abstractmethod
    def write(self, output_data: OutputData, runtime_args: RuntimeArgs) -> None: ...


class IPO(ABC):
    """ base interface for an IPO problem """

    @abstractmethod
    def input(self, producers: Producer | list[Producer]) -> Self: ...

    @abstractmethod
    def process(self, processors: Processor | list[Processor]) -> Self: ...

    @abstractmethod
    def output(self, consumers: Consumer | list[Consumer]) -> Self: ...

    @abstractmethod
    def solve(self, runtime_args: RuntimeArgs) -> list[tuple[Producer,InputData,ProcessData]]: ...


class IPOProblem(IPO):
    """ base implementation of an IPO problem """

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

    def solve(self, runtime_args: RuntimeArgs = RuntimeArgs()) -> list[tuple[Producer,InputData,ProcessData]]:
        results = []
        for producer in self.producers:             # or with 'chain'
            for input_data in producer.read(runtime_args):
                if runtime_args.debug:
                    print(f" I| - {f'read from {producer.__class__.__name__}:':<30} {input_data}")

                process_data = ProcessData.of(input_data)
                if runtime_args.debug:
                    print(f" P| - {'start processing:':<30} {process_data}")
                for processor in self.processors:
                    process_data = processor.apply(process_data, runtime_args)
                    if runtime_args.debug:
                        print(f" P| - {f'processed by {processor.__class__.__name__}:':<30} - {process_data}")

                results.append((producer, input_data, process_data))
                output_data = OutputData.of(input_data, process_data)
                for consumer in self.consumers:
                    if runtime_args.debug:
                        print(f" C| - {f'write to {consumer.__class__.__name__}:':<30} {output_data}")
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
