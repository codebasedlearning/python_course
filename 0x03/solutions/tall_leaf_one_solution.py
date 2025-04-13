# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
Task 'Tall Leaf'

Topics
  - class inheritance
"""


class Figure:
    """ base class for a figure """
    def __init__(self, description: str = ""):
        self._description = description
        self.__area_cache = None            # for part 2

    @property
    def description(self):
        """ returns the description """
        return self._description

    @description.setter
    def description(self, value):
        """ sets the description """
        self._description = value

    # def area(self):                       # only part 1
    #     return 0                          # in part 2 we use the cached version
    def area(self):
        """ returns the already calculated area or calculates it before """
        if self.__area_cache is None:
            self.__area_cache = self._calc_area()
        return self.__area_cache

    def _calc_area(self):                   # part 2 only
        """ virtual function to be implemented by derived classes """
        return 0

    def __repr__(self):
        return f"'{self.description}', area: {self.area()}"

class Rectangle(Figure):
    """ class for a rectangle figure """
    def __init__(self, width, length, description: str = ""):
        super().__init__(description)
        self._width = width
        self._length = length

    @property
    def width(self):
        """ returns the width """
        return self._width

    @property
    def length(self):
        """ returns the length """
        return self._length

    # def area(self):                       # only in part 1
    #     return self.length * self.width

    def _calc_area(self):                   # for part 2 we provide the calculation
        return self.length * self.width

    def __repr__(self):
        return f"width={self.width}, length={self.length}, {super().__repr__()}"

def using_geometry():
    """ test figure and rectangle classes """

    point = Figure(description="point")
    print(f" 1| point: {point}")

    rect = Rectangle(width=2, length=3, description="rect")
    print(f" 2| rect: {rect}")

    print(f" 3| check cache: {rect._Figure__area_cache}")   # pylint: disable=protected-access,no-member

if __name__ == "__main__":
    using_geometry()
