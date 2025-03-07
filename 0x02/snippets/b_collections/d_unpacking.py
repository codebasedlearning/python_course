# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet discusses (variable) unpacking.

Teaching focus
  - Unpacking is an essential part of the language when it comes to
    easy-to-understand code.
"""


def variable_unpacking():
    """ variable unpacking (multiple variable assignment) """
    print("\nvariable_unpacking\n==================")

    x, y = 1, 2                                                 # component by component, destructuring assignment
    print(f" 1| x,y=1,2: {x=}, {y=}")

    x, y = y, x                                                 # no need for a temp
    print(f" 2| swap x,y: {x=}, {y=}")

    def load_data():
        return True, [1,2,3]
    error, data = load_data()                                   # standard use case
    print(f" 3| error,data: {error=}, {data=}")

    triple = [1, 2, 3]
    a, _, c = triple                                            # '_' means 'unused', it is discarded
    print(f" 4| a,_,c={triple} -> {a=}, {c=}")

    values = [1, 2, 3, 4, 5]
    x1, x2, *xn = values                                        # '*' means 'rest'
    print(f" 5| x1,x2,*xn={values} -> {x1=}, {x2=}, {xn=}")

    dct = {1: "one", 2: "two"}
    print(" 6| for k,v in dict:")
    for k, v in dct.items():                                    # standard use case
        print(f"      k={k}, v={v}")
    print()


if __name__ == "__main__":
    variable_unpacking()


###############################################################################


"""
Summary

Topics
  - 'Variable unpacking', aka 'Multiple Variable Assignment',
    'Destructuring Assignment', 'Decomposition'.
  - First use of the '*'-Operator, aka 'Extended Iterable Unpacking'.

Naming
  - In Python, "unpacking" is the most commonly used and official term 
    for this concept.

See also
  - https://docs.python.org/3/reference/simple_stmts.html#assignment-statements
"""
