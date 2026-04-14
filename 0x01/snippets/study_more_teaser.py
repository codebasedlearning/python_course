# (C) A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
Python basics meant as a starter - more teaser.
"""

from utils import print_function_header

"""
Topic: Debug
"""

@print_function_header
def debug_code():
    """ Debug code with errors. """

    data = [10, 20, 0, 30]

    try:
        results = [100 / x for x in data]   # Preview list comprehension, see below
        print(f" 1| {results=}")
    except ZeroDivisionError:
        print(" 2| exception caught!")      # Where is 'results'?


"""
Topic: List Comprehension
"""

@print_function_header
def process_prices():
    """ Work with prices. """

    # Fruits (head) with prices per (line per) week.
    FRUIT_DATA = """
    Apple, Banana, Cherry, Mango, Pineapple

    [0.123, 0.678, 0.345, 0.980, 0.456]
    [0.231, 0.564, 0.897, 0.123, 0.675]
    [0.423, 0.942, 0.812, 0.503, 0.256]
    [0.134, 0.789, 0.456, 0.234, 0.897]
    """

    fruits_block, prices_block = FRUIT_DATA.split("\n\n")

    # classical style
    #   fruits = []
    #   for fruit in fruits_block.split(","):
    #       fruits.append(fruit.strip())
    #
    # Preview: with list comprehension:
    fruits = [fruit.strip() for fruit in fruits_block.split(",")]
    print(f" 1| {fruits=}")

    prices_week = [                         # Nested list comprehension.
        [float(s) for s in row.strip(" []").split(",")]         # strip(chars) removes chars from string.
        for row in prices_block.strip().split("\n")             # float(s) converts string to float.
    ]
    print(f" 2| {prices_week=}")


"""
Topic: Testing
"""

# uv run pytest 0x01/snippets/study_more_teaser.py -v

def calc_sum_directly(n):
    """ Calculates 1+..+n directly. """
    return n * (n + 1) // 2                 # '//' Integer division.

def test_sum_directly_ok():
    """ Test sum function. """
    assert calc_sum_directly(n = 5) == 15

def test_sum_directly_fail():
    """ Test sum function but fails. """
    assert calc_sum_directly(n = 5) == 15+1


if __name__ == "__main__":
    debug_code()
    process_prices()
