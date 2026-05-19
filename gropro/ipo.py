# (C) Alexander Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
Here the IPO framework is defined.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterator, Generic, TypeVar, Protocol, get_args
try:
    from typing import Self
except ImportError:                                  # Python < 3.11
    from typing_extensions import Self
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
    def apply(self, process_data: P) -> P: ...


class Consumer(ABC, Generic[O]):
    """ a consumer such as a file writer """
    @abstractmethod
    def write(self, output_data: O) -> None: ...


class Tee(Consumer[O]):
    """ multiple consumers """
    def __init__(self, *items: Consumer[O]) -> None: # producers: list[Producer[I]]
        if not all(isinstance(item, Consumer) for item in items):
            raise TypeError("items must all be Consumers")
        self.consumers: tuple[Consumer[O], ...] = items
    def write(self, output_data: O) -> None:
        for consumer in self.consumers:
            consumer.write(output_data)


class Merge(Producer[I]):
    """ multiple producers """
    def __init__(self, *items: Producer[I]) -> None:
        if not all(isinstance(item, Producer) for item in items):
            raise TypeError("items must all be Producers")
        self.producers: tuple[Producer[I], ...] = items

    def read(self, input_data: I) -> Iterator[I]:
        for producer in self.producers:
            for partial in producer.read(input_data):
                input_data = partial
            logger.debug(f" I|   - {f'read from {producer.__class__.__name__}:':<40} {input_data}")
        yield input_data


class Chain(Processor[P]):
    """ multiple processors """
    def __init__(self, *items: Processor[P]) -> None:
        if not all(isinstance(item, Processor) for item in items):
            raise TypeError("items must all be Processor")
        self.processors: tuple[Processor[P], ...] = items

    def apply(self, process_data: P) -> P:
        for processor in self.processors:
            process_data = processor.apply(process_data)
            logger.debug(f" P|   - {f'processed by {processor.__class__.__name__}:':<40} - {process_data}")
        return process_data


class EchoProducer(Producer[I]):
    """ a producer that echoes its input """
    def read(self, input_data: I) -> Iterator[I]:
        yield input_data


class IdentityProcessor(Processor[P]):
    """ a processor that does nothing """
    def apply(self, process_data: P) -> Iterator[P]:
        return process_data


class DiscardConsumer(Consumer):
    """ a consumer that discards its output """
    def write(self, output_data: O) -> None:
        pass


class BaseIPO(ABC, Generic[I, P, O]):
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

class IPO(BaseIPO[I,P,O]):
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
        if cls.process_data_class is None or cls.output_data_class is None:
            raise TypeError(
                f"{cls.__name__} must be parameterized with data classes: "
                f"class {cls.__name__}(IPOProblem[InputData, ProcessData, OutputData]): ..."
            )

    def __init__(self) -> None:
        self.producer: Producer = EchoProducer()
        self.processor: Processor = IdentityProcessor()
        self.consumer: Consumer = DiscardConsumer()

    def input(self, producer: Producer) -> Self:
        self.producer = producer
        return self

    def process(self, processor: Processor) -> Self:
        self.processor = processor
        return self

    def output(self, consumer: Consumer) -> Self:
        self.consumer = consumer
        return self

    def solve(self) -> list[O]:
        return list(self.stream())

    def stream(self) -> Iterator[O]:
        missing = [name for name, slot in
                   (("input", self.producer),
                    ("process", self.processor),
                    ("output", self.consumer)) if not slot]
        if missing:
            raise RuntimeError(
                f"{type(self).__name__} pipeline incomplete: missing {', '.join(missing)}"
            )
        input_data_base = self.input_data_class()
        for input_data in self.producer.read(input_data_base):
            process_data = self.process_data_class.of(input_data)
            logger.debug(f" I| - {f'read from {self.producer.__class__.__name__}:':<40} {input_data}")

            process_data = self.processor.apply(process_data)
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
