# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This is a sample exam task that involves building a cooking system.
"""

from dataclasses import dataclass
from abc import ABC, abstractmethod


"""
A) 7P
1. 1P class, docstring
2. 2P initializer, parameter name
3. 2P protected name attribute, read-property name
4. 1P type hints
5. 1P __repr__ with __dict__ as shown
"""

class CookingPartAOnly:
    """ (Abstract) base class for cooking parts """

    def __init__(self, name: str):
        self._name = name

    @property
    def name(self) -> str:
        """ returns the name of the cooking part """
        return self._name

    def __repr__(self) -> str:
        return f"{self.__dict__}"

"""
B) 3P
1. 1P abstract class
2. 2P abstract properties cost, calories
"""

class CookingPart(ABC):
    """ Abstract base class for cooking parts """

    def __init__(self, name: str):
        self._name = name

    @property
    def name(self) -> str:
        """ returns the name of the cooking part """
        return self._name

    @property
    @abstractmethod
    def cost(self) -> float:
        """ returns the cost of the cooking part """

    @property
    @abstractmethod
    def calories(self) -> int:
        """ returns the calories of the cooking part """

    def __repr__(self) -> str:
        return f"{self.__dict__}"

"""
C) 4P
example
    flour = Ingredient(ingredient_name="Flour", price_per_unit=0.2, calories_per_unit=360)
1. 3P subclass Ingredient, initializers w. correct names (params, attributes), super calls init
2. 1P implement abstract methods cost & calories (return attributes)
"""

class Ingredient(CookingPart):
    """ Class representing an ingredient """

    def __init__(self, ingredient_name: str, price_per_unit: float, calories_per_unit: int):
        super().__init__(name=ingredient_name)
        self._price_per_unit = price_per_unit
        self._calories_per_unit = calories_per_unit

    @property
    def cost(self) -> float:
        return self._price_per_unit

    @property
    def calories(self) -> int:
        return self._calories_per_unit

"""
D) 5P
example
    butter = Ingredient(ingredient_name="Butter", price_per_unit=1.5, calories_per_unit=720)
    flour_with_butter = Recipe(recipe_name="Flour with butter", category="Dessert", ingredients={flour:2,butter:3})

1. 1P subclass Recipe, initializers w. correct names (params, attributes), super calls init
2. 4P implement abstract methods cost & calories, use sum w. generator expression

E) 3P
1. 1P __getitem__
2. 1P __setitem__
3. 1P __iter__ (return iterator)
"""

class Recipe(CookingPart):
    """ Class representing a recipe """

    def __init__(self, recipe_name: str, category: str, ingredients: dict[Ingredient,int]):
        super().__init__(name=recipe_name)
        self._category = category
        self._ingredients = dict(ingredients)

    @property                               # not required
    def category(self) -> str:
        """ returns the category of the recipe """
        return self._category

    @property
    def cost(self) -> float:
        return sum(i.cost*q for i, q in self._ingredients.items())

    @property
    def calories(self) -> int:
        return sum(i.calories*q for i, q in self._ingredients.items())

    def __getitem__(self, ingredient: Ingredient):
        return self._ingredients[ingredient]

    def __setitem__(self, ingredient: Ingredient, quantity: int):
        self._ingredients[ingredient] = quantity

    def __iter__(self):
        return iter(self._ingredients.items())

"""
F) 8P
1. 3P dataclass, 2 attributes, correct data types
2. 2P of
3. 1P list comprehension
4. 2P dict, **kwargs
"""

@dataclass
class Attribute:
    """ Class representing an attribute """
    name: str
    typ: type[str | float | int]

    @staticmethod
    def of(text: str):
        """ creates an Attribute from a text """
        name = text[0:-2]
        suffix = text[-2:]
        typ: type[str | float | int]
        match suffix:
            case "|s": typ = str
            case "|f": typ = float
            case "|i": typ = int
            case _: raise ValueError(f"Unknown type: {suffix}")
        return Attribute(name=name, typ=typ)

def solve():
    """ Solve the exam task """

    # A)
    part = CookingPartAOnly(name="Test")
    print(f"A) {part=}")
    # __str__ => 'part=<__main__.CookingPart object at 0x3e1e250c010>'

    # B)
    # abstract CookingPart

    # C)
    flour = Ingredient(ingredient_name="Flour", price_per_unit=0.2, calories_per_unit=360)
    print(f"C) {flour=}")

    # D)
    butter = Ingredient(ingredient_name="Butter", price_per_unit=1.5, calories_per_unit=720)
    flour_with_butter = Recipe(
        recipe_name="Flour with butter", category="Dessert",
        ingredients={flour:2,butter:3}
    )
    print(f"D) {flour_with_butter=}")

    print(f"   {flour_with_butter.cost=}, {flour_with_butter.calories=}")

    # E)
    print(f"E) {flour_with_butter[butter]=}")

    flour_with_butter[butter] = 12
    print(f"   {flour_with_butter[butter]=}")

    print("   all:", end='')
    for ingr, quantity in flour_with_butter:
        print(f" {ingr.name}:{quantity}", end='')
    print()

    # F)
    line1 = "ingredient_name|s,price_per_unit|f,calories_per_unit|i"
    line2 = "Sugar, 0.5, 400"
    attributes = [Attribute.of(text) for text in line1.strip().split(",")]
    print(f"F) {attributes=}")

    kwargs = {attributes[i].name: attributes[i].typ(s) for i, s in enumerate(line2.strip().split(","))}
    sugar = Ingredient(**kwargs)
    print(f"   {sugar=}")


if __name__ == "__main__":
    solve()
