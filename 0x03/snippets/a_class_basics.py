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

__slots__
  - By default, Python stores instance attributes in a per-instance dictionary
    called __dict__. This allows dynamic attribute creation but uses more memory.
  - __slots__ declares a fixed set of allowed attributes, replacing __dict__
    with a more compact internal structure.
  - Using __slots__ prevents adding arbitrary attributes at runtime and can
    improve memory usage and attribute access speed.


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


@print_function_header
def create_team():
    """ first class instances """

    alice = TeamMember("Alice", 2005)       # What is most readable?
    alice.greetings()
    print(f" 1| {alice=}")                  # hmmm...

    bob = TeamMember(name="Bob", born_in=2007)      # or this?
    bob.greetings()
    print(f" 2| {bob=}")

    TeamMember("Charly", born_in=1999).greetings()  # chaining


class Person:
    """ simple person class """             # class doc string

    being_old = 99

    def __init__(self, surname: str, age: int):     # initializer (ctor), self = this
        self.surname = surname              # instance attributes
        self.age = age
        print(f" a|   Person.init: {self}, {self=}")

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

    def __str__(self):
        return f"('{self.surname}', {self.age})"

    def __repr__(self):
        return f"{self.__dict__}"


@print_function_header
def create_crowd():
    """ more class instances """

    peter = Person("Peter", 23)
    peter.one_year_older().celebrate()
    print(f" 1| Peter={peter}")

    paul = Person(surname="Paul", age=24)
    paul.one_year_older().celebrate()
    print(f" 2| Paul={paul}")


class Animal:
    """ class with both __str__ and __repr__ """

    def __init__(self, species: str, legs: int):
        self.species = species
        self.legs = legs

    def __str__(self):
        return f"{self.species} ({self.legs} legs)"

    def __repr__(self):
        return f"Animal({self.species!r}, {self.legs})"


class Color:
    """ class with only __repr__, no __str__ """

    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return f"Color({self.name!r})"


@print_function_header
def show_str_vs_repr():
    """ __str__ vs __repr__ — who calls what? """

    cat = Animal("Cat", 4)

    # print() and f-strings use __str__
    print(f" 1| print uses __str__: {cat}")
    # !r in f-strings and repr() use __repr__
    print(f" 2| !r uses __repr__:   {cat!r}")
    print(f" 3| repr() call:        {repr(cat)}")

    # inside containers, elements always use __repr__
    zoo = [Animal("Dog", 4), Animal("Spider", 8)]
    print(f" 4| list uses __repr__: {zoo}")

    info = {"pet": Animal("Parrot", 2)}
    print(f" 5| dict uses __repr__: {info}")

    # when only __repr__ is defined, it serves as fallback for __str__
    red = Color("red")
    print(f" 6| fallback to __repr__: {red}")
    print(f" 7| repr still works:    {red!r}")


"""
Topic: Instance and class data
"""


@print_function_header
def show_instance_data():
    """ discuss instance and dynamic data in __dict__ """

    doro = TeamMember("Doro", born_in=2000)
    mary = Person("Mary", age=25)

    print(f" 1| {doro.__dict__=}")          # this is an important observation
    print(f" 2| {mary.__dict__=}")

    doro.has_a_sister = True                # warning from pylint
    mary.has_a_brother = True

    print(f" 3| {doro.__dict__=}")
    print(f" 4| {mary.__dict__=}")

    del doro.born_in
    del doro.has_a_sister
    print(f" 5| {doro.__dict__=}")


@print_function_header
def show_class_data():
    """ discuss class and static data """

    mary = Person("Mary", age=25)
    print(f" 1| {Person.__dict__=}")
    mary.one_year_older()                   # nothing happens

    Person.being_old = 18
    print(f" 2| {Person.__dict__=}")
    mary.one_year_older()                   # class-data has changed


class SlottedPerson:
    """ person class with __slots__ instead of __dict__ """
    __slots__ = ('name', 'age')

    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    def __repr__(self):
        return f"SlottedPerson({self.name!r}, {self.age})"


@print_function_header
def show_slots():
    """ __slots__ vs __dict__ """

    sp = SlottedPerson("Eve", 30)
    print(f" 1| {sp=}, {sp.name=}, {sp.age=}")

    try:
        sp.hobby = "chess"                  # AttributeError: no __dict__
    except AttributeError as e:
        print(f" 2| cannot add attribute: {e}")

    print(f" 3| has __dict__: {hasattr(sp, '__dict__')}")
    print(f" 4| has __slots__: {sp.__slots__=}")

    print(f" 5| {sys.getsizeof(sp)=}")
    person = Person("Alice", 20)
    print(f" 6| {sys.getsizeof(person)=}, {sys.getsizeof(person.__dict__)=})")


"""
Topic: Instance creation
"""


class TrackedPerson:
    """ person class with lifecycle tracking """
    def __new__(cls, *args, **kwargs):      # here not necessary, just to see the args
        print(f" a|   TrackedPerson.new: {cls}, {args=}, {kwargs=}")
        # return object.__new__(cls)
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

    if peter.name:
        paul = TrackedPerson("Paul")
        print(f" 3| {paul.name=}")

    def inner_func():
        mary = TrackedPerson(name="Mary")
        print(f" 4| {mary.name=}")

    inner_func()
    print(" 5| end")                        # sys.getrefcount(paul)


"""
Topic: Singleton pattern
"""


class DatabaseConnector:                    # problems?
    """ a class meant to be a singleton """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)  # Call only the first time
        return cls._instance

    def __init__(self, connection_string):
        self.connection_string = connection_string


class ServiceDetector:
    """ a class meant to be a singleton - improved """
    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, url):
        if not self._initialized:
            self.url = url
            self._initialized = True


@print_function_header
def define_a_singleton():
    """ define a singleton """

    db_connector = DatabaseConnector(connection_string="aws.com")
    database_access = DatabaseConnector(connection_string="azure.com")
    print(f" 1|    {id(db_connector)=}, connected to: '{db_connector.connection_string}'")
    print(f"    {id(database_access)=}, connected to: '{database_access.connection_string}'")

    main_service = ServiceDetector(url="//server")
    docker_service = ServiceDetector(url="//docker")
    print(f" 2|   {id(main_service)=}, ask here: '{main_service.url=}'")
    print(f"    {id(docker_service)=}, ask here: '{docker_service.url=}'")


@print_function_header
def last_function():
    """ dummy function to clean up before """
    pass


if __name__ == '__main__':
    # Class basics
    create_team()
    create_crowd()
    show_str_vs_repr()

    # Instance and class data
    show_instance_data()
    show_class_data()
    show_slots()

    # Instance creation
    show_new_and_init()
    define_a_singleton()
    last_function()
