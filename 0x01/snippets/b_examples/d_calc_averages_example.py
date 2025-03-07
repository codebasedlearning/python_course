# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This script is intended as a first look at various Python features.

Teaching focus
  - Consider the code as an example of where we want to go.
  - You do not need to understand every detail right away.
  - Code it is not optimal in an algorithmic sense.
"""


# multiline-string-literal, it models fruits (head) with prices per (line per) week
FRUIT_DATA = """
Apple, Banana, Cherry, Mango, Pineapple

[0.123, 0.678, 0.345, 0.980, 0.456]
[0.231, 0.564, 0.897, 0.123, 0.675]
[0.423, 0.942, 0.812, 0.503, 0.256]
[0.134, 0.789, 0.456, 0.234, 0.897]
"""

def data_from_file():
    """ read fruits from file """
    with open("fruit_data.txt", mode="r", encoding="utf-8") as f:
        return f.read()

def read_data_blocks(from_memory=True):                         # default params
    """ read data from memory or from file and return the first two blocks as a tuple"""
    try:                                                        # try-except-finally
        fruits_block, prices_block = ((FRUIT_DATA if from_memory
                                       else data_from_file())
                                      .split("\n\n"))           # list of blocks assigned to two vars
        print(f" 1| raw data block 0: {fruits_block=}")
        print(f"  | raw data block 1: {prices_block=}")
    except IOError as e:
        print(f" 2| io error: {e}")
        fruits_block, prices_block = "?", "0"
    return fruits_block, prices_block                           # returns a tuple (x,y)


def build_fruit_history(fruits_block, prices_block):
    """ convert data blocks into a dict of fruits and their individual prices over time """

    # classical style (but skip)
    # fruits = []                                               # create and fill a list
    # for fruit in fruits_block.split(","):
    #     fruits.append(fruit.strip())

    fruits = [fruit.strip() for fruit in fruits_block.split(",")]  #  list comprehension
    print(f" 3| {fruits=}")

    # def to_float(x): return float(x)                          # local function (not strictly necessary here)
    prices_week = [                                             # nested list comprehension
        [float(s) for s in row.strip("[]").split(",")]          # strip(str) removes chars from string
        for row in prices_block.strip().split("\n")             # float(s) converts string to Float
    ]
    print(f" 4| {prices_week=}")

    # classical style (but skip)
    # num_rows = len(prices_week)
    # num_cols = len(prices_week[0])                            # assuming all rows have the same number of columns
    # prices_fruit = [[0] * num_rows for _ in range(num_cols)]  # a list of lists with num_rows zeros; '_' is a name
    # for row_index in range(num_rows):                         # x^T
    #     for col_index in range(num_cols):
    #         prices_fruit[col_index][row_index] = prices_week[row_index][col_index]

    # prices_fruit = [list(row) for row in zip(*prices_week)]
    prices_fruit = list(zip(*prices_week))                      # zip l1,l2 into (l1_i,l2_i)_i
    print(f" 5| {prices_fruit=}")

    # result = {key: value for key, value in zip(fruits, prices_fruit)}
    fruit_history = dict(zip(fruits, prices_fruit))
    print(f" 6| {fruit_history=}")

    return fruit_history


def calc_average_prices():
    """ calculate average prices """
    fruits_block, prices_block = read_data_blocks(from_memory=True)
    fruit_history = build_fruit_history(fruits_block, prices_block)
    average_prices = [(fruit, sum(values) / len(values)) for fruit, values in fruit_history.items()]
    print(f" 6| {average_prices=}")


if __name__ == "__main__":
    calc_average_prices()


###############################################################################


"""
Summary

Topics
  - default parameters
  - (file) open, read
  - split
  - list, dict comprehension
  - zip
  - local functions

See also
  - https://docs.python.org/3.13/
  - https://docs.python.org/3.13/reference/index.html
  - https://docs.python.org/3.13/library/index.html
"""
