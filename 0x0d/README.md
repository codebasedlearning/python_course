[© 2025, Alexander Voß, FH Aachen, codebasedlearning.dev](mailto:info@codebasedlearning.dev)

# Unit `0x0d` – Outlook and Preparation


## Topics covered

- Abstract Syntax Tree (AST) (teaser)
- Python Disassembler (teaser)
- Meta Classes (teaser)


## Tasks

### System

Für die Prüfung stehen (voraussichtlich) bereit:
- Python 3.11.1
- Visual Studio Code
- Python Extensions
- Terminal

---

### 👉 Task '🧑‍🍳 Cooking'

Sie entwickeln ein System zur Verwaltung und Analyse von Kochrezepten.
Jedes Rezept besteht aus mehreren Zutaten. Dazu gibt es einen Preis und
Kalorieninformationen.

Aufgaben (A:7P, B:3P, C:4P, D:5P, E:3P, F:8P, Summe=30P), Zeit 1h.

#### A) (7P)

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
	print(f"A) {part=}")
```
Die Ausgabe soll dann das Dictionary der Instanz zeigen, bspw. so
```
A) part={'_name': 'Test'}
```

#### B) (3P)

1. Erweitern Sie die Klasse `CookingPart` zu einer abstrakten Klasse.
2. Fügen Sie zwei abstrakte, Nur-Lese-Properties `cost` (Fliesskomma) und
`calories` (ganzzahlig) hinzu.

Anmerkung: Sie müssen ggf. Code auskommentieren, wo Sie Instanzen erzeugen,
denn die Klasse ist nun abstrakt.

#### C) (4P)

1. Leiten Sie eine Klasse `Ingredient` von `CookingPart` ab und ergänzen Sie
Ihren Code derart, dass in dieser Weise Instanzen erzeugt werden können
```
    flour = Ingredient(ingredient_name="Flour", price_per_unit=0.2, calories_per_unit=360)
```
und die Ausgabe `print(f"C) {flour=}")` diesen Text ausgibt:
```
C) flour={'_name': 'Flour', '_price_per_unit': 0.2, '_calories_per_unit': 360}
```
2. Für die beiden Nur-Lese-Properties nutzen Sie als Rückgabewert die
entsprechenden Attribute.

#### D) (5P)

1. Leiten Sie weiter eine Klasse `Recipe` von `CookingPart` ab und ergänzen
Sie Ihren Code derart, dass in dieser Weise Instanzen erzeugt werden können
```
    butter = Ingredient(ingredient_name="Butter", price_per_unit=1.5, calories_per_unit=720)
    flour_with_butter = Recipe(
        recipe_name="Flour with butter", category="Dessert", 
        ingredients={flour:2,butter:3}
    )
```
und die Ausgabe `print(f"D) {flour_with_butter=}")` diesen Text ausgibt:
```
D) flour_with_butter={'_name': 'Flour with butter', '_category': 'Dessert', '_ingredients': {{'_name': 'Flour', '_price_per_unit': 0.2, '_calories_per_unit': 360}: 2, {'_name': 'Butter', '_price_per_unit': 1.5, '_calories_per_unit': 720}: 3}}
```
Die Werte im Dictionary `ingredients` sind die zugehörigen Mengenangaben 
der verwendeten Ingredienzien, d.h. hier 2 Einheiten `flour` und 3 Einheiten `butter`.
2. Die Gesamtkosten `cost` und -kalorien `calories` eines Rezepts ergeben 
sich natürlich aus den jeweiligen Summen über die Ingredienzien unter
Berücksichtigung der Mengenangaben. Berechnen Sie beides und nutzen Sie 
hierzu `sum` mit einer 'generator expression'.
Im Beispiel ergeben sich `cost=4.9` und `calories=2880`.

#### E) (3P)

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
#### F) (3P)

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
einem String wie `line1` ein Attribut generiert.
3. Erzeugen Sie mittels einer 'list comprehension' eine Liste von Attributen.
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

### 👉 Lecture Check - Online Questionare

- Please participate in the survey: [Slido](https://wall.sli.do)

---

End of `Unit 0x0d`
