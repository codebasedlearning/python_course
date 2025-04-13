# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet discusses classes, initializers and constructors.

Teaching focus
  - interna of instance creation
  - __new__, __init__, __del__
"""


class Person:
    """ simple person class """
    def __new__(cls, *args, **kwargs):      # here not necessary, just to see the args
        print(f" a|   Person.new: {cls}, {args=}, {kwargs=}")
        # return object.__new__(cls)
        return super().__new__(cls)

    def __init__(self, name: str):
        self.name = name
        print(f" b|   Person.init: {self.name=}")

    def __del__(self):
        print(f" c|   Person.del: {self.name=}")
        # super().__del__()     # object has no __del__


def show_new_and_init():
    """ see new and del in action """
    print("\nshow_new_and_init\n=================")

    print(f" 1| start")
    peter = Person(name="Peter")
    print(f" 2| {peter.name=}")

    if peter.name:
        paul = Person("Paul")
        print(f" 3| {paul.name=}")

    def inner_func():
        mary = Person(name="Mary")
        print(f" 4| {mary.name=}")

    inner_func()
    print(f" 5| end")

# problems?

class DatabaseConnector:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)  # Call only the first time
        return cls._instance

    def __init__(self, connection_string):
        self.connection_string = connection_string

class ServiceDetector:
    _instance = None
    _initialized = False  # Track initialization

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)  # Create the instance only once
        return cls._instance

    def __init__(self, url):
        if not self._initialized:
            self.url = url  # Initialize only once
            self._initialized = True  # Set the flag

def define_a_singleton():
    """ define a singleton """
    print("\ndefine_a_singleton\n==================")

    db_connector = DatabaseConnector(connection_string="aws.com")
    database_access = DatabaseConnector(connection_string="azure.com")
    print(f" 1|    {id(db_connector)=}, connected to: '{db_connector.connection_string}'")
    print(f"    {id(database_access)=}, connected to: '{database_access.connection_string}'")


    main_service = ServiceDetector(url="//server")
    docker_service = ServiceDetector(url="//docker")
    print(f" 2|   {id(main_service)=}, ask here: '{main_service.url=}'")
    print(f"    {id(docker_service)=}, ask here: '{docker_service.url=}'")

def last_function():
    """ dummy function to clean up before """
    print("\nlast_function\n=============")

if __name__ == '__main__':
    show_new_and_init()
    define_a_singleton()
    last_function()


###############################################################################


"""
Summary

Topics
  - instance creation
  - __new__, __init__, __del__

__new__, __init__
  - In fact, the process of creating and initialising an instance consists 
    of several steps. 
    From Python doc https://docs.python.org/2/reference/datamodel.html#basic-customization
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
    as necessarily involving allocation; all hat we require is that '__new__' 
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
    and in almost all situations the standard  'objects.__new__' will be 
    sufficient.

dtor, Destructors
  - Python also has destructors. 
  - From Python doc https://docs.python.org/2/reference/datamodel.html#basic-customization
      - '__del__(self)' is called when the instance is about to be destroyed. 
        This is also called a 'destructor'.
    It is only called when its reference count reaches zero. Some common 
    situations may prevent the reference count of an object from going to 
    zero, e.g. circular references between objects.
  - According to https://docs.python.org/2/reference/datamodel.html
    the only required property of Python's garbage collection is that it 
    happens after all references have been deleted, so it need not happen 
    immediately afterwards, and may not happen at all.

See also
  - 
"""
