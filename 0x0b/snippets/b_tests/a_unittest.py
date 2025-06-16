# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
In this snippet, we will have a look at some simple unit tests that
we can use for our tasks.

Teaching focus
  - unit tests
  - test cases
  - test suites
  - test runners
"""


import unittest
from dataclasses import dataclass


@dataclass
class Number:
    """ A test class with a number. """
    n: int


class Odd(Number):
    def is_odd(self):
        return True


class Even(Number):
    pass


def from_int(n: int):
    """ Number-factory """
    if n < 0:
        raise RuntimeError("n negativ")
    return None if n == 0 else Even(n) if n % 2 == 0 else Odd(n)    # pls forgive me the None-case...


class TestNumber(unittest.TestCase):                    # Testcase, extends
    @classmethod
    def setUpClass(cls):                                # set up and tear down
        print(f" 1| setUp Class")

    @classmethod
    def tearDownClass(cls):
        print(f" 2| tearDown Class")

    def setUp(self):
        print(f" 3| setUp TestCase '{self._testMethodName}'")

    def tearDown(self):
        print(f" 4| tearDown TestCase '{self._testMethodName}'")

    def test_factory(self):                             # a single test with one purpose
        num0 = from_int(0)
        self.assertIsNone(num0, msg="oops - none")      # asserts, also assertIsNotNone

        num1 = from_int(9)
        self.assertIsInstance(num1, Odd)                # also assertIsNotInstance

        num2 = from_int(12)
        self.assertIsInstance(num2, Even)
        with self.assertRaises(RuntimeError):           # expect an exception
            from_int(-1)

    def test_odd(self):                                 # check values
        odd1 = Odd(1)
        odd3 = Odd(3)
        self.assertEqual(odd1.n, 1)
        self.assertIsNot(odd1, odd3)                    # also assertIs
        self.assertTrue(odd1.is_odd())                  # also assertFalse

        self.assertListEqual([1, 3], [odd1.n, odd3.n])  # also assertTupleEqual, assertDictEqual

# def test_all():                                       # all tests found in the module are run
#    unittest.main(verbosity=2)


def test_all_with_suite():
    suite = unittest.TestSuite()
    suite.addTest(TestNumber('test_factory'))           # configure TestSuite
    suite.addTest(TestNumber('test_odd'))
    runner = unittest.TextTestRunner()
    runner.run(suite)


if __name__ == '__main__':                              # running in PyCharm
    # test_all()
    test_all_with_suite()

"""
Testcase
  - The unit tests are structured in such a way that all test functions
    ('test_xxx') are defined within a 'Testcase' class. That way, all 
    asserts are available as members.

set up and tear down
  - To prepare the context, there are functions that run at the beginning 
    and end of the entire test run ('setUpClass', 'tearDownClass'). And 
    those that run before and after each individual test ('setUp','tearDown').

From Python doc:
  - test fixture
    A test fixture represents the preparation needed to perform one or 
    more tests, and any associated cleanup actions. This may involve, 
    for example, creating temporary or proxy databases, directories, 
    or starting a server process.
  - test case
    A test case is the individual unit of testing. It checks for a 
    specific response to a particular set of inputs. unittest provides 
    a base class, TestCase, which may be used to create new test cases.
  - test suite
    A test suite is a collection of test cases, test suites, or both. 
    It is used to aggregate tests that should be executed together.
  - test runner
    A test runner is a component which orchestrates the execution of 
    tests and provides the outcome to the user. The runner may use 
    a graphical interface, a textual interface, or return a special value 
    to indicate the results of executing the tests.
In 'PyCharm' you get a nice list of recent test results.

asserts
  - There are various asserts, these are the most important ones. For 
    special cases or more complex conditions, assertTrue works in any case.
    See https://docs.python.org/3/library/unittest.html

configure TestSuite
  - There are many other ways of compiling a test suite, as described in 
    the documentation.
    See https://docs.python.org/3/library/unittest.html#loading-and-running-tests
    
running in PyCharm
  - Note that running this script in PyCharm says 'Run Python tests in...' 
    and runs all the tests. To run 'test_all_with_suite' select 'Run...' from 
    the menu.
"""
