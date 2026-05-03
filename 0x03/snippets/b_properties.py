# (C) A.Voss, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet discusses class attributes, access modifiers, and properties.

Teaching focus
  - working with __dict__, class and instance attributes
  - access modifiers
  - see Python possibilities, like patching attributes or methods
    at runtime (uuuh) or 'modify' the access via __getattribute__
  - pros and cons of properties
  - backing fields
  - a lot of pylint and mypy errors for didactic reasons

Public, protected and private
  - In principle, all variables in Python are accessible, i.e. you can use them
    from a technical point of view.
  - In practice, there is an agreement that 'public' elements are named without
    leading underscores, 'protected' elements, accessible in subclasses, are
    named with one underscore, and 'private' elements, accessible only to
    class members, are named with two underscores.
    You should stick to this convention.
  - Also, the Python compiler changes the name of 'private' members to
    '_+class name+attribute name'.
  - A small overview can also be found here
    https://www.tutorialsteacher.com/python/public-private-protected-modifiers

__dict__
  - In Python, it is not necessary to declare attributes beforehand, unlike
    in languages like C++ or Java. They are assigned to the instance, e.g.
    in the initialization. However, this can be done anywhere.
  - This is a very basic idea in Python. When you want to access an element,
    say `x`, `obj.y` or `z()`, there are rules by which the access is resolved.
    We will look at this in more detail later.
  - When accessing instance attributes (`y`), Python searches a dictionary
    called '__dict__'. This dictionary contains all the attributes of the
    instance. If `y` is not found there, it is looked up in the class dictionary
    (in fact, the process is a little more complicated).
  - This is why dictionaries are so important to Python. They implement
    namespaces.
  - See
    https://blog.peterlamut.com/2018/11/04/python-attribute-lookup-explained-in-detail/
  - So it is also possible to change or add attributes at runtime... but there
    should be a good discussion about the use cases. You can find something like
    this under the term 'monkey patch'
    https://stackoverflow.com/questions/5626193/what-is-monkey-patching

Class members
  - In Python classes are also objects and can also contain data. This is the
    concept of 'static', e.g. in C++ or Java.
  - A class member can be addressed via the class object, i.e. by using the
    full qualified name. In this sense, members of a class object are treated
    no differently as members of a class instance.
  - Analogous to class attributes, there are also class methods. These are
    called in the same way as the class object (note: self=this does not exist
    for static methods). The convention is that their name is 'cls' (like 'self').
  - To mark a method as a class method, so-called 'decorators' are used, e.g.
    @classmethod. You can also write these yourself, which we will do.
  - Additionally, there is also @staticmethod. This type of method takes
    neither a self nor a cls parameter
    https://realpython.com/instance-class-and-static-methods-demystified/

Properties
  - Like C#, Python allows you to define special getters and setters, called
    properties, which can be used to access attributes. However, there are
    no automatic backing fields.
  - Their main purpose is access control, of course. But they are also
    syntactic sugar for traditional getters and setters.
  - A common use case is validation in the setter, e.g. checking that an
    age value is non-negative before assigning it.
  - See https://docs.python.org/3/library/functions.html#property
  - Even Python's type hinting system shows a warning, it's better to
    use more specific types.
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
