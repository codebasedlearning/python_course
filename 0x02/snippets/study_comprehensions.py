# (C) A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet is a dedicated deep dive into comprehensions.

Teaching focus
  - list comprehensions (basic, with filter, with transformation)
  - dict comprehensions
  - set comprehensions
  - nested comprehensions
  - when NOT to use comprehensions (readability)

Comprehensions are one of Python's most powerful features. They replace
common loop-and-append patterns with a concise, declarative syntax.

General form:
  [expression for item in iterable if condition]

See also
  https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions
  https://peps.python.org/pep-0202/
"""

from utils import print_function_header

"""
Topic: List comprehensions
"""


@print_function_header
def basic_list_comprehensions():
    """ list comprehensions: the bread and butter """

    # classic loop-and-append pattern
    squares_loop = []
    for i in range(1, 6):
        squares_loop.append(i * i)
    print(f" 1| loop:          {squares_loop}")

    # same thing as a comprehension
    squares_comp = [i * i for i in range(1, 6)]
    print(f" 2| comprehension: {squares_comp}")

    # with a filter condition
    even_squares = [i * i for i in range(1, 11) if i % 2 == 0]
    print(f" 3| even squares:  {even_squares}")

    # with a transformation and filter combined
    words = ["Hello", "world", "Python", "is", "great"]
    long_upper = [w.upper() for w in words if len(w) > 3]
    print(f" 4| long & upper:  {long_upper}")

    # conditional expression (ternary) inside comprehension
    labels = ["even" if x % 2 == 0 else "odd" for x in range(1, 6)]
    print(f" 5| labels:        {labels}")
    #        ^-- note: this is NOT a filter, it's an expression


"""
Topic: Dict and set comprehensions
"""


@print_function_header
def dict_and_set_comprehensions():
    """ dict and set comprehensions """

    # dict comprehension: {key_expr: val_expr for item in iterable}
    names = ["Alice", "Bob", "Charlie"]
    name_lengths = {name: len(name) for name in names}
    print(f" 1| name lengths: {name_lengths}")

    # inverting a dict
    original = {"a": 1, "b": 2, "c": 3}
    inverted = {v: k for k, v in original.items()}
    print(f" 2| inverted:     {inverted}")

    # dict comprehension with filter
    scores = {"Alice": 85, "Bob": 42, "Charlie": 91, "Dave": 67}
    passed = {name: score for name, score in scores.items() if score >= 60}
    print(f" 3| passed:       {passed}")

    # set comprehension: {expr for item in iterable}
    words = ["hello", "HELLO", "Hello", "world", "WORLD"]
    unique_lower = {w.lower() for w in words}
    print(f" 4| unique lower: {unique_lower}")

    # set comprehension for deduplication with transformation
    data = [1, -1, 2, -2, 3, -3, 3]
    abs_values = {abs(x) for x in data}
    print(f" 5| abs values:   {abs_values}")


"""
Topic: Nested comprehensions
"""


@print_function_header
def nested_comprehensions():
    """ nested comprehensions: read them like nested loops """

    # flatten a 2D list
    matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    flat = [x for row in matrix for x in row]       # outer loop first, inner loop second
    print(f" 1| flat:      {flat}")

    # equivalent loop for clarity:
    # for row in matrix:
    #     for x in row:
    #         flat.append(x)

    # 2D construction: list of lists
    grid = [[col * row for col in range(1, 4)] for row in range(1, 4)]
    print(f" 2| grid:      {grid}")

    # Cartesian product with filter
    pairs = [(x, y) for x in range(4) for y in range(4) if x != y]
    print(f" 3| pairs x!=y: {pairs}")

    # transpose a matrix
    transposed = [[row[i] for row in matrix] for i in range(3)]
    print(f" 4| transposed: {transposed}")


"""
Topic: When NOT to use comprehensions
"""


@print_function_header
def comprehension_limits():
    """ readability matters: when a loop is the better choice """

    # too complex, hard to read at a glance
    # result = [x * y for x in range(5) for y in range(5) if x != y and (x + y) % 2 == 0 and x > 0]

    result = []
    for x in range(5):
        for y in range(5):
            if x != y and (x + y) % 2 == 0 and x > 0:
                result.append(x * y)
    print(f" 1| complex (loop): {result}")

    evens = [x for x in range(20) if x % 2 == 0]
    print(f" 2| simple:         {evens}")

    # rule of thumb: if you can't read it in ~3 seconds, use a loop
    print(" 3| rule: if it takes more than 3 seconds to parse, use a loop")

    # generator expression vs list comprehension
    total = sum(x * x for x in range(1000))         # no brackets -> generator expression
    print(f" 4| sum of squares (generator): {total}")
    #        ^-- memory-efficient: does not create an intermediate list


"""
Topic: Python is dense; zip + comprehensions
"""

def build_fruit_history(fruits_block, prices_block):
    """ Converts data blocks into a dict of fruits and their individual prices over time. """

    # classical style
    #   fruits = []
    #   for fruit in fruits_block.split(","):
    #       fruits.append(fruit.strip())
    #
    # Preview: with list comprehension:
    fruits = [fruit.strip() for fruit in fruits_block.split(",")]
    print(f" a| {fruits=}")

    prices_week = [                         # Nested list comprehension.
        [float(s) for s in row.strip(" []").split(",")]         # strip(chars) removes chars from string.
        for row in prices_block.strip().split("\n")             # float(s) converts string to float.
    ]
    print(f" b| {prices_week=}")

    # classical style
    #   num_rows = len(prices_week)
    #   num_cols = len(prices_week[0])                          # Assuming all rows have the same number of columns.
    #   prices_fruit = [[0]*num_rows for _ in range(num_cols)]  # A list of lists with num_rows zeros; '_' is a name.
    #   for row_index in range(num_rows):                       # A^T
    #       for col_index in range(num_cols):
    #           prices_fruit[col_index][row_index] = prices_week[row_index][col_index]
    #
    # but with list comprehension, '*' (expansion) and zip (zip l1,l2 into (l1_i,l2_i)_i) )
    prices_fruit = list(zip(*prices_week, strict=True))         # Same as: [list(row) for row in zip(*prices_week)]
    print(f" c| {prices_fruit=}")

    fruit_history = dict(zip(fruits, prices_fruit, strict=True)) # Same as: {k:v for k,v in zip(fruits, prices_fruit)}
    print(f" d| {fruit_history=}")

    return fruit_history

@print_function_header
def calc_average_prices():
    """ Calculates average prices. """

    # Fruits (head) with prices per (line per) week.
    FRUIT_DATA = """
    Apple, Banana, Cherry, Mango, Pineapple

    [0.123, 0.678, 0.345, 0.980, 0.456]
    [0.231, 0.564, 0.897, 0.123, 0.675]
    [0.423, 0.942, 0.812, 0.503, 0.256]
    [0.134, 0.789, 0.456, 0.234, 0.897]
    """

    fruits_block, prices_block = FRUIT_DATA.split("\n\n")
    fruit_history = build_fruit_history(fruits_block, prices_block)
    average_prices = [(fruit, sum(values) / len(values)) for fruit, values in fruit_history.items()]
    print(f" 1| {average_prices=}")

if __name__ == "__main__":
    basic_list_comprehensions()
    dict_and_set_comprehensions()
    nested_comprehensions()
    comprehension_limits()
    calc_average_prices()
