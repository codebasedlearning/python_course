# (C) A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
Task 'Bronze Strand'

Topics
  - functions
  - dictionaries
  - if-else
  - for-loop
"""


def counter_add(counter: dict, item):
    """ Increments the count of an item in the provided counter dictionary. """
    counter[item] = counter.get(item, 0) + 1


def counter_sub(counter: dict, item):
    """ Decrements the count of an item in the provided counter dictionary. """
    if (count := counter.get(item, 0)) > 1:
        counter[item] = count - 1
    elif item in counter:
        del counter[item]


def counter_most_common(counter: dict):
    """ Returns the key of the most common item in the provided counter dictionary. """
    most_common_key = None
    max_count = float('-inf')
    for key in counter:
        if counter[key] > max_count:
            most_common_key = key
            max_count = counter[key]
    return most_common_key
    # variant using lambdas:
    #   return max(counter.items(), key=lambda x: x[1])[0]


def count_banana():
    """ How to use counters. """
    banana = {}
    for c in "banana":
        counter_add(banana, c)
    print(f" 1| {banana=}")

    counter_sub(banana, 'b')
    print(f" 2| {banana=}")

    print(f" 3| {counter_most_common(banana)=}")


if __name__ == "__main__":
    count_banana()
