# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet is about context managers.

Teaching focus
  - with
"""

import unittest
from contextlib import contextmanager, closing

"""
'with' use cases
  - Open and close          e.g. file io
  - Lock and release            ?
  - Change and reset            ?
  - Create and delete           ?
  - Enter and exit              ?
  - Start and stop              ?
  - Setup and teardown          ?

with expression as target_var:
    do_something(target_var)
"""


def context_manager_examples():
    """ context manager examples """
    print("\ncontext_manager_examples\n========================")

    # example 1 - see a_file_io.py
    # with open(filename, 'w') as writer:
    #     ...

    # example 2
    class ExampleTestCase(unittest.TestCase):
        def test_int_ops(self):
            with self.assertRaises(Exception):
                1 + '1'  # op not defined -> an exception is expected

    suite = unittest.defaultTestLoader.loadTestsFromTestCase(ExampleTestCase)
    unittest.TextTestRunner().run(suite)

    # more examples as tasks


def new_context_managers():
    """ new context managers """
    print("\nnew_context_managers\n====================")

    class SimpleIncrementContextManager:                            # (A) ContextManager
        def __init__(self, n: int):
            self.n = n + 1
            print(f" a|     init {n=}, {self.n=}")

        def __enter__(self):                                        # context manager protocol
            self.n = self.n + 1
            print(f" b|     enter {self.n=}")
            return self.n

        def __exit__(self, *args_not_used_see_below):               # context manager protocol
            self.n = self.n + 1
            print(f" c|     exit {self.n=}")

    print(f" 1| use SimpleIncrementContextManager")
    with SimpleIncrementContextManager(23) as k:                    # 'k' is the result of enter
        print(f" d|   {k=}")
    print(f" 2| after SimpleIncrementContextManager")

    class PrintContextManager:
        def __init__(self, indent):
            self.spaces = ' '*indent

        def __enter__(self):
            print(f"{self.spaces}Enter...")
            return self

        def __exit__(self, *args_not_used_see_below):
            print(f"{self.spaces}Leave...")

        def print(self, *args, **kwargs):
            print(f"{self.spaces}", end='')
            print(*args, **kwargs)

    print(f" 3| use PrintContextManager")
    with PrintContextManager(4) as pcm:                             # 'pcm' is the result of enter
        pcm.print(f"more output... type pcm: {type(pcm)}")
    print(f" 4| after PrintContextManager")

    class Guard:
        def __init__(self, items):
            self.items = items

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_value, exc_tb):            # _tb traceback
            if isinstance(exc_value, IndexError):
                print(f">>>>>>>>>> IndexError... Really? Again?")
                print(f"           block: {exc_type}")
                print(f"<<<<<<<<<< message: {exc_value}")
                return True                                         # 'swallow' exceptions
            return False                                            # technically not necessary

        def __getitem__(self, key):
            return self.items[key]

    primes = [2, 3, 5, 7, 11]
    print(f" 5| use Guard")
    with Guard(primes) as guarded:
        print(f" 6|   items[3]={guarded[3]}")
        print(f" 7|   items[7]={guarded[7]}")
    print(f" 8| after Guard\n")


def annotated_context_managers():
    """ annotated context managers """
    print("\nannotated_context_managers\n==========================")

    @contextmanager                                                 # (B) @contextmanager
    def indent_context_manager(indent_level):
        spaces = ' ' * indent_level
        print(f"{spaces}Enter...")
        yield spaces
        print(f"{spaces}Leave...")

    print(f" 1| use indent_context_manager")
    with indent_context_manager(4) as indent:                       # 'indent' stems from yield
        print(f"{indent}more output... type indent: {type(indent)}")
    print(f" 2| after indent_context_manager")


def close_a_context_manager():
    """ close a context manager """
    print("\nclose_a_context_manager\n=======================")

    class Resource:
        def close(self):
            print(" a|   clean me")

    print(f" 1| use Resource")
    # with Resource():                                              # does not support protocol
    with closing(Resource()) as res:                                # (C) closing
        print(f"    type res: {type(res)}")
    print(f" 2| after using Resource")


if __name__ == "__main__":
    context_manager_examples()
    new_context_managers()
    annotated_context_managers()
    close_a_context_manager()


"""
'with' use cases
  - Open and close          e.g. file io
  - Lock and release            mutex
  - Change and reset            data
  - Create and delete           temp. ressource
  - Enter and exit              functions
  - Start and stop              timer
  - Setup and teardown          tests

ContextManager
From https://realpython.com/python-with-statement/
  - The context manager object results from evaluating the expression after 
    with. In other words, expression must return an object that implements 
    the context management protocol. This protocol consists of two special methods:
      - .__enter__() is called by the with statement to enter the runtime context.
      - .__exit__() is called when the execution leaves the with code block.
  - The 'as' specifier is optional. If you provide a target_var with as, then 
    the return value of calling .__enter__() on the context manager object is 
    bound to that variable.

See
    https://docs.python.org/3/reference/compound_stmts.html#the-with-statement
    https://peps.python.org/pep-0343/
    https://realpython.com/python-with-statement/

@contextmanager
  - A short form. Runs the code up to the 'yield' ('init' and 'enter') and the 
    code after that instead of 'exit'.

closing
  - Historically, there have been resources that do not support the ContextManager 
    protocol, but have a 'close' function to release the resources. With 'closing' 
    you build a ContextManager around it, see
    https://docs.python.org/3/library/contextlib.html#contextlib.closing
"""
