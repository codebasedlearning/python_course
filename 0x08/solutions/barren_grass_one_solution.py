# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

""" Task 'Barren Grass' """


class Note:
    def __init__(self):
        self.level = -1

    def __enter__(self):
        self.level += 1
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.level -= 1

    def __call__(self, *args):
        self.print(*args)

    def print(self, *args):
        print("    " * self.level, end='')
        print(*args)


def show_loops():
    items = [2, 3, 5, 7, 11]
    number = 24
    with Note() as note:
        note(" 1| start loops")
        with note:
            for i in items:
                if number % i == 0:
                    note(f"{i} | {number}")
                    with note:
                        if i == 3:
                            note("found 3!")
                note.print(f"{i} checked")
        note.print(" 2| end")


if __name__ == "__main__":
    show_loops()
