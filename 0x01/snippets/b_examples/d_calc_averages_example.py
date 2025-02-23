# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This script is intended as a first look at various Python features
(it is not optimal in an algorithmic sense).

Please consider the code as an example of where we want to go.
You do not need to understand every detail right away.
"""

# this is a raw-multiline-constant-string, it models fruits (head) with
# prices per (line per) week
fruit_data = """
Apple, Banana, Cherry, Mango, Pineapple

[0.123, 0.678, 0.345, 0.980, 0.456]
[0.231, 0.564, 0.897, 0.123, 0.675]
[0.423, 0.942, 0.812, 0.503, 0.256]
[0.134, 0.789, 0.456, 0.234, 0.897]
[0.345, 0.120, 0.708, 0.659, 0.982]
"""

def read_data_blocks(from_memory=True):                         # default params
    """ read data from memory or from file and return the first two blocks as a tuple"""
    try:                                                        # try-except-finally
        fruits_block, prices_block = ((fruit_data if from_memory
                                       else open("fruit_data.txt", "r").read())
                                      .split("\n\n"))               # list of blocks assigned to two vars
        print(f" 1| raw data block 0: {fruits_block=}")
        print(f"  | raw data block 1: {prices_block=}")
    except IOError as e:
        print(f" 2| io error: {e}")
        fruits_block, prices_block = "?", "0"
    return fruits_block, prices_block                           # returns a tuple (x,y)

def convert_data_blocks(fruits_block, prices_block):
    """ convert data blocks into a list of fruits and a 2d-list (matrix) of prices per day """
    # fruits = []                                               # create and fill a list
    # for fruit in fruits_block.split(","):
    #     fruits.append(fruit.strip())
    fruits = [fruit.strip() for fruit in fruits_block.split(",")]  #  list comprehension
    print(f" 3| {fruits=}")

    # def to_float(x): return float(x)                          # local function (not strictly necessary here)
    prices = [                                                  # nested list comprehension
        [float(s) for s in row.strip("[]").split(",")]          # strip(str) removes chars from string
        for row in prices_block.strip().split("\n")             # float(s) converts string to Float
    ]
    print(f" 4| {prices=}")
    return fruits, prices                                       # a tuple again

def transpose(prices):
    """ transpose price matrix """
    # num_rows = len(prices)
    # num_cols = len(prices[0])                                 # assuming all rows have the same number of columns
    # price_rows = [[0] * num_rows for _ in range(num_cols)]    # a list of lists, each with num_rows zeros; '_' is just a name
    # for row_index in range(num_rows):                         # x^T
    #     for col_index in range(num_cols):
    #         price_rows[col_index][row_index] = prices[row_index][col_index]
    price_rows = [list(row) for row in zip(*prices)]            # Pythonic way
    # price_rows = tuple(zip(*prices))                          # same as tuple, even shorter

    print(f" 5| {price_rows=}")
    return price_rows

def calc_average_prices():
    """ calculate average prices """
    fruits_block, prices_block = read_data_blocks(from_memory=False)
    fruits, prices = convert_data_blocks(fruits_block, prices_block)
    price_rows = transpose(prices)
    average_prices = [ (fruit,sum(values) / len(values)) for fruit,values in zip(fruits,price_rows) ]   # zip l1,l2 into (l1_i,l2_i)_i
    print(f" 6| {average_prices=}")

if __name__ == "__main__":
    calc_average_prices()
