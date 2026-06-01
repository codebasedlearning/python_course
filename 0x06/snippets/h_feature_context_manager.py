# (C) A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet is about context managers.

Teaching focus
  - with

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

import time
import unittest
from contextlib import closing, contextmanager

from utils import print_function_header

"""
'with' use cases see above

with expression as target_var:
    do_something(target_var)
"""

@print_function_header
def new_context_managers():
    """ new context managers """

    def do_something_important():
        print(" x| - do something important...", end='')
        time.sleep(0.1)
        print("done")
    
    class TimerV1:
        # perf_counter is a high-resolution timer that returns a float of seconds;
        # it uses the most precise clock available on the platform
        def __enter__(self):
            self.start = time.perf_counter()
            print(" a| - start")
    
        def __exit__(self, *args):          # args needed but unused, see below
            elapsed = time.perf_counter() - self.start
            print(f" b| - stop, {elapsed=:0.4f}s")

    print(" 1| timer class version 1")
    with TimerV1():
        do_something_important()
    print()

    # __enter__ returns self, __exit__ writes to self, => standard pattern

    class TimerV2:
        def __enter__(self):
            self.start = time.perf_counter()
            self.elapsed = 0.0
            return self                     # becomes the 'as' variable

        def __exit__(self, *args):
            self.elapsed = time.perf_counter() - self.start

    print( " 2| timer class version 2, start")
    with TimerV2() as t2:
        do_something_important()
    print(f"  | stop, {t2.elapsed=:0.4f}s")
    print()

    # what about this version, does it work?

    class TimerV3:
        def __enter__(self):
            self.start = time.perf_counter()
            return lambda: time.perf_counter() - self.start

        def __exit__(self, *args):
            pass

    print( " 3| timer class version 3, start")
    with TimerV3() as t3:
        do_something_important()
    print(f"  | stop, elapsed={t3():0.4f}s")
    print()

    class PrintContextManager:
        def __init__(self, indent):
            self.spaces = ' '*indent

        def __enter__(self):
            print(f"{self.spaces}Enter...")
            return self

        def __exit__(self, *args):
            print(f"{self.spaces}Leave...")

        def print(self, *args, **kwargs):
            print(f"{self.spaces}", end='')
            print(*args, **kwargs)

    print(" 4| use PrintContextManager")
    with PrintContextManager(4) as pcm:     # 'pcm' is the result of enter
        pcm.print(f"more output... {type(pcm)=}")
    print(" 5| after PrintContextManager")

    class Guard:
        def __init__(self, items):
            self.items = items

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_value, exc_tb):        # _tb traceback
            if isinstance(exc_value, IndexError):
                print(f">>>>>>>>>> IndexError... Really? Again?")
                print(f"           block: {exc_type}")
                print(f"<<<<<<<<<< message: {exc_value}")
                return True                 # 'swallow' exceptions
            return False                    # technically not necessary

        def __getitem__(self, key):
            return self.items[key]

    primes = [2, 3, 5, 7, 11]
    print(" 6| use Guard")
    with Guard(primes) as guarded:
        print(f" 7|   items[3]={guarded[3]}")
        print(f" 8|   items[7]={guarded[7]}")
    print(" 9| after Guard\n")


@print_function_header
def annotated_context_managers():
    """ annotated context managers """

    @contextmanager                         # @contextmanager
    def indent_context_manager(indent_level):
        spaces = ' ' * indent_level
        print(f"{spaces}Enter...")
        yield spaces
        print(f"{spaces}Leave...")

    print(" 1| use indent_context_manager")
    with indent_context_manager(4) as indent:                       # 'indent' stems from yield
        print(f"{indent}more output... {type(indent)=}")
    print(" 2| after indent_context_manager")


@print_function_header
def close_a_context_manager():
    """ close a context manager """

    class Resource:
        def close(self):
            print(" a|   clean me")

    print(" 1| use Resource")
    # with Resource():                      # Resource does not support protocol
    with closing(Resource()) as res:        # closing
        print(f"    type res: {type(res)}")
    print(" 2| after using Resource")

    # more examples as tasks

if __name__ == "__main__":
    new_context_managers()
    annotated_context_managers()
    close_a_context_manager()
