#!/usr/bin/env python               # (A) Shebang, see below.
# -*- coding: utf-8 -*-             # (B) Encoding, see below.

# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev
#
# Make executable:
#   > chmod +x hello_script.py
# Undo:
#   > chmod -x hello_script.py

import platform

print(f"Hello Script! (python {platform.python_version()})")

"""
(A) Shebang or Hash-Bang. 
    This makes it possible to execute the file directly as a script that 
    implicitly invokes the interpreter. This still requires permission to 
    execute, e.g. via 
            > chmod +x hello_script.py
    Btw, use 
            > chmod -x hello_script.py
    to remove the execution flag again. 
    Attention, it is not '/usr/bin/python' to include virtual environments.
    ->  Omitted. First of all, the specification is only for the *nix 
        faction and secondly, we will rarely run the script from the 
        command line as executable.

(B) Encoding.
    ->  Omitted. For Python 3.x UTF-8 is the default.
"""
