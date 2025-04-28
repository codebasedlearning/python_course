# (C) 2025 Alexander Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
Here the main solver (=processor) for the IPO framework is defined.
"""

# import problem data and IPO framework
from problem_a_data import RuntimeArgs, ProcessData     # InputData, OutputData
from problem_b_ipo import  Processor                    # IPOSolver, Producer, Consumer

# pylint: disable=too-few-public-methods
# pylint: disable=missing-class-docstring


class SimpleProcessor(Processor):
    def apply(self, process_data: ProcessData, runtime_args: RuntimeArgs) -> ProcessData:
        if runtime_args.debug:
            print("======> square, dt=0.005")   # just an example
        return ProcessData(y = process_data.y ** 2 + 1)
