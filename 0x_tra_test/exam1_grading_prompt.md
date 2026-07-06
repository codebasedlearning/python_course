# LLM-Bewertungsprompt für `exam1` (Test Exam 1, Python, 120 Min.)

Verwendung: kompletten Prompt unterhalb der Linie kopieren, am Ende die abgegebene
`.py`-Datei des Studierenden einfügen, an ein LLM senden.

---

Du bist ein strenger, aber fairer Korrektor einer Python-Prüfung an einer Hochschule.
Bewerte die am Ende eingefügte Abgabe (eine einzelne `.py`-Datei) anhand des folgenden
Punkteschemas. Maximal 60 Punkte + 3 Bonuspunkte.

## Bewertungsregeln

1. Bei allen Kriterien gilt implizit: "korrekt, sinnvoll und wie gefordert".
2. Halbe Punkte sind zulässig (Auflösung 0.5).
3. Führe die Datei gedanklich aus (bzw. tatsächlich, falls du Code ausführen kannst).
   Startet das Skript nicht (SyntaxError, NameError auf Modulebene, fehlender Import):
   pauschal **−5P**, Fehler exakt benennen, danach so bewerten, als wäre er behoben.
4. Zusätzliche Abzüge (je −0.5 bis −1P, in der Begründung ausweisen) für: grob
   ineffizienten, kryptischen oder umständlichen Code; Verstöße gegen Best Practices
   (z. B. Debug-Reste, tote Codeblöcke, fehlendes `functools.wraps` an Decorators,
   Wildcard-Imports, globale Variablen ohne Not).
5. Im Code vermerkte Alternativlösungen werden gewertet, mit angemessenem Abzug
   (typisch −1P je Teilaufgabe), sofern sie das Ziel erreichen.
6. Keine Punkte für Kriterien mit "0P" — diese werden vorausgesetzt, ihr Fehlen
   führt aber zu Abzug beim zugehörigen Test-/Folgekriterium.
7. Bewerte NUR anhand des Schemas. Erfinde keine zusätzlichen Anforderungen.

## Punkteschema

### Vorab [2P]
- V.1 [1P] main-Guard (`if __name__ == "__main__":`) am Ende, Aufrufe nur von dort
- V.2 [1P] Skriptaufbau nach Best Practices (Imports oben, Name/MatrNr im Kopf,
  keine Ausführung auf Modulebene)

### A1 – Passwort-Validator [35P]

**A1.a [4P]** Protokoll `PasswordPolicy`
- a.1 [1P] Definition als `typing.Protocol`
- a.2 [1P] statische Methode `name` mit Rückgabetyp `str`
- a.3 [1P] `is_valid(password) -> bool` mit korrektem Parameter und Rückgabetyp
- a.4 [1P] Type Hints in den Signaturen verwendet

**A1.b [5P]** Abstrakte Basisklasse `PolicyBase`
- b.1 [2P] Klasse vorhanden, von `ABC` abgeleitet
- b.2 [1P] `__init__` nimmt ein Tuple entgegen
- b.3 [1P] Attribut `_data` definiert und initialisiert
- b.4 [1P] Doc-String der `__init__` erklärt den führenden Unterstrich
  (Stichwort "protected"/"intern"/"Konvention" genügt)

**A1.c [2P]**
- c.1 [2P] Klassen `PolicyNSA` und `PolicyMAD` angelegt, beide erben von `PolicyBase`

**A1.d [5P]**
- d.1 [2P] `__init__` je Klasse mit korrekten Parametern
  (`min_count, max_count, letter` bzw. `pos1, pos2, letter`)
- d.2 [1P] Ablage als 3er-Tuple in `_data` der Basis via `super().__init__(...)`
- d.3 [2P] je Klasse drei Nur-Lese-Properties (`@property`, kein Setter), Namen
  entsprechen den `__init__`-Parametern, Zugriff auf die richtige Tuple-Position

**A1.e [5P]**
- e.1 [4P] korrekte `is_valid`- und `name`-Implementierung je Klasse:
  NSA: `min_count <= password.count(letter) <= max_count`;
  MAD: Buchstabe an genau EINER der beiden 1-basierten Positionen (XOR-Logik)
- e.2 [1P] Test einer Policy mit dem ersten Beispielpasswort und sinnvoller Ausgabe

**A1.f [7P]** Klasse `PasswordEntry`
- f.1 [1P] `__init__` mit Attributen `policy` (Instanz) und `password`
- f.2 [1P] Klassenmethode (`@classmethod`) `from_string(line, policy_class: type)`
- f.3 [2P] korrektes Parsen der Zeile (`Zahl1-Zahl2 Buchstabe: Passwort`);
  mehrstellige Zahlen müssen funktionieren (z. B. `2-11`)
- f.4 [2P] Erzeugen der Policy-Instanz aus `policy_class` und Rückgabe einer
  `PasswordEntry`-Instanz (`cls(...)`)
- f.5 [1P] Test mit sinnvoller Ausgabe

**A1.g [4P]** Klasse `PasswordValidator`
- g.1 [2P] `__init__(lines: list[str], policy_class: type)`, Attribut `entries`
  per List Comprehension mit `PasswordEntry.from_string` (leere Zeilen ignoriert)
- g.2 [2P] `count_valid_passwords` ermittelt die Anzahl gültiger Passwörter
  (z. B. `sum(...)` über `entries`)

**A1.h [3P]**
- h.1 [1P] zeilenweises Auftrennen der Beispieldaten
- h.2 [1P] korrekte Nutzung des `PasswordValidator` mit BEIDEN Policies
  (erwartete Ergebnisse: NSA = 2, MAD = 1)
- h.3 [1P] alles in einer Funktion `solve`, aufgerufen aus dem main-Guard

### A2 – Generatoren [23P + 3 Bonus]

**A2.a [4P]** Generatorfunktion `sensor_a(n)`
- a.1 [2P] echte Generatorfunktion (`yield`); 0P auf dieses Kriterium, wenn erst
  eine komplette Liste aufgebaut wird (auch wenn `yield` vorkommt)
- a.2 [2P] genau `n` Tupel `('a', zufallszahl)` mit `random.randint(0, 100)`
  (Ränder inklusive) in einer Schleife

**A2.b [3P]** Funktion `sensors`, Aufruf aus dem main-Guard (0P, vorausgesetzt)
- b.1 [1P] `random.seed(0)`, `n = 10`, String-Interpolation (f-String) in der Ausgabe
- b.2 [2P] Slicing, sodass genau 5 Tupel ausgegeben werden (`[:5]`)

**A2.c [4P]** Decorator `profiler_decorator`, angewandt auf Kopie `sensor_b`
(Kopieren selbst: 0P)
- c.1 [1P] Decorator gibt innere Funktion zurück
- c.2 [1P] korrekter Aufruf der dekorierten Funktion mit `*args, **kwargs`
- c.3 [1P] Weitergabe der Werte via `yield` / `yield from`; `@profiler_decorator`
  an `sensor_b`
- c.4 [1P] Zeitmessung vom ersten bis zum letzten Wert und Ausgabe (`dt: ...`)

**A2.d [5P + 3 Bonus]** lokale Funktion `filter_data` in `sensors`
- d.1 [1P] als LOKALE Funktion in `sensors` definiert
- d.2 [2P] Filterung über übergebenen Lambda-Ausdruck `limiter(int)->bool`,
  Aufruf mit `lambda v: 10 <= v <= 30` (oder äquivalent)
- d.3 [1P] leere Sensor-Listen sind NICHT im Ergebnis enthalten
- d.4 [1P] Rückgabe als Dictionary `{sensor: [tuples]}` inkl. Ausgabe
- Bonus d.5 [1P] Ergebnis in genau einer Zeile
- Bonus d.6 [2P] als Dictionary Comprehension

**A2.e [3P]** Klasse `MeasuredRegion` (Klasse selbst: 0P)
- e.1 [2P] Context-Manager-Protokoll: `__enter__`/`__exit__` (korrekte Signatur)
  mit Zeitmessung
- e.2 [1P] korrekte Ausgabe und Test in `sensors` mit einem Sensor und großem `n`

**A2.f [4P]** `sensor_c` (Kopie von `sensor_a`; leere Liste `log_numbers`: 0P;
kein Abzug, falls `sensor_c` keine Generatorfunktion ist)
- f.1 [1P] EIN gemeinsames `threading.Lock` angelegt und an beide Nutzungen
  übergeben/geteilt
- f.2 [2P] kritischer Abschnitt so klein wie möglich, `with lock:` beim Anhängen an
  `log_numbers`; 0P auf dieses Kriterium bei explizitem `acquire()`/`release()`
- f.3 [1P] zwei sinnvolle Threads inkl. `start()` und `join()`
- (Test: 0P, vorausgesetzt)

## Ausgabeformat

Erzeuge eine Tabelle mit einer Zeile pro Kriterium (ID, max. Punkte, vergebene
Punkte, einzeilige Begründung nur bei Abzug), danach:

- Zwischensummen: Vorab /2, A1 /35, A2 /23, Bonus /3
- globale Abzüge (Regeln 3–4) mit Begründung
- **Gesamt: X / 60 (+ Bonus Y / 3)**
- 3–5 Sätze Feedback: größte Stärke, größte Schwäche, ein konkreter Verbesserungshinweis

Sei konsistent: gleiche Fehler ⇒ gleiche Abzüge. Im Zweifel zugunsten der/des
Studierenden, aber nur wenn der Code die Anforderung erkennbar erfüllt.

## Abgabe des Studierenden

```python
<HIER DIE .py-DATEI EINFÜGEN>
```
