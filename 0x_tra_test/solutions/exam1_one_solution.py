# (C) A.Voß, a.voss@fh-aachen.de, python@codebasedlearning.dev
# Name: A.Voß, MatrNr: 99999
import functools
import random
import threading
import time
from abc import ABC, abstractmethod
from typing import Protocol  #, Self

"""
Hinweise zur Bewertung:
  - bei allen Kriterien gilt implizit 'korrekt, sinnvoll und wie gefordert'
  - Abzüge gibt es auch für Code, der nicht den 'Best Practices' entspricht,
    obwohl er womöglich das korrekte Ergebnis produziert
  - bei unvollständigen Ansätzen sind auch halbe Punkte möglich
  - zum Teil steht in der Bewertung '0P', das ist kein Fehler, sondern
    der entsprechende Teil wird vorausgesetzt
"""

"""
Vorab: 2P
  - 'main-Guard' am Ende
  
mögliche Punkte:
  - A1: 35
  - A2: 23 + 3 Bonus
  
Gesamt: 2+35+23 = 60 Punkte, mgl. Bonus 3 Punkte
"""

# A1

"""
A1.a [4P]
  .1    1P Definition Protocol 'PasswordPolicy'
  .2    1P statische Methode 'name' mit korrektem Rückgabetyp
  .3    1P 'is_valid' mit korrektem Parameter und korrektem Rückgabetyp
  .4    1P type hints verwendet
"""
class PasswordPolicy(Protocol):
    def is_valid(self, password: str) -> bool:
        ...

    @staticmethod
    def name() -> str:
        ...


"""
A1.b [5P]
  .1    2P Klasse 'PolicyBase', von ABC abgeleitet
  .2    1P __init__ mit tuple
  .3    1P Definition und Initialisierung von '_data'
  .4    1P Stichwort 'protected' oder 'intern' als Erläuterung als Doc-String
"""
class PolicyBase(ABC):
    def __init__(self, data: tuple):
        """ _data, damit es protected ist """
        self._data = data

    @staticmethod
    @abstractmethod
    def name() -> str:
        ...

"""
A1.c [2P]
  .1    2P Klassen 'PolicyNSA' und 'PolicyMAD' sind angelegt
  
A1.d [5P]
  .1    2P __init__ je Klasse mit den korrekten Parametern
  .2    1P Ablage der Parameter im Basistuple via super()
  .3    2P Definition der drei Properties je Klasse

A1.e [5P]
  .1    4P korrekte Implementierung der Funktionen 'is_valid' und 'name' je Klasse
  .2    1P Test
"""
class PolicyNSA(PolicyBase):
    def __init__(self, min_count: int, max_count: int, letter: str):
        super().__init__((min_count, max_count, letter))

    @property
    def min_count(self) -> int:
        return self._data[0]

    @property
    def max_count(self) -> int:
        return self._data[1]

    @property
    def letter(self) -> str:
        return self._data[2]

    def is_valid(self, password: str) -> bool:
        count = password.count(self.letter)
        return self.min_count <= count <= self.max_count

    @staticmethod
    def name() -> str:
        return "NSA"


class PolicyMAD(PolicyBase):
    def __init__(self, pos1: int, pos2: int, letter: str):
        super().__init__((pos1, pos2, letter))

    @property
    def pos1(self) -> int:
        return self._data[0]

    @property
    def pos2(self) -> int:
        return self._data[1]

    @property
    def letter(self) -> str:
        return self._data[2]

    def is_valid(self, password: str) -> bool:
        return (password[self.pos1 - 1] == self.letter) ^ (password[self.pos2 - 1] == self.letter)

    @staticmethod
    def name() -> str:
        return "MAD"


"""
A1.f [7P]
  .1    1P Klasse 'PasswordEntry' mit __init__ Parametern für 'policy' und 'password'
           (type hints waren nicht gefordert)
  .2    1P Klassenmethode 'from_string' mit korrekten Parametern, und
  .3    2P Parsen der Zeile und Ermittlung der Parameter für die Instanzen, 
           hier insb. Berücksichtigung, dass int-Werte nicht nur aus einer Ziffer bestehen, sowie
  .4    2P Erzeugen der korrekten Instanzen 'PasswordPolicy' und 'PasswordEntry'
  .5    1P Test
"""
class PasswordEntry:
    def __init__(self, policy: PasswordPolicy, password: str):
        self.policy = policy
        self.password = password

    # garantiertes Format: "1-3 a: abcde"
    @classmethod
    def from_string(cls, input_string: str, policy_class: type) -> 'PasswordEntry': # or Self
        range_part, letter_part, password = input_string.split()
        min_count, max_count = map(int, range_part.split('-'))
        letter = letter_part[0]
        policy = policy_class(min_count, max_count, letter)
        return cls(policy, password)


"""
A1.g [4P]
  .1    2P Klasse 'PasswordValidator' mit __init__, die
           'entries' korrekt via List Comprehension initialisiert
  .2    2P Summation in 'count_valid_passwords'
"""
class PasswordValidator:
    def __init__(self, lines: list[str], policy_class: type):
        self.entries = [PasswordEntry.from_string(line.strip(), policy_class) for line in lines if line.strip()]

    def count_valid_passwords(self) -> int:
        return sum(entry.policy.is_valid(entry.password) for entry in self.entries)


"""
A1.h [3P]
  .1    1P zeilenweise Auftrennung der Daten
  .2    1P korrekte Nutzung 'PasswordValidator'
  .3    1P in 'solve' mit 'main-Guard'
"""
def solve(input_data: str, policy_class: type[PolicyBase]):
    lines = input_data.splitlines()
    validator = PasswordValidator(lines, policy_class)
    print(f"[{policy_class.name()}] valid passwords: {validator.count_valid_passwords()}")

# end of A1

# A2


"""
A2.a [4P]
  .1    2P Generatorfunktion mit Parameter 'n', d.h. Nutzung von 'yield' 
           keine Punkte hier, falls zuerst eine Liste erzeugt wird, auch wenn 'yield' verwendet wird
  .2    2P korrekte Generierung der 'n' Tuple mit Zufallszahl und Name
           in Schleife
"""
def sensor_a(n):
    # result = []
    for _ in range(n):
        value = random.randint(0, 100)
        yield 'a', value
        # result.append(('a', value))
    # return result


"""
A2.c [4P]
  -     0P Kopieren zu 'sensor_b'
  Decorator 'profiler_decorator' mit 
  .1    1P Rückgabe der inneren Funktion ('wrapped')
  .2    1P korrektem Aufruf der dekorierten Funktion ('func') inkl. Parameter ('*args, **kwargs')
  .3    1P Rückgabe via 'yield' und Dekorieren von 'sensor_b'
  .4    1P Messung der Zeit inkl. Ausgabe
"""
def profiler_decorator(func):
    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        for value in result:
            yield value
        end_time = time.time()
        print(f"    dt: {end_time - start_time} s")
        # return result ## das funktioniert nicht
    return wrapped


@profiler_decorator
def sensor_b(n):
    for _ in range(n):
        value = random.randint(0, 100)
        yield 'b', value


"""
A2.e [3P]
  -     0P Klasse 'MeasuredRegion'
  .1    2P 'Context Manager Protokoll', d.h. '__enter__' und '__exit__'
           inkl. Zeitmessung und Initialisierung
  .2    1P korrekte Ausgabe inkl. Test
"""
class MeasuredRegion:
    def __init__(self):
        self.dt = 0
        self.t0 = 0

    def __enter__(self):
        self.t0 = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.dt = time.time() - self.t0
        print(f"    dt: {self.dt} s")


def sensor_c(n, lk, numbers):
    for _ in range(n):
        value = random.randint(0, 100)
        with lk:
            numbers.append(value)
        yield value


"""
A2.b [3P]
  -     0P 'sensors' mit Aufruf aus 'main-Guard'
  .1    1P String-Interpolation und korrekte Ausgabe
  .2    2P Slicing
"""
def sensors():
    random.seed(0)
    n = 10

    numbers_a = list(sensor_a(n))
    print(f" 3| {numbers_a[:5]}")

    # x = sensor_b(n)
    # print(type(x))

    numbers_b = list(sensor_b(n))
    print(f" 4| {numbers_b[:5]}")

    values = [('a', 23), ('a', 28), ('a', 42), ('b', 48), ('b', 45), ('c', 25)]

    """
    A2.d [5P]
      .1    1P lokale Funktion 'filter_data' in 'sensors'
      .2    2P Filtern der passenden Werte, d.h. Verwendung und Aufruf mit Lambda 
      .3    1P Herausfiltern der leeren Mengen (Sensor 'b')
      .4    1P Erzeugung und Rückgabe als dict
    Bonus:
      .5    1P eine Zeile 
      .6    2P als Dictionary Comprehension
    """
    def filter_data(tupels, limiter):
        # all_sensors = set(x[0] for x in tupels)
        # all_valid = {s: [x for x in tupels if x[0] == s and limiter(x[1])] for s in all_sensors}
        # result = {s: l for s, l in all_valid.items() if l}
        # return result
        return {s: l for s, l in {s: [x for x in tupels if x[0] == s and limiter(x[1])]
                                  for s in set(x[0] for x in tupels)}.items() if l}

    filtered_data = filter_data(values, lambda x: 10 <= x <= 30)
    print(f" 5| {filtered_data}")

    numbers_c = []
    with MeasuredRegion():
        numbers_c.extend(list(sensor_b(100000)))
    print(f" 6| {numbers_c[:5]}")

    """
    A2.f [4P]
      -     0P leere Liste 'log_numbers'
      -     0P Kopieren zu 'sensor_c', kein Abzug, falls 'sensor_c' keine Generatorfunktion ist
      .1    1P Lock: Anlegung, Übergabe und Nutzung eines gemeinsamen Locks für 'sensor_c'
      .2    2P in 'sensor_c' eine möglichst kleine kritische Region und Verwendung von 'with' 
               beim Füllen von 'log_numbers';
               keine Punkte hier, falls explizites 'lock' und 'unlock'
      .3    1P Anlegen zweier sinnvollen Threads inkl. 'join'
      -     0P Test
    """
    random.seed(0)
    numbers_lock = threading.Lock()
    log_numbers = []
    numbers_d1 = []
    numbers_d2 = []
    threads = [
        threading.Thread(target=lambda: numbers_d1.extend((3, value) for value in sensor_c(n, numbers_lock, log_numbers)), args=()),
        threading.Thread(target=lambda: numbers_d2.extend((4, value) for value in sensor_c(n, numbers_lock, log_numbers)), args=())
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print(f" 7| {numbers_d1[:5]}")
    print(f" 8| {numbers_d2[:5]}")

    print(f" 9| {len(log_numbers)=}, {log_numbers}")


# end of A2


def main():
    # A1

    # Beispiel 1
    pw = 'abcde'
    policy = PolicyNSA(1, 3, 'a')
    print(f" 1| {policy.name()=}, {policy.min_count=}, {policy.max_count=}, {policy.letter=}, {policy.is_valid(pw)=}")

    # Beispiel 2
    # entry = PasswordEntry(policy, pw)
    entry = PasswordEntry.from_string("1-3 a: abcde", PolicyNSA)
    print(f" 2| {entry.policy.name()}, {entry.password=}, {entry.policy.is_valid(entry.password)=}")

    data = """
    1-3 a: abcde
    1-3 b: cdefg
    2-11 c: cccccccccccd
    """
    solve(data, PolicyNSA)
    solve(data, PolicyMAD)

    # A2
    sensors()


if __name__ == "__main__":
    main()
