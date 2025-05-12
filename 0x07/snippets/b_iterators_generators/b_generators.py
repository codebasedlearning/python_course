# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet introduces yield, generators and generator functions.

Teaching focus
  - yield
  - generators
  - generator functions
"""

import itertools
from inspect import isgeneratorfunction, isgenerator


def motivate_generators():
    """ motivate generators """
    print("\nmotivate_generators\n===================")

    def read_data(base, lower_limit, upper_limit):
        print(" a| - (in read) ")
        numbers = []
        for i in range(lower_limit, upper_limit+1):
            numbers.append(i * base)
        return numbers
        # return [i * base for i in range(lower_limit, upper_limit + 1)]  # consider this as large input data

    print(" 1| start reading ")
    items_all = read_data(7, 1, 20)         # what is the 'problem' here?
    print(f" 2| items_all=...: ", end='')
    for n in items_all:
        print(f"{n} ", end='')
    print()

    def generate_data(base, lower_limit, upper_limit):  # generator function and generator iterator
        print("(in generator) ", end='')
        for i in range(lower_limit, upper_limit+1):     # the 'algorithm'
            yield i * base                              # instead of .append

    items_gen = generate_data(7, 1, 20)     # generator iterator = "generator" (is a iterator)
    print(f" 3| items_gen=...: ", end='')
    for n in items_gen:
        print(f"{n} ", end='')
    print()

    def generate_123():                     # continue after yield until the end
        print("(start) ", end='')
        yield 1
        print("(i) ", end='')
        yield 2
        print("(ii) ", end='')
        yield 3
        print("(end) ", end='')

    item123 = generate_123()
    print(f" 4| item123=...: ", end='')
    for n in item123:
        print(f"{n} ", end='')
    print()

    data123 = generate_123()                # basically iter(generate_123())
    print(f" 5| data123=...: ", end='')
    try:
        while True:
            n = next(data123)               # also starts and gets the next value from the generator
            print(f"{n} ", end='')
    except StopIteration:
        print("stop")                       # data123 is exhausted, no more values

    print(f" 6| {isgeneratorfunction(generate_123)=} {isgenerator(item123)=}")


def generator_function_examples():
    """ motivate generators """
    print("\ngenerator_function_examples\n===========================")

    def gen_fib_seq(stop):                  # generator function with state
        fib_n0, fib_n1 = (1, 1)
        for _ in range(0, stop):
            yield fib_n0
            fib_n0, fib_n1 = (fib_n1, fib_n0 + fib_n1)

    fib10 = gen_fib_seq(10)
    print(f" 1| fib10={" ".join(map(str, fib10))}")

    def gen_countdown(n):                   # generator function with state
        while n > 0:
            yield n
            n -= 1

    cnt10 = gen_countdown(10)
    print(f" 2| cnt10={" ".join(map(str, cnt10))}")

    def gen_from_iterable(it):              # generator function from iterable
        for item in it:
            yield item

    prim7 = gen_from_iterable([2,3,5,7])
    print(f" 3| prim7={" ".join(map(str, prim7))}")

    print(f" 4| => list  {list(gen_fib_seq(10))}")
    print(f" 5| => list  {[*gen_fib_seq(10)]}")
    print(f" 6| => tuple {(*gen_fib_seq(10),)}")


def show_generator_expressions():
    """ show generator expressions """
    print("\nshow_generator_expressions\n==========================")

    squares = [i*i for i in range(1, 5)]    # list comprehension
    print(f" 1| {squares=}")

    gen_squares = (i*i for i in range(1, 5)) # generator expression
    print(f" 2| {list(gen_squares)=}")

    print(f" 3| {isgeneratorfunction(gen_squares)=} {isgenerator(gen_squares)=}")


"""
Concept                 How You Write It            What It Is                  What It Returns / Does

Generator Function      def + yield inside          function producing          Does not run yet, returns 
                                                    a generator iterator        generator iterator
Generator Iterator      Result of calling a         The actual iterator         Provides values when 
                        generator function          object                      next() is called
Generator Expression    (expr for item in iterable) inline, lazy generator      Returns a generator iterator 
                                                    producing values on demand  immediately
Generator (informal)    Often used to refer to      Usually means 
                        any of the above            generator iterator

"""


def using_pipelines():
    """ show pipelines """
    print("\nusing_pipelines\n===============")

    def to_square(numbers):
        return (number ** 2 for number in numbers)

    def filter_even(numbers):
        return (number for number in numbers if number % 2 == 0)

    def to_float(numbers):
        return (float(number) for number in numbers)

    lst = [1, 2, 3, 4, 5]
    even_squared = to_float(filter_even(to_square(lst)))    # this is the pipeline
    lst += [6]
    print(f" 1| even_squared={list(even_squared)}\n")       # lazy evaluated


def reuse_generators():
    """ discuss generator reuse """
    print("\nreuse_generators\n================")

    squares = (i * i for i in range(1, 5))                          # 1, 4, 9, 16; sum=30
    sum_squares_squared1 = sum(squares) * sum(squares)              # oops
    print(f" 1| {sum_squares_squared1=}")                           # reuse generator - any idea?

    # f_squares = lambda: (i * i for i in range(1, 5))              # lambda w.o. params, returns a generator expression
    def f_squares(): return (i * i for i in range(1, 5))            # see PEP8 for bound lambdas
    sum_squares_squared2 = sum(f_squares()) * sum(f_squares())      # note the call! works
    print(f" 2| {sum_squares_squared2=}")


def introducing_yield_from():
    """ introducing yield from """
    print("\nintroducing_yield_from\n======================")

    def f_gen1(): return (i*i*i for i in range(1, 3))   # 1, 8
    def f_gen2(): return (i*i for i in range(3, 6))     # 9, 16, 25

    gen_chained1 = itertools.chain(f_gen1(), f_gen2())  # how is this implemented?
    print(f" 1| chain1={list(gen_chained1)}")

    def gen_combined(g1, g2):                           # first variant
        for x in g1:
            yield x
        for x in g2:
            yield x

    gen_chained2 = gen_combined(f_gen1(), f_gen2())
    print(f" 2| chain2={list(gen_chained2)}")

    def gen_from(g1, g2):                               # yield from
        yield from g1
        yield from g2

    gen_chained3 = gen_from(f_gen1(), f_gen2())
    print(f" 3| chain3={list(gen_chained3)}")


def using_generator_send():                             # send... what?
    """ using generator send """
    print("\nusing_generator_send\n====================")

    def count_from(n):                                  # idea: count, but set 'start'
        while True:
            m = yield n
            if isinstance(m, int):
                n = m
            n += 1

    gen_n = count_from(20)

    lst = [next(gen_n) for _ in range(1, 11)]           # which numbers?
    print(f" 1| {lst=}")

    lst = [next(gen_n) for _ in range(1, 11)]           # which numbers?
    print(f" 2| {lst=}")

    x0 = gen_n.send(100)                                # x0 = ?
    x1 = next(gen_n)                                    # debug from 'send' with 'step into'
    x2 = next(gen_n)
    lst = [x0, x1, x2] + [next(gen_n) for _ in range(1, 11-3)]
    print(f" 3| {lst=}")

    def resettable_average():               # living generator, controllable
        total = 0
        count = 0
        average = None
        while True:
            try:
                number = yield average
                total += number
                count += 1
                average = total / count
            except ZeroDivisionError:
                print(" a| - reset average")
                total = 0
                count = 0
                average = None

    def start(generator):
        next(generator)
        return generator

    avg = start(resettable_average())

    print(f" 4| {avg.send(10)=}")
    print(f" 5| {avg.send(20)=}")

    avg.throw(ZeroDivisionError)            # reset the state

    print(f" 6| {avg.send(30)=}")
    print(f" 7| {avg.send(40)=}")


if __name__ == "__main__":
    motivate_generators()
    generator_function_examples()
    show_generator_expressions()
    using_pipelines()
    reuse_generators()
    introducing_yield_from()
    using_generator_send()

"""
process data one by one
  - In many cases it is not necessary, or even possible, to get all the data 
    first and then process it one by one. 
    What we need is a technique that allows us to have only the data that we 
    want to process, no more and no less. 
    So-called 'generators', in various forms (see below), deal with exactly 
    this problem. You can think of them as a kind of intelligent iterator.

generator function
  - From https://realpython.com/python-iterators-iterables
    In Python, you’ll commonly use the term 'generators' to collectively refer 
    to two separate concepts: the generator function and the generator iterator. 
      - The generator function is the function that you define using the yield statement. 
      - The generator iterator is what this function returns.
  - From https://docs.python.org/3/reference/simple_stmts.html:
    Using yield in a function definition is sufficient to cause that definition 
    to create a generator function instead of a normal function.

generator expression
  - From https://realpython.com/introduction-to-python-generators
    Like list comprehensions, generator expressions allow you to quickly 
    create a generator object in just a few lines of code. They’re also 
    useful in the same cases where list comprehensions are used, with an 
    added benefit: 
      - you can create them without building and holding the entire object 
        in memory before iteration. In other words, you’ll have no memory 
        penalty when you use generator expressions. 

lazy evaluated
  - This is important. Note that in the examples the generator takes the new 
    element into account. This is only possible if the evaluation is not done 
    at definition but at use.

reuse generator
  - Also important to know. Once the generator is done, it is 'exhausted', 
    i.e. done. So you cannot use it twice in the same expression.
  - Basically, we have three choices:
      - Store values... 
      - Create a class with some kind of reset.
      - Lambdas or functions to create a generator expression.

yield from
  - See https://docs.python.org/3/reference/simple_stmts.html
    and https://docs.python.org/3/reference/expressions.html#yieldexpr
    When yield from <expr> is used, the supplied expression must be an 
    iterable. The values produced by iterating that iterable are passed 
    directly to the caller of the current generator’s methods.

send
  - In PEP 342, support was added for passing values into generator
    https://github.com/qingkaikong/blog-1/blob/f453d320c06ac5b1a8d43380f9e6f9d9cf8c3022/content/2013-04-07-improve-your-python-yield-and-generators-explained.md

  - Remarks: There are more functions like 'send', namely 'close' and 'throw'. 
    See https://realpython.com/introduction-to-python-generators
"""
