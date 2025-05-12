# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

""" Task 'Rash Annie' """

from itertools import islice


def gen_factorial():
    def factorial(n=None):
        i, f = 0, 1                                                 # from n=0, 0!=1,..,5!=120
        while True:
            yield f
            if i == n:
                break
            i += 1
            f *= i

    print(f"01| fac_gen(8)={list(factorial(8))}")
    print(f"    fac_gen() ={list(islice(factorial(),9))}\n")


def gen_fibonacci():
    def fibonacci(n=None):
        i, f0, f1 = 1, 0, 1                                         # from n=1, fib_7 = 13
        while True:
            yield f1
            if i == n:
                break
            i += 1
            f0, f1 = f1, f0 + f1

    print(f"02| fib_gen(8)={list(fibonacci(8))}")
    print(f"    fib_gen() ={list(islice(fibonacci(),8))}")


def main():
    gen_factorial()
    gen_fibonacci()


if __name__ == "__main__":
    main()
