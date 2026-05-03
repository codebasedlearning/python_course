# (C) A.Voss, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet discusses ...

Teaching focus
  - getatribute
"""


from utils import print_function_header

class AdultPerson:
    """ is allowed to see any film in the cinema """

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __getattribute__(self, attr_name):  # rarely overwritten...
        if attr_name != "age" or super().__getattribute__('age') >= 18:
            return super().__getattribute__(attr_name)
        return 18


@print_function_header
def access_every_cinema():
    """ replace or patch attributes at runtime """

    harry = AdultPerson(name="Dirty Harry", age=16)

    print(f" 1| {harry.__dict__}, "
          f"name: '{harry.name}', age: {harry.age}... or, real-age: {harry.__dict__['age']}\n")

if __name__ == "__main__":
    access_every_cinema()
