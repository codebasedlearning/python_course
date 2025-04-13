# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
Task 'Canoe Hair'

Topics
  - class
  - property
  - staticmethod
"""


class Window:
    """ base class for a window """
    def __init__(self):
        print(" a|   init Window!")

    def draw(self):
        """ draws a window """
        print(" b|   I am a Window!")

    def __del__(self):
        print(" c|   del Window!")


class Button(Window):
    """ a button """
    def __init__(self):
        super().__init__()
        print(" d|   init Button!")

    def draw(self):
        print(" e|   I am a Button!")

    def __del__(self):
        print(" f|   del Button!")
        super().__del__()


class Checkbox(Window):
    """ a checkbox """
    def __init__(self):
        super().__init__()
        print(" g|   init Checkbox!")

    def draw(self):
        print(" h|   I am a Checkbox!")

    def __del__(self):
        print(" i|   del Checkbox!")
        super().__del__()


def draw_ui():
    """ test Button and Checkbox """

    print(" 1| init all")
    lst = [Button(), Checkbox()]

    print(" 2| draw all")
    for item in lst:
        print(f" 3| {item.__class__.__name__=}")
        item.draw()
    print(" 3| done")

def last_function():
    """ just to see 'del' working as expected """
    print(" 1| ... end, see 'del' before")

if __name__ == "__main__":
    draw_ui()
    last_function()
