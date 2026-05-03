# (C) Alexander Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet discusses the idea behind the general IPO approach.

Teaching focus
  - IPO idea

Simple Model problem:
  - Calculate the root x0 for a given linear equation ax+b=0,
    given by the coefficients a, b.
"""

from utils import print_function_header


class RootProblem:
    """ This class is representative of commonly submitted solutions in terms of content and structure. """

    def __init__(self, source):
        self.a = 0.0                        # init problem data
        self.b = 0.0
        self.x0 = 0.0
        self.source = source

    def get_data(self):
        """ read data from a source, maybe a file """
        self.a = 3.0                        # 3x + 4.5 = 0 => x0 = -1.5
        self.b = 4.5
        print(f" -> read coefficients a={self.a}, b={self.b} from '{self.source}'")

    def get_root(self):
        """ solve the problem and print the solution """
        print(f" -> solve ({self.a})x + ({self.b}) = 0...", end='')
        if self.a==0:
            raise ValueError("a=0, no solution")
        self.x0 = (-self.b) / self.a
        print(f" => x={self.x0}")
        dest = self.source.replace(".in",".out")
        print(f" -> write 'a={self.a}, b={self.b}, x0={self.x0}' to '{dest}'")

@print_function_header
def typical_solution():
    """ main sequence """

    problem = RootProblem(source="data.in")
    problem.get_data()
    problem.get_root()

"""
What could be improved here?

---

Perhaps with a view to SOLID?

Single Responsibility: 
    Class does too many things: input, process, and output all mixed.
Open/Closed: 
    Hard to extend without modifying the existing class (e.g., change input format, new output destination).
Liskov Substitution: 
    No way to substitute for part of the behavior (e.g., alternative solvers, or new processing steps).
Interface Segregation: 
    No interfaces at all; client code (the main) is tied to the big bloated methods.
Dependency Inversion: 
    Depends directly on low-level details (how it reads, how it writes, how it computes), not abstractions.
"""

if __name__ == "__main__":
    typical_solution()
