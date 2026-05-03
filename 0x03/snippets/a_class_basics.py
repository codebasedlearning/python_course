# (C) A.Voss, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet discusses classes, initializers, methods, __dict__, and instance creation.

Teaching focus
  - create instances
  - learn the concept of dynamic data
  - __str__ vs __repr__ in different contexts
  - internals of instance creation
  - __new__, __init__, __del__

Class
  - Python classes provide all the standard features of Object Oriented Programming:
      - the class inheritance mechanism allows multiple base classes,
      - a derived class can override any methods of its base class or classes,
      - and a method can call the method of a base class with the same name.
  - Objects can contain arbitrary amounts and kinds of data. As is true for modules,
    classes partake of the dynamic nature of Python:
      - they are created at runtime,
      - and can be modified further after creation.
  - Creating a new class creates a new type of object, allowing new instances
    of that type to be made. Each class instance can have attributes attached
    to it for maintaining its state.
  - Class instances can also have methods (defined by its class) for modifying its state.
  - In C++ terminology, normally class members (including the data members)
    are public (except see below Private Variables), and all member functions
    are virtual.
  - The method function is declared with an explicit first argument representing
    the object, which is provided implicitly by the call. As in Smalltalk,
    classes themselves are objects. This provides semantics for importing and renaming.
  - Unlike C++ [...] built-in types can be used as base classes for extension by
    the user. Also, like in C++, most built-in operators with special syntax
    (arithmetic operators, subscripting etc.) can be redefined for class instances.
  - https://docs.python.org/3/tutorial/classes.html

Methods
  - As already noted before, methods get an explicit argument, called 'self',
    which contains the reference to the object from which the method was called.
    This is the same in C++, except that 'this' is not included in the signature.

Self
  - Suppose you want to return a reference to the object with which the method
    was called _and_ also express this in the signature. Then you can use the
    class name, of course, but this is no longer useful if the method was
    overwritten in derived classes and you want to call methods of the subclass,
    e.g. when chaining.
  - PEP 673 https://peps.python.org/pep-0673/
    makes this possible, but only since Python 3.11. Before that you had to
    import 'typing' and 'Self' from typing import Self.

__str__, __repr__
  - There are predefined names for operators or special methods, here the
    counterpart for 'toString', a representation of the object for the user.
    You can recognise these functions by the two '__', double underscore,
    or short 'dunder'...
  - A similar internal function is '__repr__', which creates a representation
    of the object that contains all the essential properties.
  - In contrast to '__repr__' the function '__str__' is more informal and
    suitable for output. The print statement uses __str__ to display an instance.
    In the course we will get to know more internal methods, such as operators.

__new__, __init__
  - In fact, the process of creating and initialising an instance consists
    of several steps.
    From Python doc https://docs.python.org/3/reference/datamodel.html#basic-customization
      - __new__(cls[, ...]) is called to create a new instance of class cls.
        __new__() is a static method (special-cased so you need not declare it
        as such) that takes the class of which an instance was requested as its
        first argument.
      - __init__(self[, ...]) is called after the instance has been created
        (by __new__()), but before it is returned to the caller.
      - __new__() is intended mainly to allow subclasses of immutable types
        (like int, str, or tuple) to customize instance creation.
  - Python's '__new__' is nothing more and nothing less than similar per-class
    customisation of the "allocate a new instance" part. This of course allows
    you to do unusual things such as returning an existing instance rather than
    allocating a new one. So in Python, we shouldn't really think of this part
    as necessarily involving allocation; all that we require is that '__new__'
    comes up with a suitable instance from somewhere.
  - In contrast, Python's '__init__' initialises the attributes of an already
    constructed instance, referred to by 'self'.
  - Python is not the only programming language in which it is possible to
    separate these two steps, as is the case in C++, for example (new operator,
    calling class::class()).
    However, in most known OO languages, an expression like 'Class(args)'
    combines object creation and initialisation. It is called a 'constructor'.
    Even though this is not 100% correct from a technical point of view,
    we will tolerate this name when we talk about the '__init__' method
    because of the similarity to existing OOP concepts.
  - In addition, the definition of a custom '__new__' is a rare event,
    and in almost all situations the standard 'object.__new__' will be
    sufficient.

__del__ (Destructors)
  - Python also has destructors.
  - From Python doc https://docs.python.org/3/reference/datamodel.html#basic-customization
      - '__del__(self)' is called when the instance is about to be destroyed.
        This is also called a 'destructor'.
    It is only called when its reference count reaches zero. Some common
    situations may prevent the reference count of an object from going to
    zero, e.g. circular references between objects.
  - According to https://docs.python.org/3/reference/datamodel.html
    the only required property of Python's garbage collection is that it
    happens after all references have been deleted, so it need not happen
    immediately afterwards, and may not happen at all.

pylint, error `too-few-public-methods`
  - The class defines fewer public methods than the threshold specified by
    Pylint (default is 2 methods). Pylint considers that a class with too few
    public methods might be better represented as a simpler structure, such as
    a function or a named tuple, depending on its purpose.

"""

import sys
from utils import print_function_header


"""
Topic: Class basics
"""


class TeamMember:
    """ simple team member class """        # class doc string

    def __init__(self, name: str, born_in: int):    # initializer (ctor), self = this
        self.name = name                    # instance attributes
        self.born_in = born_in
        print(f" a|   TeamMember.init: {self.name=}, {self.born_in=}")

    def greetings(self):                    # methods, self
        """ greetings from name """
        print(f" b|   TeamMember.greetings: Hello, I am {self.name}, born in {self.born_in}.")
        return self

    def __repr__(self):                     # Comment out and cmp the output.
        return f"('{self.name}', * {self.born_in})"


@print_function_header
def create_team():
    """ first class instances """

    alice = TeamMember("Alice", 2005)       # What is most readable?
    alice.greetings()                                       # Call a member functions.
    print(f" 1| {alice=}, {alice.name=}, {alice.born_in=}") # Access member vars.

    bob = TeamMember(name="Bob", born_in=2007)      # or this?
    bob.greetings()
    print(f" 2| {bob=}, {bob.name=}, {bob.born_in=}")

    TeamMember("Charly", born_in=1999).greetings()  # chaining


@print_function_header
def understand_instance_data():
    """ discuss instance and dynamic data in __dict__ """

    alice = TeamMember("Alice", 2005)
    bob = TeamMember(name="Bob", born_in=2007)

    print(f" 1| {alice.__dict__=}")         # Key moment, an important observation.
    print(f" 2| {bob.__dict__=}")

    alice.has_a_sister = True               # This is about understanding, not best practice!
    bob.has_a_brother = False               # warning from pylint

    print(f" 3| {alice.has_a_sister=}, {bob.has_a_brother=} -> it works")
    print(f" 4| {alice.__dict__=}")
    print(f" 5| {bob.__dict__=}")

    del alice.born_in                       # Even removing works.
    del alice.has_a_sister
    print(f" 5| {alice.__dict__=}")


class Person:
    """ simple person class """             # class doc string

    being_old = 99

    def __init__(self, surname: str, age: int):     # initializer (ctor), self = this
        self.surname = surname              # instance attributes
        self.age = age

    def one_year_older(self):
        """ increases age by one """
        self.age += 1
        if self.age > Person.being_old:
            print(f" b|   Respect, {self.surname}!")
        return self

    def celebrate(self): # -> Self:
        """ celebrate birthday """
        print(f" c|   Person.celebrate: Happy {self.age}th birthday, {self.surname}!")
        return self

    def __repr__(self):
        return f"{self.__dict__}"


@print_function_header
def show_class_data():
    """ more class instances """

    print(f" 1| {Person.__dict__=}")

    mary = Person("Mary", age=25)
    print(f" 2| {Person.being_old=}, {mary=}, {mary.being_old=}") # Person.being_old accessible by instance.
    mary.one_year_older()                   # nothing happens
    print(f" 3| {Person.being_old=}, {mary=}, {mary.being_old=}")

    Person.being_old = 18
    print(f" 4| {Person.__dict__=}")

    print(f" 5| {Person.being_old=}, {mary=}, {mary.being_old=}")
    #print(f" 2| {Person.__dict__=}")

    mary.one_year_older()  # class-data has changed
    print(f" 6| {Person.being_old=}, {mary=}, {mary.being_old=}")

    mary.being_old = 33
    print(f" 7| {Person.being_old=}, {mary=}, {mary.being_old=}")


class Animal:
    """ class with both __str__ and __repr__ """

    def __init__(self, species: str, legs: int):
        self.species = species
        self.legs = legs

    def __str__(self):
        return f"|{self.species}, {self.legs}| [__str__]"

    def __repr__(self):
        return f"({self.species}, {self.legs}) [__repr__]"


@print_function_header
def show_str_vs_repr():
    """ __str__ vs __repr__ — who calls what? """

    cat = Animal("Cat", 4)

    print(f" 1| {cat}")
    print(f" 2| {cat!r}") # or repr(cat)
    print(f" 3| {cat=}")
    # !r in f-strings and repr() use __repr__

    # inside containers, elements always use __repr__
    zoo = [Animal("Dog", 4), Animal("Spider", 8)]
    print(f" 4| list: {zoo}")

    s = "Lorem ipsum"
    print(f" 5| {s}, {s!r}, {s=}")

    # when only __repr__ is defined, it serves as fallback for __str__


"""
Topic: Instance and class data
"""


class IdentPerson:
    """ simple person class """

    next_id = 1                             # class attribute

    def __init__(self, name):
        self.name = name                    # instance attribute

        # protected, with prefix '_' (convention)
        self._id = IdentPerson.next_id

        # private, two '__', not only a convention (renamed to '_Person__secret_number')
        self.__secret_number = self._id*23

        IdentPerson.next_id += 1                 # access class attribute
        print(f" a|   Person.init: {self}")

    def __str__(self):
        return f"{self.__dict__}"

    def secret(self):
        """ getter for private number """
        return self.__secret_number

    def __my_internal_secret(self):
        """ secret function """
        return self.__secret_number         # also private

    @classmethod                            # class method with decorator
    def print_next_id(cls):
        """ print class attribute """
        print(f" b|   {IdentPerson.next_id=}")


@print_function_header
def show_access_modifiers():
    """ access different attributes """

    peter = IdentPerson(name="Peter")
    print(f" 1| public:    {peter}")
    print(f" 2| protected: {peter._id=}")
    print(f" 3| private:   {peter._IdentPerson__secret_number=}, {peter._IdentPerson__my_internal_secret()=}")

    IdentPerson.print_next_id()


"""
Topic: Instance creation
"""


class TrackedPerson:
    """ person class with lifecycle tracking """
    def __new__(cls, *args, **kwargs):      # here not necessary, just to see the args
        print(f" a|   TrackedPerson.new: {cls}, {args=}, {kwargs=}")
        return super().__new__(cls)

    def __init__(self, name: str):
        self.name = name
        print(f" b|   TrackedPerson.init: {self.name=}")

    def __del__(self):
        print(f" c|   TrackedPerson.del: {self.name=}")
        # super().__del__()     # object has no __del__


@print_function_header
def show_new_and_init():
    """ see new and del in action """

    print(" 1| start")
    peter = TrackedPerson(name="Peter")
    print(f" 2| {peter.name=}")
    print(f" 3| {sys.getrefcount(peter)=}")
    vip = peter
    print(f" 4| {sys.getrefcount(peter)=}")

    if True:
        paul = TrackedPerson("Paul")
        print(f" 5| {paul.name=}")

    def inner_func():
        mary = TrackedPerson(name="Mary")
        print(f" 6| {mary.name=}")

    inner_func()
    print(" 7| end")

if __name__ == '__main__':
    create_team()
    understand_instance_data()
    show_class_data()
    show_str_vs_repr()
    show_access_modifiers()
    show_new_and_init()
