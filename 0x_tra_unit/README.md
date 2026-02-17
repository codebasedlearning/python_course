[© A.Voß, FH Aachen, codebasedlearning.dev](mailto:info@codebasedlearning.dev)

# Unit `0x_tra_unit` – Outlook and Preparation

## Overview

This unit previews advanced topics such as ASTs, the Python disassembler, and metaclasses while also covering exam preparation details.

### Focus

Get a high-level orientation to advanced introspection tools and organize your exam strategy.

## Topics

- AST (teaser)
- Python disassembler (teaser)
- Metaclasses (teaser)
- Exam preparation


## Exam – Golden Words

### Randbedingungen

#### System
Für die Prüfung stehen (voraussichtlich) bereit:
- Python 3.11.1
- Visual Studio Code
- Python Extensions
- Terminal

#### 'Kofferklausur'
- Material: Bücher, Python-Code, Cheat-Sheets, keine Binaries
- Offline, aber Abgabe per Mail (Online-Mail-Zugang notwendig)

#### Ergebnisse
- Veröffentlichung im Ilias (Python-Seite oder Ergebnis-Seite)
- Bei der Identitäts- und Anmeldeprüfung zu Beginn der Prüfung bekommen 
Sie ein Passwort für die Ilias-Ergebnis-Seite und eine Nummer in dieser Form
  - 9C73, oder
  - F48A,

  die Sie sich notieren. Unter dieser Nummer wird das Ergebnis veröffentlicht.
- Es gibt ein detailliertes Punkteschema (wie hier), sodass Sie selber
mit der Angabe Ihrer (Teil)punkte kontrollieren können, was fehlt. 
- Wenn sie hierbei Abweichungen feststellen, die Sie sich nicht erklären können, können Sie das in der Einsicht vorbringen.

Beispiel
- Schema: 
  - A1.a 7P: 1P class, docstring; 2P initializer, parameter name; 2P protected name attribute, read-property name; 1P type hints; 1P `__repr__` with `__dict__`
  - A1.b 3P: 1P abstract class; 2P abstract properties `cost`, `calories`

- Ergebnisse
  - 9C73 A1 .a 3/7 .b 1/3 ... A2 ... => 34/60 Note 3.7
  - F48A A1 .a 7/7 .b 2/3 ... A2 ... => 58/60 Note 1.0

### Topics?

- ???

---

## Tasks

### 👉 Task 'A1 – 🧑‍🍳 Cooking'

Sie entwickeln ein System zur Verwaltung und Analyse von Kochrezepten.
Jedes Rezept besteht aus mehreren Zutaten. Dazu gibt es einen Preis und
Kalorieninformationen.

Aufgaben (a:7P, b:3P, d:4P, d:5P, e:3P, f:8P, Summe=30P), Zeit 1h.

#### a) (7P)

1. Definieren Sie die Klasse `CookingPart` mit einer Beschreibung der Klasse.
2. Instanzen sollen (zunächst) wie folgt erzeugt werden können:
``` 
	part = CookingPart(name="Test")
```
3. Das Argument soll in der Instanz 'protected' gespeichert werden 
und über das Nur-Lese-Property `name` zur Verfügung stehen (Tipp in 5.).
4. Versehen Sie alle Elemente der Klasse mit 'type-hints'. Das wird
im weiteren Code nicht mehr erwartet, Sie dürfen aber.
5. Geben Sie eine Instanz wie folgt aus. 

``` 
	print(f"a) {part=}")
```
Die Ausgabe soll dann das Dictionary der Instanz zeigen, bspw. so
```
a) part={'_name': 'Test'}
```

#### b) (3P)

1. Erweitern Sie die Klasse `CookingPart` zu einer abstrakten Klasse.
2. Fügen Sie zwei abstrakte, Nur-Lese-Properties `cost` (Fliesskomma) und
`calories` (ganzzahlig) hinzu.

Anmerkung: Sie müssen ggf. Code auskommentieren, wo Sie Instanzen erzeugen,
denn die Klasse ist nun abstrakt.

#### c) (4P)

1. Leiten Sie eine Klasse `Ingredient` von `CookingPart` ab und ergänzen Sie
Ihren Code derart, dass in dieser Weise Instanzen erzeugt werden können
```
    flour = Ingredient(ingredient_name="Flour", price_per_unit=0.2, calories_per_unit=360)
```
und die Ausgabe `print(f"c) {flour=}")` diesen Text ausgibt:
```
c) flour={'_name': 'Flour', '_price_per_unit': 0.2, '_calories_per_unit': 360}
```
2. Für die beiden Nur-Lese-Properties nutzen Sie als Rückgabewert die
entsprechenden Attribute.

#### d) (5P)

1. Leiten Sie weiter eine Klasse `Recipe` von `CookingPart` ab und ergänzen
Sie Ihren Code derart, dass in dieser Weise Instanzen erzeugt werden können
```
    butter = Ingredient(ingredient_name="Butter", price_per_unit=1.5, calories_per_unit=720)
    flour_with_butter = Recipe(
        recipe_name="Flour with butter", category="Dessert", 
        ingredients={flour:2,butter:3}
    )
```
und die Ausgabe `print(f"d) {flour_with_butter=}")` diesen Text ausgibt:
```
d) flour_with_butter={'_name': 'Flour with butter', '_category': 'Dessert', '_ingredients': {{'_name': 'Flour', '_price_per_unit': 0.2, '_calories_per_unit': 360}: 2, {'_name': 'Butter', '_price_per_unit': 1.5, '_calories_per_unit': 720}: 3}}
```
Die Werte im Dictionary `ingredients` sind die zugehörigen Mengenangaben 
der verwendeten Ingredienzien, d.h. hier 2 Einheiten `flour` und 3 Einheiten `butter`.
2. Die Gesamtkosten `cost` und -kalorien `calories` eines Rezepts ergeben 
sich natürlich aus den jeweiligen Summen über die Ingredienzien unter
Berücksichtigung der Mengenangaben. Berechnen Sie beides und nutzen Sie 
hierzu `sum` mit einer 'generator expression'.
Im Beispiel ergeben sich `cost=4.9` und `calories=2880`.

#### e) (3P)

Für den Umgang mit Rezepten ergänzen Sie die Klasse so, dass
1.  der Indexzugriff die zugehörige Mengenangabe zurückgibt oder eine 
Ausnahme wirft, sollte diese Ingredienz nicht Teil des Rezepts sein. 
Beispiel
```flour_with_butter[butter]``` ergibt 3.
2. über einen Indexzugriff die Menge geändert werden kann, z.B. so
```flour_with_butter[butter] = 12```.
3. über die Ingredienzien iteriert werden kann, z.B. derart
```
    for ingr, quantity in flour_with_butter:
        print(f" {ingr.name}:{quantity}", end='')
```
#### f) (3P)

Die folgende Zeile `line1` enthält Informationen zum Aufbau der Zeilen einer
Datei. Attribute sind durch Kommata getrennt und jedes Attribut enthält 
hinter dem Zeichen `|` am Ende eine Kurzangabe zum Datentyp (`s`,`f`,`i`).
Hier im Beispiel gibt es drei Attribute (`ingredient_name`,
`price_per_unit` und `calories_per_unit`) mit den zugehörigen Datentypen
`string`, `float` und `int`.
`line2` enthält Daten zu diesen Attributen.
```
    line1 = "ingredient_name|s,price_per_unit|f,calories_per_unit|i"
    line2 = "Sugar, 0.5, 400"
```

1. Entwerfen Sie eine Datenklasse `Attribute`, um ein solches Attribut
mit Namen und Datentyp zu modellieren.
2. In der Klasse gibt es eine statische Fabrikmethode `of`, die aus
einem String wie `ingredient_name|s` in `line1` ein Attribut generiert.
3. Erzeugen Sie aus einem String, der aufgebaut ist wie `line1`, mittels 
einer 'list comprehension' eine Liste von Attributen.
4. Nutzen Sie diese Liste, um aus einer Datenzeile wie `line2` ein Dictionary 
zu generieren, mit dem Sie direkt eine `Ingredient` Instanz erzeugen können.
Der Code für 3. und 4. sieht (unvollständig) so aus
```
    attributes = <todo: list comprehension>
    kwargs = <todo: dictionary>
    sugar = Ingredient(<todo: use kwargs>)
```
Es sind hier keine Dateioperationen gefordert.

---

### 👉 Task 'Exam Preparation' 

Think about how you can prepare.

---

### 👉 Task 'AI Snapshot' – Metaclass vs Decorator

Prompt
- "When should you use a metaclass instead of a class decorator?"

AI Answer A
Use a metaclass when you need to control class creation or enforce rules across subclasses.

AI Answer B
Use a metaclass whenever you want to add a method to a class.

Discuss
- Which answer is correct and why?
- Why is a class decorator often sufficient?

---

### 👉 Task 'AI Snapshot' – `ast` vs `dis`

Prompt
- "Which tool inspects Python bytecode: `ast` or `dis`?"

AI Answer A
`dis` inspects bytecode; `ast` parses source into a syntax tree.

AI Answer B
`ast` inspects bytecode; `dis` parses source into a syntax tree.

Discuss
- Which answer is correct?
- When would you prefer `ast` over `dis`?

---

## Comprehension Check

- What does `dis` show that `ast` does not?
- Why might you inspect bytecode during debugging?
- What is a metaclass in Python?

---
