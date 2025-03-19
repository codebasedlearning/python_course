# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
Task 'Eastern Sands'

Topics
  - functions
  - while-loop
  - try-except
  - input
  - int-conversion
  - print
  - walrus operator (:=)
"""


def read_number():
    """ Read a number from std-input. """
#    while True:
#        if (line := input("Please enter n: ")) == "":
#            break
    while (line := input("Please enter n: ")) != "":
        try:
            n = int(line)
            print(f"Your number was {n}.")
        except ValueError as e:
            print(f"An error occurred: '{e}' -> try again.")


if __name__ == "__main__":
    read_number()
