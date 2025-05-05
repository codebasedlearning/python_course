# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
Task 'Cornwin Bay'

Topics
  - Mixin
"""

# pylint: disable=missing-function-docstring, missing-class-docstring, multiple-statements, too-few-public-methods


class PrintableMixin:
    def print(self):
        print(f"[PRINT] {str(self)}")

class User:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"User: {self.name}"

class Server:
    def __init__(self, ip):
        self.ip = ip

    def __str__(self):
        return f"Server IP: {self.ip}"

class PrintableUser(User, PrintableMixin):
    pass

class PrintableServer(Server, PrintableMixin):
    pass

def cornwin_bay():
    print("\ncornwin_bay\n===========")

    u = PrintableUser("Alice")
    s = PrintableServer("192.168.0.1")

    u.print()  # ➜ [PRINT] User: Alice
    s.print()  # ➜ [PRINT] Server IP: 192.168.0.1

if __name__ == '__main__':
    cornwin_bay()
