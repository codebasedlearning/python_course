# (C) A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet demonstrates building command-line interfaces with argparse.

Teaching focus
  - basic parser with positional and optional arguments
  - type conversion and choices
  - subcommands
  - how to test argparse without actually running from the command line

argparse
  - argparse is Python's standard library for building CLI tools.
  - It generates help messages, handles type conversion, validates input,
    and provides a consistent interface for command-line arguments.
  - For more complex CLIs, consider 'click' or 'typer' (third-party).

See also
  https://docs.python.org/3/library/argparse.html
  https://docs.python.org/3/howto/argparse.html
"""

import argparse
import sys

from utils import print_function_header


"""
Topic: Basic argument parsing
"""


@print_function_header
def basic_arguments():
    """ positional and optional arguments """

    parser = argparse.ArgumentParser(
        description="A simple greeting tool",
    )
    # positional argument (required)
    parser.add_argument("name", help="person to greet")

    # optional arguments (prefixed with - or --)
    parser.add_argument("-c", "--count", type=int, default=1,
                        help="number of greetings (default: 1)")
    parser.add_argument("-l", "--loud", action="store_true",
                        help="greet in uppercase")

    # simulate command-line input (instead of sys.argv)
    args = parser.parse_args(["Alice", "--count", "3", "--loud"])

    greeting = f"Hello, {args.name}!"
    if args.loud:
        greeting = greeting.upper()

    for i in range(args.count):
        print(f" {i+1}| {greeting}")

    print(f" 4| parsed: {args}")


"""
Topic: Type conversion and choices
"""


@print_function_header
def types_and_choices():
    """ argparse validates types and restricts values """

    parser = argparse.ArgumentParser(description="File converter")
    parser.add_argument("input", help="input file path")
    parser.add_argument("-f", "--format", choices=["csv", "json", "xml"],
                        default="json", help="output format")
    parser.add_argument("-v", "--verbosity", type=int, choices=[0, 1, 2],
                        default=1, help="verbosity level")

    args = parser.parse_args(["data.txt", "-f", "csv", "-v", "2"])
    print(f" 1| input={args.input}, format={args.format}, verbosity={args.verbosity}")

    # what happens with invalid choices?
    parser2 = argparse.ArgumentParser()
    parser2.add_argument("--level", choices=["low", "mid", "high"])
    try:
        parser2.parse_args(["--level", "ultra"])
    except SystemExit:
        print(f" 2| invalid choice 'ultra' → argparse calls sys.exit(2)")

    # nargs: accept multiple values
    parser3 = argparse.ArgumentParser()
    parser3.add_argument("files", nargs="+", help="one or more files")
    parser3.add_argument("--tags", nargs="*", default=[], help="optional tags")
    args3 = parser3.parse_args(["a.py", "b.py", "--tags", "v1", "release"])
    print(f" 3| files={args3.files}, tags={args3.tags}")


"""
Topic: Subcommands
"""


@print_function_header
def using_subcommands():
    """ subcommands for git-style CLI tools """

    parser = argparse.ArgumentParser(description="Package manager")
    subparsers = parser.add_subparsers(dest="command", help="available commands")

    # 'install' subcommand
    install_parser = subparsers.add_parser("install", help="install a package")
    install_parser.add_argument("package", help="package name")
    install_parser.add_argument("--upgrade", action="store_true")

    # 'list' subcommand
    list_parser = subparsers.add_parser("list", help="list installed packages")
    list_parser.add_argument("--outdated", action="store_true")

    # simulate different commands
    for argv in [
        ["install", "requests", "--upgrade"],
        ["list", "--outdated"],
    ]:
        args = parser.parse_args(argv)
        print(f" 1| command={args.command}, args={vars(args)}")


"""
Topic: Auto-generated help
"""


@print_function_header
def show_help_output():
    """ argparse generates help text automatically """

    parser = argparse.ArgumentParser(
        prog="mytool",
        description="A demonstration CLI tool",
        epilog="Example: mytool input.csv -o output.json -v 2",
    )
    parser.add_argument("input", help="input file")
    parser.add_argument("-o", "--output", default="out.json", help="output file")
    parser.add_argument("-v", "--verbose", action="count", default=0,
                        help="increase verbosity (-v, -vv, -vvv)")

    # print the help text (without exiting)
    print(f" 1| auto-generated help:\n")
    parser.print_help()

    # action='count' allows stacking: -vvv → verbose=3
    args = parser.parse_args(["data.csv", "-o", "result.json", "-vvv"])
    print(f"\n 2| verbosity level: {args.verbose}")


if __name__ == "__main__":
    basic_arguments()
    types_and_choices()
    using_subcommands()
    show_help_output()
