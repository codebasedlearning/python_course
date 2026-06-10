# (C) A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet is about logging.

Teaching focus
  - Why logging beats print() for anything beyond quick debugging.
  - Log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL.
  - Configuring handlers, formatters, and loggers.
  - Logging to console and file simultaneously.
  - Per-module loggers via getLogger(__name__).

Key ideas:
  - print() is for user-facing output.
  - logging is for developer-facing diagnostics.
  - The logging module is part of the standard library — no install needed.
  - Log levels let you filter noise without removing code.

More sources:
    https://docs.python.org/3/library/logging.html
    https://docs.python.org/3/howto/logging.html
    https://docs.python.org/3/howto/logging-cookbook.html
    https://realpython.com/python-logging/
"""

import logging
import sys

from utils import print_function_header


# ---------------------------------------------------------------------------
# Module-level logger — one per module is the convention.
# ---------------------------------------------------------------------------

logger = logging.getLogger(__name__)


@print_function_header
def basic_logging():
    """Show the five log levels with the default configuration."""

    # The default level is WARNING, so DEBUG and INFO are hidden.
    logging.debug("01| This is DEBUG — you won't see this by default")
    logging.info("02| This is INFO — also hidden by default")
    logging.warning("03| This is WARNING — visible by default")
    logging.error("04| This is ERROR — always visible")
    logging.critical("05| This is CRITICAL — always visible")

    print()
    print(" Note: only WARNING and above appeared. That's the default level.")


@print_function_header
def configure_basic():
    """Use basicConfig to lower the threshold and add timestamps."""

    # basicConfig only takes effect once per process — subsequent calls
    # are silently ignored unless force=True.
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)-8s] %(message)s",
        datefmt="%H:%M:%S",
        force=True,                     # override any prior basicConfig
    )

    logging.debug("01| Now DEBUG is visible too")
    logging.info("02| INFO is visible as well")
    logging.warning("03| WARNING still works")


@print_function_header
def use_module_logger():
    """Demonstrate per-module loggers — the recommended pattern."""

    # The module-level `logger` was created above with getLogger(__name__).
    # Each logger inherits the root logger's level and handlers unless
    # configured otherwise.
    logger.info("01| This message comes from the module logger")
    logger.warning("02| Module logger at WARNING level")

    # You can check what the effective level is.
    print(f"\n 03| logger name:            {logger.name}")
    print(f" 04| logger effective level:  {logging.getLevelName(logger.getEffectiveLevel())}")


@print_function_header
def custom_handler_and_formatter():
    """Build a logger with a custom console handler and formatter."""

    # Create a dedicated logger — not the root logger.
    custom = logging.getLogger("custom_demo")
    custom.setLevel(logging.DEBUG)

    # Avoid adding duplicate handlers if this function runs twice.
    if not custom.handlers:
        console = logging.StreamHandler(sys.stderr)
        console.setLevel(logging.DEBUG)

        fmt = logging.Formatter(
            "%(asctime)s | %(name)-12s | %(levelname)-8s | %(message)s",
            datefmt="%H:%M:%S",
        )
        console.setFormatter(fmt)
        custom.addHandler(console)

    custom.debug("01| fine-grained diagnostic")
    custom.info("02| informational")
    custom.warning("03| something unexpected")
    custom.error("04| something went wrong")
    custom.critical("05| application cannot continue")


@print_function_header
def log_to_file():
    """Demonstrate logging to a file and the console at the same time."""

    file_logger = logging.getLogger("file_demo")
    file_logger.setLevel(logging.DEBUG)

    if not file_logger.handlers:
        # Handler 1: console (INFO and above)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(
            logging.Formatter("[%(levelname)-8s] %(message)s")
        )

        # Handler 2: file (DEBUG and above — captures everything)
        file_handler = logging.FileHandler("demo.log", mode="w")
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(
            logging.Formatter("%(asctime)s [%(levelname)-8s] %(name)s: %(message)s")
        )

        file_logger.addHandler(console_handler)
        file_logger.addHandler(file_handler)

    file_logger.debug("01| only in the file")
    file_logger.info("02| in both console and file")
    file_logger.warning("03| in both console and file")

    print(f"\n Check 'demo.log' — it should contain all three messages.")


@print_function_header
def logging_with_context():
    """Show how to include variable context in log messages."""

    user = "Alice"
    action = "login"
    duration_ms = 42

    # Prefer %-style in logging calls — it defers string formatting until
    # the message is actually emitted (saves work if the level is filtered).
    logger.warning("01| User %s performed %s in %d ms", user, action, duration_ms)

    # f-strings work too, but the string is always constructed.
    logger.warning(f"02| User {user} performed {action} in {duration_ms} ms")


@print_function_header
def logging_exceptions():
    """Demonstrate exc_info for logging tracebacks."""

    try:
        result = 1 / 0
    except ZeroDivisionError:
        logger.error("01| Something broke — here is the traceback:", exc_info=True)

    print("\n Note: the traceback appears in the log, not as a crash.")


if __name__ == "__main__":
    basic_logging()
    configure_basic()
    use_module_logger()
    custom_handler_and_formatter()
    log_to_file()
    logging_with_context()
    logging_exceptions()
