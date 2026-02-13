# (C) A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet is about custom exceptions and exception hierarchies.

Teaching focus
  - defining custom exception classes
  - exception hierarchies (catching base vs derived)
  - adding context with raise ... from ...
  - ExceptionGroup and except* (Python 3.11+)

Why custom exceptions?
  - Built-in exceptions (ValueError, TypeError) are generic.
  - Custom exceptions make error handling precise: catch exactly what you
    mean, not everything that happens to be a ValueError.
  - Hierarchies let callers choose their granularity: catch the base class
    for 'any domain error', or a specific subclass for fine-grained handling.

See also
  https://docs.python.org/3/tutorial/errors.html#user-defined-exceptions
  https://docs.python.org/3/library/exceptions.html#ExceptionGroup
  https://peps.python.org/pep-0654/
"""

from utils import print_function_header

"""
Topic: Custom exception classes
"""


# A simple hierarchy: base class + specific subclasses
class PaymentError(Exception):
    """Base exception for all payment-related errors."""


class InsufficientFundsError(PaymentError):
    """Raised when an account lacks funds for a transaction."""

    def __init__(self, balance, amount):
        self.balance = balance
        self.amount = amount
        super().__init__(
            f"Cannot withdraw {amount}: only {balance} available"
        )


class CardExpiredError(PaymentError):
    """Raised when a card's expiration date has passed."""

    def __init__(self, card_id, expired_on):
        self.card_id = card_id
        self.expired_on = expired_on
        super().__init__(
            f"Card '{card_id}' expired on {expired_on}"
        )


@print_function_header
def using_custom_exceptions():
    """ define and raise custom exceptions """

    def withdraw(balance, amount):
        if amount > balance:
            raise InsufficientFundsError(balance, amount)
        return balance - amount

    # catch the specific exception
    try:
        withdraw(100.0, 250.0)
    except InsufficientFundsError as e:
        print(f" 1| caught: {e}")
        print(f" 2| balance={e.balance}, amount={e.amount}")

    # catch the base class -> catches any PaymentError
    try:
        raise CardExpiredError("VISA-1234", "2024-01-31")
    except PaymentError as e:
        print(f" 3| caught via base class: {type(e).__name__}: {e}")


"""
Topic: Exception hierarchies in practice
"""


@print_function_header
def hierarchy_granularity():
    """ catching at different levels of the hierarchy """

    errors = [
        InsufficientFundsError(50, 100),
        CardExpiredError("MC-5678", "2023-06-15"),
    ]

    # fine-grained: handle each type differently
    print(" 1| fine-grained handling:")
    for err in errors:
        try:
            raise err
        except InsufficientFundsError:
            print(" 2|   insufficient funds -> suggest smaller amount")
        except CardExpiredError:
            print(" 3|   card expired -> suggest card renewal")

    # coarse-grained: treat all payment errors the same
    print(" 4| coarse-grained handling:")
    for err in errors:
        try:
            raise err
        except PaymentError as e:
            print(f" 5|   payment problem: {e}")


"""
Topic: Chaining exceptions with 'from'
"""


class ConfigError(Exception):
    """Error in application configuration."""


@print_function_header
def exception_chaining():
    """ raise ... from ... preserves the original cause """

    def load_config(path):
        try:
            # simulate a missing file
            raise FileNotFoundError(f"No such file: '{path}'")
        except FileNotFoundError as e:
            raise ConfigError(f"Cannot load config from '{path}'") from e

    try:
        load_config("/etc/myapp/config.toml")
    except ConfigError as e:
        print(f" 1| caught: {e}")
        print(f" 2| caused by: {e.__cause__}")
        print(f" 3| cause type: {type(e.__cause__).__name__}")

    # without 'from': implicit chaining (less explicit, harder to debug)
    # with 'from':    explicit chaining (the recommended pattern)


"""
Topic: ExceptionGroup and except* (Python 3.11+)
"""


@print_function_header
def exception_groups():
    """ handle multiple exceptions at once with ExceptionGroup """

    # ExceptionGroup bundles multiple exceptions into one
    # useful for concurrent operations where several things can fail at once

    errors = ExceptionGroup("validation failed", [
        ValueError("name must not be empty"),
        TypeError("age must be an int, got str"),
        ValueError("email format invalid"),
    ])

    # except* matches by type across the group
    try:
        raise errors
    except* ValueError as eg:
        print(f" 1| caught {len(eg.exceptions)} ValueErrors:")
        for e in eg.exceptions:
            print(f" 2|   - {e}")
    except* TypeError as eg:
        print(f" 3| caught {len(eg.exceptions)} TypeErrors:")
        for e in eg.exceptions:
            print(f" 4|   - {e}")

    # note: except* can match MULTIPLE handlers for the same ExceptionGroup
    # (unlike regular except, where only one handler runs)


if __name__ == "__main__":
    using_custom_exceptions()
    hierarchy_granularity()
    exception_chaining()
    exception_groups()
