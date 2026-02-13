# (C) A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet is about running external processes from Python.

Teaching focus
  - subprocess.run() basics
  - capturing output (capture_output, text)
  - error handling (check=True, CalledProcessError)
  - shell=True vs shell=False (security)

subprocess
  - The subprocess module is the recommended way to spawn new processes
    in Python. It replaces os.system(), os.popen(), and the old
    commands module.
  - Always prefer shell=False (the default) to avoid shell injection.

See also
  https://docs.python.org/3/library/subprocess.html
"""

import subprocess
import sys

from utils import print_function_header


"""
Topic: Basic usage
"""


@print_function_header
def basic_subprocess():
    """ run external commands and capture their output """

    # simple command execution
    result = subprocess.run(
        [sys.executable, "--version"],      # list of args (no shell!)
        capture_output=True,                # capture stdout and stderr
        text=True,                          # decode output as text (not bytes)
    )
    print(f" 1| stdout: {result.stdout.strip()}")
    print(f" 2| returncode: {result.returncode}")

    # run a Python one-liner
    result = subprocess.run(
        [sys.executable, "-c", "print(40 + 2)"],
        capture_output=True,
        text=True,
    )
    print(f" 3| python -c result: {result.stdout.strip()}")

    # list directory contents (cross-platform via Python)
    result = subprocess.run(
        [sys.executable, "-c", "import os; print('\\n'.join(os.listdir('.')))"],
        capture_output=True,
        text=True,
    )
    lines = result.stdout.strip().split("\n")
    print(f" 4| current dir has {len(lines)} entries")


"""
Topic: Error handling
"""


@print_function_header
def error_handling():
    """ check=True raises CalledProcessError on non-zero exit codes """

    # without check: you handle the return code yourself
    result = subprocess.run(
        [sys.executable, "-c", "import sys; sys.exit(1)"],
        capture_output=True,
        text=True,
    )
    print(f" 1| exit code (no check): {result.returncode}")

    # with check=True: non-zero exit code raises an exception
    try:
        subprocess.run(
            [sys.executable, "-c", "import sys; sys.exit(42)"],
            capture_output=True,
            text=True,
            check=True,
        )
    except subprocess.CalledProcessError as e:
        print(f" 2| CalledProcessError: exit code {e.returncode}")

    # capture stderr from a failing command
    try:
        subprocess.run(
            [sys.executable, "-c", "raise ValueError('boom')"],
            capture_output=True,
            text=True,
            check=True,
        )
    except subprocess.CalledProcessError as e:
        last_line = e.stderr.strip().split("\n")[-1]
        print(f" 3| stderr last line: {last_line}")


"""
Topic: Timeout and input
"""


@print_function_header
def timeout_and_input():
    """ timeouts prevent hanging, input feeds stdin """

    # timeout: kill the process if it takes too long
    try:
        subprocess.run(
            [sys.executable, "-c", "import time; time.sleep(10)"],
            timeout=0.5,
        )
    except subprocess.TimeoutExpired:
        print(f" 1| process timed out after 0.5s (as expected)")

    # feeding input via stdin
    result = subprocess.run(
        [sys.executable, "-c", "import sys; data=sys.stdin.read(); print(f'got: {data.strip()}')"],
        input="hello from parent",          # feed this to the child's stdin
        capture_output=True,
        text=True,
    )
    print(f" 2| child says: {result.stdout.strip()}")


"""
Topic: Security — shell=True vs shell=False
"""


@print_function_header
def shell_security():
    """ why shell=False is the default and the safe choice """

    # shell=False (default): arguments are passed directly, no shell interpretation
    # shell=True: command is passed to the shell → vulnerable to injection!

    # SAFE: each argument is a separate list element
    result = subprocess.run(
        [sys.executable, "-c", "print('safe')"],
        capture_output=True, text=True,
    )
    print(f" 1| shell=False (safe): {result.stdout.strip()}")

    # DANGEROUS example (DO NOT do this with user input):
    # user_input = "harmless; rm -rf /"  # shell injection!
    # subprocess.run(f"echo {user_input}", shell=True)  # executes the rm!

    print(f" 2| rule: never use shell=True with untrusted input")
    print(f" 3| rule: prefer list of args over string commands")


if __name__ == "__main__":
    basic_subprocess()
    error_handling()
    timeout_and_input()
    shell_security()
