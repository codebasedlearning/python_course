# (C) A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet introduces generator send.

send
  - In PEP 342, support was added for passing values into generator
    https://github.com/qingkaikong/blog-1/blob/f453d320c06ac5b1a8d43380f9e6f9d9cf8c3022/content/2013-04-07-improve-your-python-yield-and-generators-explained.md

  - Remarks: There are more functions like 'send', namely 'close' and 'throw'.
    See https://realpython.com/introduction-to-python-generators
"""

from utils import print_function_header


@print_function_header
def using_generator_send():                 # send... what?
    """ using generator send """

    def count_from(n):                      # idea: count, but set 'start'
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

    x0 = gen_n.send(100)                    # x0 = ?
    x1 = next(gen_n)                        # debug from 'send' with 'step into'
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
    using_generator_send()
