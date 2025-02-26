# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

import platform  # a line comment

print(f"Hello World! (python {platform.python_version()})")

"""
Here this is a block comment, with three " " " (without spaces) before and after.
Actually it is a string literal, not a comment in Python. However, whether it 
behaves like a comment depends on how it is used (examples follow).
"""


"""
Summary

Comments
  - More on comments in the next section.
  - https://docs.python.org/3/tutorial/introduction.html#comments
  - https://docs.python.org/3.13/reference/lexical_analysis.html#comments

import
  - The 'platform' module is loaded. 
  - A lot of functionality comes in libraries, i.e. modules. In Python this is 
    called 'batteries included'. We will see more snippets about 'import' later.
  - https://docs.python.org/3.13/reference/import.html

print
  - Output function with string literal and prefix 'f'. 
  - This allows for expressions to be enclosed in a {}. This type of formatting is 
    also known as 'string interpolation' (or 'variable interpolation', 
    'variable substitution' or 'variable expansion').
  - https://docs.python.org/3.13/library/functions.html#print
    
Execution
  - Code is executed from top to bottom.
  
See also
  - https://docs.python.org/3.13/
  - https://docs.python.org/3/tutorial/introduction.html#hello-world
"""
