# (C) Alexander Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
Here the IPO framework is defined.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
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
    def read(self, input_data: I) -> Iterator[I]: ...

class Processor(ABC, Generic[P]):
    """ component to solve the original problem or parts of it """
    @abstractmethod
    def apply(self, process_data: P) -> Iterator[P]: ...

class Consumer(ABC, Generic[O]):
    """ a consumer such as a file writer """
    @abstractmethod
    def write(self, output_data: O) -> None: ...

F = TypeVar('F')

def flatten(*items: F | list[F] | tuple[F, ...]) -> tuple[F, ...]:
    """ accept (a, b, c) or ([a, b, c]) → tuple """
    if len(items) == 1 and isinstance(items[0], (list, tuple)):
        return tuple(items[0])
    return items                                      # type: ignore[return-value]


def split_role(
    *items: Producer[I] | Processor[P] | Consumer[O]
            | list[Producer[I] | Processor[P] | Consumer[O]]
            | tuple[Producer[I] | Processor[P] | Consumer[O], ...],
) -> tuple[tuple[Producer[I], ...], tuple[Processor[P], ...], tuple[Consumer[O], ...]]:
    """ flatten + classify; one of the returned tuples is always empty """
    items = flatten(*items)
    if not items:
        raise ValueError("split_role() requires at least one argument")
    if all(isinstance(x, Producer) for x in items):
        return items, (), ()                              # ype: ignore[return-value]
    if all(isinstance(x, Processor) for x in items):
        return (), items, ()                                  # ype: ignore[return-value]
    if all(isinstance(x, Consumer) for x in items):
        return (), (), items                                 # ype: ignore[return-value]
    raise TypeError("split_role(): items must all be Producers OR all Processors OR all Consumers")

class Fan(Producer[I],Processor[P],Consumer[O]):
    def __init__(self, *items: Producer[I] | Processor[P] | Consumer[O]
                | list[Producer[I] | Processor[P] | Consumer[O]]
                | tuple[Producer[I] | Processor[P] | Consumer[O], ...]
                 ) -> None: # producers: list[Producer[I]]
        producers, processors, consumers = split_role(*items)
        self.producers: tuple[Producer[I], ...] = producers
        self.processors: tuple[Processor[P], ...] = processors
        self.consumers: tuple[Consumer[O], ...] = consumers

    def read(self, input_data: I) -> Iterator[I]:
        for producer in self.producers:
            yield from producer.read(input_data)

    def apply(self, process_data: P) -> Iterator[P]:
        for processor in self.processors:
            yield from processor.apply(process_data)

    def write(self, output_data: O) -> None:
        for consumer in self.consumers:
            consumer.write(output_data)

class Chain(Producer[I],Processor[P]):
    def __init__(self, *items: Producer[I] | Processor[P]
                | list[Producer[I] | Processor[P]]
                | tuple[Producer[I] | Processor[P], ...]
                 ) -> None:
        producers, processors, consumers = split_role(*items)
        self.producers: tuple[Producer[I], ...] = producers
        self.processors: tuple[Processor[P], ...] = processors

    def read(self, input_data: I) -> Iterator[I]:
        base = input_data
        for producer in self.producers:
            for partial in producer.read(base):
                base = partial
        yield base

    def apply(self, process_data: P) -> Iterator[P]:
        base = process_data
        for processor in self.processors:
            for partial in processor.apply(base):
                base = partial
        yield base

class EchoProducer(Producer[I]):
    def read(self, input_data: I) -> Iterator[I]:
        yield input_data

class IdentityProcessor(Processor[P]):
    def apply(self, process_data: P) -> Iterator[P]:
        yield process_data

class DiscardConsumer(Consumer):
    def write(self, output_data: O) -> None:
        pass


class IPO(ABC, Generic[I, P, O]):
    """ base interface for an IPO problem """

    @abstractmethod
    def input(self, producer: Producer) -> Self: ...

    @abstractmethod
    def process(self, processor: Processor) -> Self: ...

    @abstractmethod
    def output(self, consumer: Consumer) -> Self: ...

    @abstractmethod
    def solve(self) -> list[O]: ... # ResultData[I,P,O]

    @abstractmethod
    def stream(self) -> Iterator[O]: ...


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
        self.producer: Producer = EchoProducer() #  | None = None # list[Producer] = []
        self.processor: Processor = IdentityProcessor() # | None = None # list[Processor] = []
        self.consumer: Consumer = DiscardConsumer() # | None = None # list[Consumer] = []

    # def input(self, producers: Producer | list[Producer]) -> Self:
    #     self.producers = [producers] if isinstance(producers, Producer) else producers
    #     return self
    def input(self, producer: Producer) -> Self:
        self.producer = producer
        return self

    def process(self, processor: Processor) -> Self:
        self.processor = processor # [processors] if isinstance(processors, Processor) else processors
        return self

    def output(self, consumer: Consumer) -> Self:
        self.consumer = consumer # [consumers] if isinstance(consumers, Consumer) else consumers
        return self

    def solve(self) -> list[O]:
        return list(self.stream())

    def stream(self) -> Iterator[O]:
        # fail fast on a half-wired pipeline instead of silently returning []
        missing = [name for name, slot in
                   (("input", self.producer),
                    ("process", self.processor),
                    ("output", self.consumer)) if not slot]
        if missing:
            raise RuntimeError(
                f"{type(self).__name__} pipeline incomplete: missing {', '.join(missing)}"
            )

        #  InputData must be constructible with no arguments (all fields have defaults).
        input_data_base = self.input_data_class()
        for input_data in self.producer.read(input_data_base):
            logger.debug(f" I| - {f'read from {self.producer.__class__.__name__}:':<40} {input_data}")

            process_data_base = self.process_data_class.of(input_data)
            for process_data in self.processor.apply(process_data_base):
                logger.debug(f" P| - {f'processed by {self.processor.__class__.__name__}:':<40} - {process_data}")

                output_data = self.output_data_class.of(input_data, process_data)

                logger.debug(f" C| - {f'write to {self.consumer.__class__.__name__}:':<40} {output_data}")
                self.consumer.write(output_data)

                yield output_data

    @classmethod
    def of(cls,
           input: Producer = EchoProducer(),  # pylint: disable=redefined-builtin
           process: Processor = IdentityProcessor(),
           output: Consumer = DiscardConsumer(),
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
