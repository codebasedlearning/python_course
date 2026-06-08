# (C) A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

""" Task 'Coral Ridge' """

import functools


def debug(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        print(f">>> called {func.__name__}({signature})")
        value = func(*args, **kwargs)
        print(f"<<< result {value!r}")
        return value
    return wrapper


@debug
def parse_log_entry(entry: str) -> tuple[str, str]:
    match entry.split(":", 1):
        case ["ERROR", message]:
            return "error", message
        case ["WARN", message]:
            return "warning", message
        case ["INFO", message]:
            return "info", message
        case _:
            return "unknown", entry


def use_parse_log_entry():
    parse_log_entry("ERROR:timeout after 30s")
    parse_log_entry("WARN:retry 2/3")
    parse_log_entry("INFO:started")
    parse_log_entry("DEBUG:verbose output")
    parse_log_entry("malformed entry")


if __name__ == "__main__":
    use_parse_log_entry()
