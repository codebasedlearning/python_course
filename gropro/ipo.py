# (C) Alexander Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
Here the IPO framework is defined.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Self, Iterator, Generic, TypeVar, Protocol, get_args
from contextlib import contextmanager
from contextvars import ContextVar

import logging
logger = logging.getLogger('ipo')

# pylint: disable=too-few-public-methods
# pylint: disable=missing-function-docstring

I = TypeVar('I')   # InputData
P = TypeVar('P')   # ProcessData
O = TypeVar('O')   # OutputData

class Producer(ABC, Generic[I]):
    """ a producer such as a file reader """
    @abstractmethod
    def read(self) -> Iterator[I]: ...

class Processor(ABC, Generic[P]):
    """ component to solve the original problem or parts of it """
    @abstractmethod
    def apply(self, process_data: P) -> P: ...

class Consumer(ABC, Generic[O]):
    """ a consumer such as a file writer """
    @abstractmethod
    def write(self, output_data: O) -> None: ...

@dataclass
class ResultData(Generic[I,P,O]):
    producer: Producer = None
    input_data: I = None
    process_data: P = None
    output_data: O = None

class IPO(ABC, Generic[I, P, O]):
    """ base interface for an IPO problem """

    @abstractmethod
    def input(self, producers: Producer | list[Producer]) -> Self: ...

    @abstractmethod
    def process(self, processors: Processor | list[Processor]) -> Self: ...

    @abstractmethod
    def output(self, consumers: Consumer | list[Consumer]) -> Self: ...

    @abstractmethod
    def solve(self) -> list[ResultData[I,P,O]]: ...


class HasOf(Protocol):
    @classmethod
    def of(cls, *args) -> Self: ...

class IPOProblem(IPO[I,P,O]):
    """ base implementation of an IPO problem """
    input_data_class:   type[HasOf] = None     # subclass may set this
    process_data_class: type[HasOf] = None
    output_data_class:  type[HasOf] = None

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        # Use vars(cls), NOT getattr — getattr would walk the MRO and pick up
        # IPOProblem's own IPO[I,P,O] bases, silently assigning the raw
        # TypeVars (~I, ~P, ~O) as data classes.
        for base in vars(cls).get('__orig_bases__', ()):
            args = get_args(base)
            if len(args) == 3:
                cls.input_data_class, cls.process_data_class, cls.output_data_class = args
                return
        # No [I, P, O] on this class — only fine if a parameterized parent
        # already provided them (e.g. `class Faster(SquarePlusOneProblem)`).
        if cls.process_data_class is None or cls.output_data_class is None:
            raise TypeError(
                f"{cls.__name__} must be parameterized with data classes: "
                f"class {cls.__name__}(IPOProblem[InputData, ProcessData, OutputData]): ..."
            )

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

    def solve(self) -> list[ResultData[I,P,O]]:
        # fail fast on a half-wired pipeline instead of silently returning []
        missing = [name for name, slot in
                   (("input", self.producers),
                    ("process", self.processors),
                    ("output", self.consumers)) if not slot]
        if missing:
            raise RuntimeError(
                f"{type(self).__name__} pipeline incomplete: missing {', '.join(missing)}"
            )

        results = []
        for producer in self.producers:     # or with 'chain'
            for input_data in producer.read():
                logger.debug(f" I| - {f'read from {producer.__class__.__name__}:':<40} {input_data}")

                process_data = self.process_data_class.of(input_data)
                for processor in self.processors:
                    process_data = processor.apply(process_data)
                    logger.debug(f" P| - {f'processed by {processor.__class__.__name__}:':<40} - {process_data}")

                output_data = self.output_data_class.of(input_data,process_data)
                results.append(ResultData(producer, input_data, process_data, output_data))
                for consumer in self.consumers:
                    logger.debug(f" C| - {f'write to {consumer.__class__.__name__}:':<40} {output_data}")
                    consumer.write(output_data)
        return results

    @classmethod
    def of(cls,
               input: Producer | list[Producer],        # pylint: disable=redefined-builtin
               process: Processor | list[Processor],
               output: Consumer | list[Consumer]
    ) -> Self:
        return cls() \
            .input(input) \
            .process(process) \
            .output(output)

T = TypeVar('T')

@contextmanager
def ipo_context(ctx_var: ContextVar[T], value: T):
    token = ctx_var.set(value)
    try:
        yield
    finally:
        ctx_var.reset(token)
