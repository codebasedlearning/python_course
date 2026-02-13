# (C) 2025 Alexander Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet discusses the idea behind the general IPO approach.

Teaching focus
  - IPO idea

Model problem:
  - Calculate x^2+1 for a given x
"""


class SquareAdd1Problem:
    """ This class is representative of commonly submitted solutions in terms of content and structure. """

    def __init__(self, source):
        self.x = 0                          # init problem data
        self.y = 0
        self.source = source

    def get_data(self):
        """ read data from a source, maybe a file """
        self.x = 3
        print(f" -> read x={self.x} from '{self.source}'")

    def solve_and_print(self):
        """ solve the problem and print the solution """
        print(f" -> solve for x={self.x}...", end='')
        self.y = self.x * self.x            # x^2 + 1
        self.y += 1                         # sometimes in multiple steps
        print(f" -> y={self.y}")
        dest = self.source.replace(".in",".out")
        print(f" -> write '{self.x} -> {self.y}' to '{dest}'")

def typical_solution():
    """ main sequence """
    print("\ntypical_solution\n================")

    problem = SquareAdd1Problem(source="data.in")
    problem.get_data()
    problem.solve_and_print()

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
