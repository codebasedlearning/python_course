# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet discusses (single) inheritance in Python.

Teaching focus
  - inheritance
"""


class Person:                                                   # inherits implicitly from 'object'
    """ Simple person class """

    def __init__(self, name):
        super().__init__()                                      # necessary? btw. not: super.__init__()
        self.name = name
        print(f" a|   Person.init name='{self.name}', id={id(self)}")

    def introduce_myself(self):
        print(f" b|   --- Hello, I am {self.name} ---")

    def __del__(self):
        print(f" c|   Person.del name='{self.name}'")


class Employee(Person):                                         # with base class(es)
    def __init__(self, name, salary):
        super().__init__(name)                                  # super; Person.__init__(self, name)
        self.salary = salary
        print(f" d|   Employee.init name='{self.name}', id={id(self)}")

    def introduce_myself(self):
        super().introduce_myself()                              # same principle as before
        # Person.introduce_myself(self)                         # works, discuss this with multiple inheritance
        print(f" e|   --- and my salary is {self.salary} ---")

    def __del__(self):
        print(f" f|   Employee.del name='{self.name}'")
        super().__del__()


def create_team():
    """ create team with different persons """
    print("\ncreate_team\n===========")

    print(f" 1| create Peter")
    peter = Person(name="Peter")
    peter.introduce_myself()

    print(f" 2| and Mary")
    mary = Employee(name="Mary", salary=1000)
    mary.introduce_myself()

    print(f" 3| end")


def introduce_MRO():
    """ introduce MRO """
    print("\nintroduce_MRO\n=============")

    print(f" 1| MRO==method resolution order\n"
          f"    {Person.__mro__}\n"
          f"    {Employee.__mro__}")


if __name__ == '__main__':
    create_team()
    introduce_MRO()


###############################################################################


"""
Summary

Topics
  - inheritance
  - super
  - MRO

Inheritance
  - Inherits implicitly from 'object'.
  - It is
        class Person(object) 
    for Python 2.x
  - Technically, it is not necessary to call the initializer of object. 
    The question is whether, to avoid errors, the rule of calling the 
    the base class should generally be followed.
  - A nice discussion can be found here
    https://stackoverflow.com/questions/52272811/when-inheriting-directly-from-object-should-i-call-super-init
    This question becomes more interesting in the case of multiple inheritance.

super
  - As a rule of thumb, I would always call the constructor of the base class. 
    This is because a subclass usually uses base functionality, and an employee 
    instance is a person. Then you should give the base class a chance to 
    initialise its own data or clean up in the destructor.
  - super() returns a delegate object to its parent class, so you call the 
    method of your choice directly on it.
  - Note also, that in case of 'Mary' the object 'self' in Person.init _is_ 
    of type Employee.
  - super() starts searching for a matching method (here call_base) at 
    one level above in the instance hierarchy. If you specify the first 
    argument in super, searching starts from there.
  - Be careful in calling virtual methods from 'init'. You will end up 
    working with instances that may not be initialised. This can happen 
    if the initialisation of the object or the calling of virtual functions 
    is not well thought out.

MRO, method resolution order
  - From 
    https://realpython.com/python-super/
    The method resolution order (or MRO) tells Python how to search for 
    inherited methods. This comes in handy when you’re using super() because 
    the MRO tells you exactly where Python will look for a method you’re 
    calling with super() and in what order.

See also
  - 
"""
