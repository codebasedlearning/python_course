# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

""" Task 'Poke Peach' """


def fib_itr(n: int) -> int:
    n1, n2 = 0, 1
    for _ in range(n - 1):                                      # default _
        n2, n1 = n2 + n1, n2
        # old = n2; n2 = n2 + n1; n1 = old                      # comments?
    return n2

def fib_rec(n: int) -> int:
    return 1 if n <= 2 else fib_rec(n - 2) + fib_rec(n - 1)

def fib_mem(n: int) -> int:                                      # usually Memoization can be implemented using default
    history: dict[int, int] = {}                                # parameters, but there is a problem with mutable defaults
    def calc_fib(k: int) -> int:                                # local function
        return history.get(k) or history.setdefault(k, 1 if k <= 2 else calc_fib(k - 1) + calc_fib(k - 2)) # None->False
        # some variants:
        #
        # if n in history:                                      # comments?
        #    return history[n]
        #
        # if (fk := history.get(k)) is not None:                # comments?
        #     return fk
        #                                                       # comments?
        # history[k] = (m := 1 if k <= 2 else calc_fib(k - 2) + calc_fib(k - 1))
        # return m
    return calc_fib(n)

def main():
    n = int(input("n: "))
    print(f"Iteratively: {fib_itr(n)=}")
    print(f"Recursively: {fib_rec(n)=}")           # n>=36..
    print(f"Memoization: {fib_mem(n)=}")

if __name__ == "__main__":
    main()
