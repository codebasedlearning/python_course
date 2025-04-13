# (C) 2025 Alexander Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet discusses classes, initializers, methods and __dict__.

Teaching focus
  - create instances
  - learn the concept dynamic data
"""


class TeamMember:
    """ simple team member class """                            # class doc string

    def __init__(self, name: str, born_in: int):                # initializer (ctor), self = this
        self.name = name                                        # instance attributes
        self.born_in = born_in
        print(f" a|   TeamMember.init: {self.name=}, {self.born_in=}")

    def greetings(self):                                        # methods, self
        print(f" b|   TeamMember.greetings: Hello, I am {self.name}, born in {self.born_in}.")
        return self


def create_team():
    """ first class instances """
    print("\ncreate_team\n===========")

    alice = TeamMember("Alice", 2005)                           # What is most readable?
    alice.greetings()
    print(f" 1| {alice=}")                                      # hmmm...

    bob = TeamMember(name="Bob", born_in=2007)                  # or this?
    bob.greetings()
    print(f" 2| Bob={bob=}")

    TeamMember("Charly", born_in=1999).greetings()              # chaining


class Person:
    """ simple person class """                                 # class doc string

    being_old = 99

    def __init__(self, surname: str, age: int):                 # initializer (ctor), self = this
        self.surname = surname                                  # instance attributes
        self.age = age
        print(f" a|   Person.init: {self}, {self=}")

    def one_year_older(self):
        self.age += 1
        if self.age > Person.being_old:
            print(f" b|   Respect, {self.surname}!")
        return self

    def celebrate(self): # -> Self:
        print(f" c|   Person.celebrate: Happy {self.age}th birthday, {self.surname}!")
        return self

    def __str__(self):
        return f"('{self.surname}', {self.age})"

    def __repr__(self):
        return f"{self.__dict__}"


def create_crowd():
    """ more class instances """
    print("\ncreate_crowd\n============")

    peter = Person("Peter", 23)
    peter.one_year_older().celebrate()
    print(f" 1| Peter={peter}")

    paul = Person(surname="Paul", age=24)
    paul.one_year_older().celebrate()
    print(f" 2| Paul={paul}")


def show_instance_data():
    print("\nshow_instance_data\n==================")

    doro = TeamMember("Doro", born_in=2000)
    mary = Person("Mary", age=25)

    print(f" 1| {doro.__dict__=}")                              # this is an important observation
    print(f" 2| {mary.__dict__=}")

    doro.has_a_sister = True
    mary.has_a_brother = True

    print(f" 3| {doro.__dict__=}")
    print(f" 4| {mary.__dict__=}")

    del doro.born_in
    del doro.has_a_sister
    print(f" 5| {doro.__dict__=}")


def show_class_data():
    print("\nshow_class_data\n===============")

    mary = Person("Mary", age=25)
    print(f" 1| {Person.__dict__=}")
    mary.one_year_older()                                       # nothing happens

    Person.being_old = 18
    print(f" 2| {Person.__dict__=}")
    mary.one_year_older()                                       # class-data has changed


if __name__ == '__main__':
    create_team()
    create_crowd()
    show_instance_data()
    show_class_data()


###############################################################################


"""
Summary

Topics
  - create instances
  - self
  - __dict__
  - class doc string
  - initializer (ctor)
  - methods
  - dynamic data
  - class data

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

See also
  - 
"""
