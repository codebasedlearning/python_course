# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

""" Task 'Red Berry' """

from collections.abc import Iterator
from functools import reduce


def introducing_pinq():
    class PINQ(Iterator):
        def __init__(self):
            self._clear()

        def _clear(self, iterable=None):
            self._ops = []
            self._iterable = iterable
            self._generator = None

        def From(self, iterable):
            self._clear(iterable)
            return self

        def Select(self, op):
            self._ops.append((op, lambda _: True))
            return self

        def Where(self, predicate):
            self._ops.append((lambda z: z, predicate))
            return self

        @staticmethod
        def apply(z, op): return (op[0](z) if (op[1](z)) else None) if z is not None else None

        def to_generator(self):
            return (y for x in self._iterable if (y := reduce(PINQ.apply, self._ops, x)) is not None)

        def __iter__(self):
            self._generator = self.to_generator()
            return self

        def __next__(self):
            return self._generator.__next__()

        def to_list(self):
            return list(self.to_generator())

    data = [1, 2, 3]

    gen = PINQ().From(data).Select(lambda x: (x+10)).Where(lambda x: x > 11).to_generator()
    print(f"01| {list(gen)}")

    gen = PINQ().From(data).Select(lambda x: (x+10)).Where(lambda x: x > 11).to_list()
    print(f"02| {gen}")

    gen = PINQ().From(data).Select(lambda x: (x+10)).Where(lambda x: x > 11)
    print(f"03| {list(gen)}")

    gen = PINQ().From(data).Select(lambda x: (x+10, x+100)).Where(lambda x: x[0] > 11)
    print(f"04| {list(gen)}")

    gen = PINQ().From(data).Select(lambda x: x*x).Select(lambda x: x+10).Where(lambda x: x > 11)
    print(f"05| {list(gen.to_list())}")

    gen = PINQ().From(data).Select(lambda x: x*x).Select(lambda x: x+10).Where(lambda x: x > 11).Select(lambda x: x-4)
    print(f"06| {list(gen)}")


def main():
    introducing_pinq()


if __name__ == "__main__":
    main()
