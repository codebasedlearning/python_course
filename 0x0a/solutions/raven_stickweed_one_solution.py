# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

""" Task 'Raven Stickweed' """

import types


def simulate_class_instance_method():

    class ClassInstanceMethod:
        def __init__(self, f):
            self.f = f

        def __get__(self, obj, cls=None):
            if cls is None:
                cls = type(obj)

            return types.MethodType(self.f, (cls, obj))

    class C:
        def __init__(self, base: int):
            self.base = base

        @ClassInstanceMethod
        def mult(clsSelf, n_times):
            cls, self = clsSelf
            return f"{self.base*n_times=} in {cls}"

    c7 = C(base=7)
    print(f"01| class method:  {c7.mult(5)}")

    class D(C):
        ...

    d4 = D(base=4)
    print(f"02| class method:  {d4.mult(3)}")


def main():
    simulate_class_instance_method()


if __name__ == "__main__":
    main()
