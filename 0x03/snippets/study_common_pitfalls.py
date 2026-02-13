# (C) A.Voss, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet demonstrates common OOP pitfalls in Python.

Teaching focus
  - mutable default arguments in __init__
  - class variable mutation vs instance variables
  - forgetting self in method body
  - is vs == for custom objects

Each pitfall is shown as a broken/fixed pair so students can see the
difference in behavior.
"""

from utils import print_function_header

"""
Topic: Mutable default argument trap
"""


class BrokenShoppingCart:
    """ all instances share the same default list! """

    def __init__(self, items=[]):           # noqa: B006 — intentional bug
        self.items = items

    def add(self, item):
        self.items.append(item)
        return self


class FixedShoppingCart:
    """ each instance gets its own list """

    def __init__(self, items=None):
        self.items = items if items is not None else []

    def add(self, item):
        self.items.append(item)
        return self


@print_function_header
def show_mutable_default_trap():
    """ mutable default argument — broken vs fixed """

    cart_a = BrokenShoppingCart()
    cart_b = BrokenShoppingCart()
    cart_a.add("Milk")

    print(f" 1| cart_a.items = {cart_a.items}")
    print(f" 2| cart_b.items = {cart_b.items}")     # also has "Milk"!
    print(f" 3| same list? {cart_a.items is cart_b.items}")

    cart_x = FixedShoppingCart()
    cart_y = FixedShoppingCart()
    cart_x.add("Bread")

    print(f" 4| cart_x.items = {cart_x.items}")
    print(f" 5| cart_y.items = {cart_y.items}")     # empty, as expected
    print(f" 6| same list? {cart_x.items is cart_y.items}")


"""
Topic: Class variable mutation
"""


class BrokenTeam:
    """ class-level list mutated via instance — affects all instances """
    members = []

    def add(self, name):
        self.members.append(name)           # mutates the class list!
        return self


class FixedTeam:
    """ proper instance variable in __init__ """

    def __init__(self):
        self.members = []

    def add(self, name):
        self.members.append(name)
        return self


@print_function_header
def show_class_variable_mutation():
    """ class variable vs instance variable """

    team_a = BrokenTeam()
    team_b = BrokenTeam()
    team_a.add("Alice")

    print(f" 1| team_a.members = {team_a.members}")
    print(f" 2| team_b.members = {team_b.members}")    # also has "Alice"!
    print(f" 3| same list? {team_a.members is team_b.members}")

    team_x = FixedTeam()
    team_y = FixedTeam()
    team_x.add("Bob")

    print(f" 4| team_x.members = {team_x.members}")
    print(f" 5| team_y.members = {team_y.members}")    # empty, as expected
    print(f" 6| same list? {team_x.members is team_y.members}")


"""
Topic: Forgetting self in method body
"""


class BrokenGreeter:
    """ assigns to local variable instead of self.name """

    def __init__(self, name):
        self.name = name

    def rename(self, new_name):
        name = new_name                     # oops — local variable, not self.name # noqa: F841
        return self


class FixedGreeter:
    """ correctly uses self.name """

    def __init__(self, name):
        self.name = name

    def rename(self, new_name):
        self.name = new_name
        return self


@print_function_header
def show_forgetting_self():
    """ local variable vs self.attribute """

    broken = BrokenGreeter("Alice")
    broken.rename("Bob")
    print(f" 1| broken.name = {broken.name!r}")         # still "Alice"

    fixed = FixedGreeter("Alice")
    fixed.rename("Bob")
    print(f" 2| fixed.name  = {fixed.name!r}")          # "Bob"


"""
Topic: is vs == for custom objects
"""


class Money:
    """ without __eq__, == falls back to identity comparison """

    def __init__(self, amount: int, currency: str):
        self.amount = amount
        self.currency = currency

    def __repr__(self):
        return f"Money({self.amount}, {self.currency!r})"


class ComparableMoney:
    """ with __eq__, == checks value equality """

    def __init__(self, amount: int, currency: str):
        self.amount = amount
        self.currency = currency

    def __eq__(self, other):
        return (isinstance(other, ComparableMoney)
                and self.amount == other.amount
                and self.currency == other.currency)

    def __repr__(self):
        return f"ComparableMoney({self.amount}, {self.currency!r})"


@print_function_header
def show_is_vs_eq():
    """ is vs == — identity vs value equality """

    a = Money(100, "EUR")
    b = Money(100, "EUR")
    print(f" 1| {a=}, {b=}")
    print(f" 2| {(a == b)=}")               # False — no __eq__, falls back to 'is'
    print(f" 3| {(a is b)=}")               # False — different objects

    x = ComparableMoney(100, "EUR")
    y = ComparableMoney(100, "EUR")
    print(f" 4| {x=}, {y=}")
    print(f" 5| {(x == y)=}")               # True — __eq__ compares values
    print(f" 6| {(x is y)=}")               # False — still different objects


if __name__ == "__main__":
    show_mutable_default_trap()
    show_class_variable_mutation()
    show_forgetting_self()
    show_is_vs_eq()
