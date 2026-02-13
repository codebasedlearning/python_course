# (C) 2025 Alexander Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
Here all problem-specific data classes are defined.
"""

from dataclasses import dataclass
from typing import Self


@dataclass
class RuntimeArgs:
    """ control run-time options """
    debug: bool = False
    # verbosity: int = 0
    # ... etc.


@dataclass
class InputData:
    """ input data such as file content or console input """
    source: str
    x: int


@dataclass
class ProcessData:
    """ process data needed for solving the problem """
    y: int = 0

    @classmethod
    def of(cls, input_data: InputData) -> Self:
        """ factory method to create ProcessData from InputData """
        return cls(y=input_data.x)


@dataclass
class OutputData:
    """ output data for writing the results to a file or console """
    source: str
    x: int
    y: int

    @classmethod
    def of(cls, input_data: InputData, process_data: ProcessData) -> Self:
        """ factory method to create OutputData from InputData and ProcessData """
        return cls(source=input_data.source, x=input_data.x, y=process_data.y)
