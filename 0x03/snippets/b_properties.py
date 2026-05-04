# (C) A.Voss, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet discusses properties — Python's @property decorator and the
property() function — and the backing-field convention.

Teaching focus
  - pros and cons of properties
  - hand-made getter/setter via property(...)
  - the @property / @<name>.setter decorator pair
  - backing fields (`_name`, `_age`) as a convention
  - validation in setters

Properties
  - Like C#, Python allows you to define special getters and setters, called
    properties, which can be used to access attributes. However, there are
    no automatic backing fields.
  - Their main purpose is access control, of course. But they are also
    syntactic sugar for traditional getters and setters.
  - A common use case is validation in the setter, e.g. checking that an
    age value is non-negative before assigning it.
  - See https://docs.python.org/3/library/functions.html#property

See also
  - a_class_basics.py — for __dict__, class vs instance attributes,
    and the public / _protected / __private naming convention.
  - preview_getattribute.py — for overriding attribute access via
    __getattribute__.
"""

from utils import print_function_header


"""
Topic: Properties
"""


class PersonWithProperties:
    """ Person class demonstrating properties """

    def __init__(self, name, age):
        self._name = name                   # now protected
        self._age = age
        self._artist = False

    def __repr__(self):
        return f"({self.__dict__})"

    def my_get_name(self) -> str:           # 'hand-made' getter and setter
        """ name getter """
        print(f" a|   name getter '{self._name}'")
        return self._name

    def my_set_name(self, value: str) -> None:
        """ name setter """
        print(f" b|   name setter '{self._name}', new '{value}'")
        self._name = value

    name = property(my_get_name, my_set_name, None, "my doc str")       # properties

    artist = property(lambda self: self._artist,
                      lambda self, val: setattr(self, '_artist', val))  # error for 'self._tag = val'

    @property                               # another way defining a getter
    def age(self):
        """ I'm the 'age' property """
        print(f" c|   age getter '{self._age}'")
        return self._age

    @age.setter                             # 'name'.setter
    def age(self, value):
        """ I'm the 'age' property setter """
        print(f" d|   age setter '{self._age}', new '{value}'")
        if value < 0:
            raise ValueError("Age cannot be negative")
        self._age = value


@print_function_header
def show_properties():
    """ work with properties """

    hp = PersonWithProperties(name="Hans-Peter K.", age=46)
    print(f" 1| {hp=}")

    name = hp.name
    age = hp.age
    artist = hp.artist
    print(f" 2| {name=}, {age=}, {artist=}")

    hp.name = "Horst S."
    hp.age = 57
    hp.artist = True

    print(f" 3| {hp=}")

    try:
        hp.age = -1                         # triggers ValueError from validation
    except ValueError as e:
        print(f" 4| validation: {e}")


if __name__ == '__main__':
    show_properties()
