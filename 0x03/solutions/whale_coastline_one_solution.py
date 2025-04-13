# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
Task 'Whale Coastline'

Topics
  - class
  - data class
  - property
"""

from dataclasses import dataclass

# classical approach
#
# class Pet:
#     """ Simple pet class """
#     def __init__(self, name, age):
#         self.name = name
#         self.age = age

@dataclass
class Pet:
    """ Simple pet (data) class """
    name: str
    age: int

    @property
    def is_senior(self):
        """ returns True if age >= 7 """
        return self.age >= 7

    def celebrate_birthday(self):
        """ increments age by 1 """
        self.age += 1

    def __repr__(self):
        return f"({self.__dict__})"

def pet_test():
    """ test Pet class and properties """
    p = Pet("Fluffy", 6)
    print(f" 1| {p=}, {p.age=}, {p.is_senior=}")

    p.celebrate_birthday()
    print(f" 2| {p=}, {p.age=}, {p.is_senior=}")

if __name__ == '__main__':
    pet_test()
