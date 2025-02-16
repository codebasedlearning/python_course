# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

import platform
import sys
import os

# mark color
_m: str = "\033[31m"  # mark red
_M: str = "\033[00m"  # mark off

_home = os.path.expanduser("~")  # expands to something like '/user/name'


def pretty_path(path: str):
    """ Shortens (0x00->...) and anonymizes (home->tilde) the path and removes __init__. """
    return (f".../{path[n:]}" if (n := path.find("0x00")) >= 0 else path.replace(_home, "~")) \
        .replace("/__init__.py", "")


def main():
    """ Prints platform and setup information and attempts to import the cbl package. """
    print(f"{_m}python {platform.python_version()}{_M} {pretty_path(sys.executable)}")
    try:
        import cbl
        print(f"{_m}cbl {cbl.setup.about_package().version}{_M} {pretty_path(cbl.__file__)}")
    except ModuleNotFoundError:  # Error message replaced for didactic reasons.
        return f"{_m}'cbl' package not installed{_M} ('> pip3 install cbl')"


if __name__ == "__main__":
    sys.exit(main())
