# (C) 2024 A.Voß, a.voss@fh-aachen.de, python@codebasedlearning.dev

import platform                                                     # (A) import (see below)

print(f"Hello World! (python {platform.python_version()})")         # (B) print (see below)

"""
This is a block comment, with three " " " (without spaces) before and after.

For comments in the snippets: There are short comments in the code and 
long numbered comments at the end of the file. This is to avoid disturbing 
the reading flow. Example: 
    # (A) Topic
means: Further explanations can be found under (A) at the end of the program.

You can use PyCharm's 'Split Down' function in the context menu of the editor 
tab if you want to see the explanation at the same time as the code. 

---

(A) The 'platform' module is loaded. 
A lot of functionality comes in libraries, i.e. modules. In Python this 
is called 'batteries included'. We will see more snippets about 'import' later.

(B) Output function with string literal and prefix 'f'. 
This allows for expressions to be enclosed in a {}. This type of formatting is 
also known as 'string interpolation' (or 'variable interpolation', 
'variable substitution' or 'variable expansion').
"""
