# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

""" Task 'Big Pea' """


def counter_add(counter: dict, item):
    """ Increments the count of an item in the provided counter dictionary. """
    counter[item] = counter.get(item, 0) + 1

def counter_subtract(counter: dict, item):
    """ Decrements the count of an item in the provided counter dictionary. """
    if item in counter:
        counter[item] -= 1
        if counter[item] <= 0:
            del counter[item]

def counter_most_common(counter: dict):
    """ Returns the key of the most common item in the provided counter dictionary. """
    # return max(counter.items(), key=lambda x: x[1])[0]        # short version using lambdas

    most_common_key = None
    max_count = float('-inf')
    for key in counter:
        if counter[key] > max_count:
            most_common_key = key
            max_count = counter[key]
    return most_common_key

def count_banana():
    """ How to use counters. """
    banana = {}
    for c in "banana":
        counter_add(banana, c)
    print(f" 1| {banana=}")                                     # {'b': 1, 'a': 3, 'n': 2}

    counter_subtract(banana, 'b')
    print(f" 2| {banana=}")                                     # {'a': 3, 'n': 2}

    print(f" 3| {counter_most_common(banana)=}")                # 'a'

if __name__ == "__main__":
    count_banana()
