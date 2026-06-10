# (C) A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
Check setup information.
 – Prints platform and setup information.
 – Tries to import the cbl package.
"""

import os
import platform
import sys

_m: str = "\033[31m"                        # mark in red
_M: str = "\033[00m"                        # mark in off


def pretty_path(path: str):
    """ Shortens and anonymizes path. """
    return (f".../{path[n:]}" if (n := path.find("python_course")) >= 0
            else path.replace(os.path.expanduser("~"), "~")
            ).replace("/__init__.py", "")


def main():
    """ Prints platform and setup information and attempts to import the cbl package. """
    print(f"{_m}python version: {platform.python_version()}{_M} ('{pretty_path(sys.executable)}')")
    try:
        import cbl

        print(f"{_m}cbl file: '{pretty_path(cbl.__file__)}'")
        print(f"{_m}cbl version: {cbl.setup.about_package().version}{_M} ")
        print(f"{_m}cbl package: {cbl.setup.about_package()}{_M}")
        print(f"{_m}cbl platform: {cbl.setup.about_platform()}{_M}")
        print(f"{_m}cbl python: {cbl.setup.about_python()}{_M}")
    except ModuleNotFoundError:             # Error message replaced for didactic reasons.
        print(f"{_m}'cbl' package not installed{_M}")


if __name__ == "__main__":
    main()
