#!/usr/bin/env python               # Shebang, see below.
# -*- coding: utf-8 -*-             # noqa: UP009

"""
(C) A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

Shows how to make a script runnable (on *nix).

Shebang or Hash-Bang
  - This makes it possible to execute the file directly as a script that
    implicitly invokes the interpreter. This still requires permission to
    execute, e.g. via
        > chmod +x study_hello_script.py
    Use
        > chmod -x study_hello_script.py
    to remove the execution flag again.
  - Note:
      * It is not '#!/usr/bin/python' but '#!/usr/bin/env python'.
        to take virtual environments into account.
      * The shebang is not necessary for the script to work.
      * This specification is only for the *nix faction, and we will
        rarely run the script from the command line as executable.

Encoding
  - For Python 3.x UTF-8 is the default.
"""

import platform

print(f"Hello Script! (python version: {platform.python_version()})")
