# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet shows some nice functions from itertools.

Teaching focus
  - itertools
"""

import itertools                                                    #


def using_count():
    """ motivate generators """
    print("\nusing_count\n===========")

    print(f" 1| count from 10: ", end='')
    for i in itertools.count(10):           # how can 'count' be implemented?
        print(f"{i} ", end='')
        if i >= 15:
            print()
            break
    gen1 = itertools.count(10)
    data1 = [next(gen1) for _ in range(6)]
    print(f" 2| with comprehension: {data1}")

    gen2 = itertools.count(10)
    data2 = (next(gen2) for _ in range(6))
    print(f" 3| with generator expression: {list(data2)}")

    def my_count(start=0):                  # count with a fixed step
        step = 1
        n = start
        while True:
            yield n
            n += step
    gen4 = my_count(10)
    data4 = (next(gen4) for _ in range(6))
    print(f" 4| with my_count: {list(data4)}")


def using_islice():
    """ motivate generators """
    print("\nusing_islice\n============")

    def islice_light(iterable, cnt):
        for i, element in enumerate(iterable):
            if i >= cnt:
                break
            yield element

    gen1 = itertools.count(10)
    data1 = [next(gen1) for _ in range(6)]                          # as before
    print(f" 1| count with gen1: {data1}")

    gen2 = islice_light(itertools.count(10), 6)                     # 6 times
    data2 = list(gen2)
    print(f"    count with gen2: {data2}")

    gen3 = itertools.islice(itertools.count(10), 6)                 # same as islice
    data3 = list(gen3)
    print(f"    count with gen3: {data3}")

    rg1 = itertools.islice(range(2, 8), 4)                          # index 0..3: 2,3,4,5
    print(f" 2| islice and range1: {list(rg1)}")

    rg2 = itertools.islice(range(2, 8), 4, 6)                       # index 0,1,2,3: 2,3,4,5; 4,5: yield 6,7; 6,7:8,9
    print(f"    islice and range2: {list(rg2)}")                    # -> be careful, it iterates from start to end


def using_repeat():
    """ using itertools.repeat """
    print("\nusing_repeat\n============")

    print(f" 1| repeat 10, 3: {list(itertools.repeat(10, 3))}\n"
          f"    repeat [1,2], 4: {list(itertools.repeat([1,2], 4))}\n"
          f"    repeat map pow 0..9, 2: {list(map(pow, range(10), itertools.repeat(1)))}\n")


def using_chain():
    """ using itertools.chain """
    print("\nusing_chain\n===========")

    gen = (i*i for i in range(6))
    print(f" 1| chain : {list(itertools.chain(range(2,5,2),gen))}\n")


def using_drop_or_takewhile():
    """ using itertools.drop or takewhile """
    print("\nusing_drop_or_takewhile\n=======================")

    data = [1, 4, 9, 16, 25, 23]
    pred = lambda x: x < 10
    print(f" 1| dropwhile x<10, [1,4,9,16,25,23]: {list(itertools.dropwhile(pred, data))}")
    print(f" 2| takewhile x<10, [1,4,9,16,25,23]: {list(itertools.takewhile(pred, data))}\n")


def using_zip():
    """ using zip """
    print("\nusing_zip\n=========")

    chars = ['A', 'B', 'C']
    numbers = [1, 2, 3]
    print(f" 1| zip: {list(zip(chars, numbers))}\n")                # zip not in itertools, but zip_longest


def using_compress():
    """ using itertools.compress """
    print("\nusing_compress\n==============")

    sieve = [1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1]                 # see Task
    numbers = range(0, len(sieve))
    print(f" 1| compress: {list(itertools.compress(numbers, (1-i for i in sieve)))}\n")


if __name__ == "__main__":
    using_count()
    using_islice()
    using_repeat()
    using_chain()
    using_drop_or_takewhile()
    using_zip()
    using_compress()


"""
See https://docs.python.org/3/library/itertools.html
"""
