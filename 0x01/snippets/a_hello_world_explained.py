# '#' starts a line comment. See below for an explanation of the code.
###############################################################################


# (C) A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
Hello World!

Summary:

Execution
  - Code is executed from top to bottom ('top-down execution'), i.e. the
    interpreter reads the code line by line and executes it.
  - https://docs.python.org/3/tutorial/introduction.html

References
  - Usually you can find information about a specific Python feature in the
    official documentation.
  - https://docs.python.org/3/
  - https://docs.python.org/3/tutorial/introduction
  - https://docs.python.org/3/tutorial
  - https://docs.python.org/3/reference
  - https://docs.python.org/3/library
  - https://peps.python.org/pep-0000

Comments
  - '#' starts a line comment, everything after it is ignored by the interpreter.
  - Three " " " (without spaces) starts and ends a multiline or block comment.
    Actually it is a string literal and it is either a (free placed) comment,
    a comment with a special meaning like a function- or module-docstring or
    a multiline string literal.
  - Using triple-quoted strings outside of docstrings can confuse tools (like
    linters or Pylint) because they're typically associated with docstrings.
  - Single-line comments with `#` are more efficient. Triple-quoted strings are
    still treated as strings by the interpreter, i.e. they exist in the code,
    which could have a small performance impact in extreme scenarios.
  - When working with writing tools such as spell checkers or grammar
    improvement software, the leading `#` in Python comments can hinder the
    tool's ability to process the text correctly. In such scenarios, using
    Python's multiline string literals as comments is a practical alternative
    because they don't have the leading `#`. Because of this the warning is
    disabled in Pylint (see .pylintrc).
  - https://docs.python.org/3/tutorial/introduction.html#comments
  - https://docs.python.org/3/reference/lexical_analysis.html#comments

'import'
  - The 'platform' module is loaded.
  - A lot of functionality comes in libraries, i.e. modules. In Python this is
    called 'batteries included'. We will see more snippets about 'import' later.
  - Hold your mouse on 'platform'... (PyCharm) to see the module description.
  - https://docs.python.org/3/reference/import.html

'print'
  - Output function with string literal and prefix 'f'.
  - This allows for expressions to be enclosed in a {}. This type of formatting is
    also known as '(f-)string interpolation' (or 'variable interpolation',
    'variable substitution' or 'variable expansion').
  - https://docs.python.org/3/library/functions.html#print
"""

import platform

print(f"Hello World! (python version: {platform.python_version()})")
