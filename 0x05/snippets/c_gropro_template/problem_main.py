# (C) 2025 Alexander Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
Here the main problem is defined and solved.
"""

# import problem data, IPO framework and components
from problem_a_data import RuntimeArgs      # InputData, ProcessData, OutputData
from problem_b_ipo import IPOProblem        # Producer, Processor, Consumer
from problem_c_io import ConstantProducer, ConsoleConsumer
from problem_c_solver import SimpleProcessor


class SquareProblem(IPOProblem):
    """ the problem to solve """


def main():
    """ create a problem instance, configure and solve it. """
    print("\nmain\n====")

    runtime_args = RuntimeArgs(debug=True)
    SquareProblem.create(
        input=ConstantProducer(initial_x=2),
        process=SimpleProcessor(),
        output=ConsoleConsumer()
    ).solve(runtime_args)


if __name__ == "__main__":
    main()
