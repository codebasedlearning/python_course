# (C) 2025 Alexander Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet discusses a simple class with attributes.

Teaching focus
  - working with __dict__, class and instance attributes
  - access modifiers
  - see Python possibilities, like patching attributes or methods
    at runtime (uuuh) or 'modify' the access via __getattribute__
  - a lot of pylint and mypy errors for didactic reasons
"""


class Person:
    """ simple person class """

    next_id = 1                             # class attribute

    def __init__(self, name):
        self.name = name                    # instance attribute

        self._id = Person.next_id           # protected, with prefix '_' (convention)
        self.__secret_number = self._id*23  # private, two '__', not only a convention (renamed to '_Person__secret_no')

        Person.next_id += 1                 # access class attribute
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
        print(f" b|   {Person.next_id=}")


def class_vs_instance_attribute():
    """ see order in action """
    print("\nclass_vs_instance_attribute\n===========================")

    peter = Person(name="Peter")
    mary = Person(name="Mary")
    print(f" 1| current state:\n"
          f"      {peter} -> {peter.next_id=}\n"
          f"      {mary} -> {mary.next_id=}\n"
          f"      {Person.__dict__=} -> {Person.next_id=}")

    peter.next_id = 123
    print(f" 2| peter.next_id changed:\n"
          f"      {peter} -> {peter.next_id=}\n"
          f"      {mary} -> {mary.next_id=}\n"
          f"      {Person.__dict__=} -> {Person.next_id=}")

    Person.next_id = 456
    print(f" 3| Person.next_id changed:\n"
          f"      {peter} -> {peter.next_id=}\n"
          f"      {mary} -> {mary.next_id=}\n"
          f"      {Person.__dict__=} -> {Person.next_id=}")

    Person.next_id = 2


def show_access_modifiers():
    """ access different attributes """
    print("\nshow_access_modifiers\n=====================")

    peter = Person(name="Peter")
    print(f" 1| public:    {peter}")
    print(f" 2| protected: {peter._id=}")
    print(f" 3| private:   {peter._Person__secret_number=}, {peter._Person__my_internal_secret()=}")

    Person.print_next_id()


# Now the fun (or illegal) stuff... primarily shown for educational purposes!


def patch_attributes():
    """ replace or patch attributes at runtime """
    print("\npatch_attributes\n================")

    peter = Person(name="Peter")
    paul = Person(name="Paul")
    mary = Person(name="Mary")
    print(f" 1| create: {peter},\n"
          f"            {paul},\n"
          f"            {mary}")

    peter.fan_of = "LFC"                    # dynamically add attributes,
    paul.mothers_name = "Eve"               # this is a proof of concept, not best practise!
    mary.fan_of = "ManU"
    print(f" 2| modify: {peter},\n"
          f"            {paul},\n"
          f"            {mary}")

    fan_set = [f"{peter.name}:{peter.fan_of}",
               f"{mary.name}:{mary.fan_of}"]            # accessible...
    try:
        fan_set.append(f"{paul.name}:{paul.fan_of}")    # if exists...
    except AttributeError:
        fan_set.append(f"{paul.name}:?")
    print(f" 3| fans: {fan_set}")

    del peter.fan_of                        # delete attribute...
    del mary.fan_of
    # del paul.mothers_name
    paul.__dict__.pop("mothers_name")       # or pop it from __dict__
    print(f" 4| clear:  {peter},\n"
          f"            {paul},\n"
          f"            {mary}")


    print(f" 5| secret orig:    {peter.secret()=}, {paul.secret()=}, {mary.secret()=}")

    def secret(self):
        return self._id*-1

    Person.secret = secret                  # patch method
    print(f" 6| secret patched: {peter.secret()=}, {paul.secret()=}, {mary.secret()=}")


class AdultPerson:
    """ is allowed to see any film in the cinema """

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __getattribute__(self, attr_name):  # rarely overwritten...
        if attr_name != "age" or super().__getattribute__('age') >= 18:
            return super().__getattribute__(attr_name)
        return 18


def access_every_cinema():
    """ replace or patch attributes at runtime """
    print("\naccess_every_cinema\n===================")

    harry = AdultPerson(name="Dirty Harry", age=16)

    print(f" 1| {harry.__dict__}, "
          f"name: '{harry.name}', age: {harry.age}... or, real-age: {harry.__dict__['age']}\n")


if __name__ == '__main__':
    class_vs_instance_attribute()
    show_access_modifiers()
    patch_attributes()
    access_every_cinema()


###############################################################################


"""
Summary

Topics
  - "public", "protected" und "private"
  - class and instance attributes
  - methods, @classmethod 
  - __dict__
  - __getattribute__

Public, protected und private.
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
    https://stackoverflow.com/questions/33533148/how-do-i-type-hint-a-method-with-the-type-of-the-enclosing-class

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
"""
