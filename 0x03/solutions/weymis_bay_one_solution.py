# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
Task 'Weymis Bay'

Topics
  - class
  - property
  - __repr__
  - __getitem__
  - __contains__
  - __iter__
"""

from dataclasses import dataclass, field


@dataclass                                  # instead of: class Spell
class Spell:
    """ class representing a spell """
    name: str
    mana_cost: int
    element: str

    def cast(self):
        """ casts the spell """
        return f"Casting {self.name} ({self.element}) for {self.mana_cost} mana."

    # provided by dataclass
    #
    # def __init__(self, name, mana_cost, element):
    #     self.name = name
    #     self.mana_cost = mana_cost
    #     self.element = element
    #
    # def __repr__(self):
    #     return f"({self.__dict__})"


@dataclass
class Spellbook:
    """ Class representing a spellbook """

    # `init=False` ensures `_spells` is not passed during initialization and
    # is still created as part of the object. Like in
    # def __init__(self):
    #   self._spells = {}
    #
    _spells: dict = field(default_factory=dict, init=False)

    def learn(self, spell):
        """ add a spell to the book """
        self._spells[spell.name.lower()] = spell

    def forget(self, name):
        """ remove a spell from the book """
        self._spells.pop(name.lower(), None)

    def cast(self, name):
        """ cast a spell if it exists """
        spell = self._spells.get(name.lower())
        return spell.cast() if spell else "Spell not known."

    def __contains__(self, name):
        return name.lower() in self._spells

    def __getitem__(self, name):
        return self._spells[name.lower()]

    def __iter__(self):
        return iter(self._spells.values())


"""
Does it make sense to use a data class? 

  - The `Spellbook` class doesn’t primarily handle user-defined data fields 
    that would benefit directly from using `@dataclass`.
    While in this case, the data class only simplifies the initialization 
    of `_spells`, it can be more useful if additional fields were introduced 
    (e.g., metadata for the spellbook like `title` or `author`).
  - Since the `Spell` class mainly stores data (`name`, `mana_cost`, and `element`) 
    and provides a simple method (`cast`), using `@dataclass` is an ideal fit here. 
    The `@dataclass` decorator will automatically handle repetitive tasks like 
    creating the `__init__` and `__repr__` methods. So `Spell` is a good choice 
    for a data class.
"""

def cast_around():
    """ test Spell and Spellbook classes """

    fireball = Spell("Fireball", 30, "fire")
    icebolt = Spell("Icebolt", 20, "ice")
    lightning = Spell("Zap", 25, "lightning")

    print(f" 1| {fireball=}")
    print(f" 2| {icebolt=}")
    print(f" 3| {lightning=}")

    book = Spellbook()
    book.learn(fireball)
    book.learn(icebolt)
    book.learn(lightning)
    print(f" 4| {book=}\n")

    print(f" 5| {book["Fireball"]=}")       # Indexer

    print(f" 6| {book.cast("Zap")=}")

    print(f" 7| {'icebolt' in book=}\n")      # Contains

    print(" 8| all spells:")
    for spell in book:
        print(f"     - {spell}")            # spells in book

if __name__ == '__main__':
    cast_around()
