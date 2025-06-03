[© 2025, Alexander Voß, FH Aachen, codebasedlearning.dev](mailto:info@codebasedlearning.dev)

# Unit `0x09` – Test Exam

## Prüfung Python – Dauer 120 Min.

### Allgemeine Randbedingungen und Anforderungen

- Beachten Sie: Bei jeder Aufgabe gibt es Abzüge, wenn das Programm nicht 
kompiliert, wenn der Code grob ineffizient, kryptisch oder umständlich bzw. 
unverständlich ist. Beachten Sie in Ihrer Implementierung immer auch Best Practices!
- Generell gilt: Sollten Sie bei einer Teilaufgabe nicht auf die gefragte Lösung 
kommen, haben aber eine Alternativlösung, so vermerken Sie das im Code und zur 
Sicherheit als Hinweis auf dem Aufgabenblatt! Die Alternative wird ggf. mit 
Abzügen gewertet, aber Sie kommen weiter. Gleiches gilt, falls die Aufgabenstellung 
an einer Stelle unklar sein sollte.
- Offline: Jede aktive Netzverbindung vor der Abgabe gilt als Täuschungsversuch.
- KI: Jede aktive Form eines KI-unterstützten Code-Assistenten (AI Assistent, 
Copilot etc.) gilt als Täuschungsversuch. Hinweise der IDE in Form von Warnungen 
oder Code-Vervollständigung, z.B. beim Aufruf einer Funktion, sind erlaubt.
- Abgabe: Es wird nur die `.py` Datei als Anhang per Mail an den Dozenten 
gesendet, weitere Dateien werden nicht berücksichtigt! Der Betreff lautet:
`Py_<MatrNr>_<Nachname>`, die Mail hat keinen weiteren Inhalt und geht an
`pruefung.a.voss@fh-aachen.de für Aachen (Prof. Dr. A. Voß)`.
Sollte sich Ihr Mailprogramm weigern, ein Python-Skript zu verschicken, nennen 
Sie es um (`*.txt`) oder zippen Sie die Datei.

Bitte zuerst den gesamten Text lesen! Viel Erfolg!

## Start

- Durchführung: Legen Sie in Ihrer Entwicklungsumgebung ein Projekt an und 
bearbeiten Sie die Aufgaben in *genau einer* Quellcodedatei mit dem Namen
`exam_<MatrNr>_<Nachname>.py`, wobei Sie natürlich die Platzhalter ersetzt haben. 
- Geben Sie Ihren Namen und Ihre Matrikelnummer im Kopf dieser Datei an. 

**Ohne diese Einträge oder bei falschem Dateinamen wird die Prüfung nicht gewertet!**

- [2P] Achten Sie hier auf Best Practices zum Aufbau des Skripts.

## Aufgabe A1 - Passwort-Validator 

### Beschreibung

Sie sollen eine Anwendung in Python erstellen, die Passwörter anhand spezifischer 
Richtlinien überprüft. 

Die Zeilen der Eingabedaten enthalten Informationen, die die jeweilige Richtlinie 
zur Überprüfung benötigt, sowie das Passwort.
Jede nicht-leere Zeile entspricht genau dieser Form `Zahl1-Zahl2 Buchstabe: Passwort`. 
Sie brauchen diesbezüglich keine Fehlerbehandlung zu implementieren. Die Zeichen 
`-` und `:` sind garantierter Teil des Formats. 

Beispiel Eingabedaten:
```
    1-3 a: abcde
    1-3 b: cdefg
    2-11 c: cccccccccccd
```

Die fiktiven (!) Richtlinien der NSA (`PolicyNSA`) und des MADs (`PolicyMAD`) 
könnten wie folgt aussehen:

- Für die NSA ist ein Passwort gültig, wenn der zu untersuchende Buchstabe 
mindestens `Zahl1`-mal und höchstens `Zahl2`-mal vorkommt (jeweils inklusive). 
Danach ist das erste Passwort (`a` kommt in `abcde` einmal vor) und das letzte 
(`c` kommt in `cccccccccccd` 11-mal vor) gültig, das mittlere Passwort hingegen 
nicht (`b` kommt in `cdefg` nicht mindestens einmal vor).

- Dem MAD nach ist ein Passwort dann gültig, wenn im Passwort an den durch 
`Zahl1` und `Zahl2` gegebenen Positionen (Start bei 1) genau einmal (!) der 
angegebene Buchstabe vorkommt. Demnach ist nur das erste Passwort gültig, da 
hier `a` nur an Position 1, nicht jedoch an Position 3 zu finden ist. Im letzten 
Passwort kommt `c` sowohl an Position 2 als auch an Position 11 vor, d.h. nicht 
genau einmal und deshalb ist es ungültig. Weitere Vorkommen des Buchstabens 
sind für die Richtlinie unerheblich.

### Aufgaben

a) [4P] Definieren Sie ein `PasswordPolicy` Protokoll, das eine Methode 
`is_valid` und eine statische Methode `name` deklariert. `is_valid` bekommt 
ein Passwort übergeben und gibt einen Booleschen Wert zurück, ob es gültig 
ist oder nicht. `name` gibt einen String mit dem Namen der Policy zurück. 
Nutzen Sie (nur hier) Type Hints für die Signaturen der Methoden.

b) [5P] Erstellen Sie eine abstrakte Basisklasse `PolicyBase`, die ein der 
Initialisierung übergebenes Tuple als Attribut `_data` speichert.
Ergänzen Sie als Doc-String der Initialisierungsfunktion, welche Funktion 
der führende Unterstrich besitzt.

c) [2P] Legen Sie zunächst die Klassen `PolicyNSA` und `PolicyMAD` nur an. 
Beide erben von `PolicyBase`.

d) [5P] Die Initialisierungsfunktionen der Klassen `PolicyNSA` bzw. `PolicyMAD` 
besitzen die Parameter `min_count`, `max_count` und `letter` bzw. `pos1`, `pos2` 
und `letter`. Legen Sie diese Werte jeweils als 3er-Tuple in der Basisklasse in 
`_data` ab.
Ergänzen Sie die Klassen nun *jeweils* um drei Nur-Lese-Properties, die die 
abgelegten Daten einzeln zur Verfügung stellen. Die Namen der Properties entsprechen 
dabei den Parametern der jeweiligen Initialisierungsfunktion, d.h. in `PolicyNSA` 
gibt es das Property `min_count`, welches den Wert an Position 0 des Tuples `_data` 
der Basis zurückgibt, `max_count` von Position 1 usw. und für `PolicyMAD` entsprechend.

e) [5P] Implementieren Sie für beide Klassen das `PasswordPolicy` Protokoll 
entsprechend der jeweiligen Richtlinie und testen Sie eine davon mit dem ersten 
Passwort der Beispieldaten und einer geeigneten Ausgabe, die z.B. so aussehen könnte:
```
    policy.name()='NSA', policy.min_count=1, policy.max_count=3, policy.letter='a', policy.is_valid('abcde')=True
```

f) [7P] Implementieren Sie eine Klasse `PasswordEntry`, deren Instanzen sowohl 
ein Attribut `policy` für die *Instanz* einer Passwortrichtlinie, als auch ein 
Attribut `password` besitzen. 

Ergänzen Sie die Klasse um eine *Klassenmethode* `from_string`, die eine Zeile 
aus den Eingabedaten und die Passwortrichtlinie als Typ (Type-Hint wäre: `type`) 
übergeben bekommt. 
Diese Funktion erzeugt eine Instanz der Richtlinie mit den aus der Zeile 
extrahierten jeweiligen Argumenten, anschliessend eine `PasswordEntry`-Instanz 
mit Policy und Passwort und gibt diese zurück. 
Testen Sie `from_string` mit einer geeigneten Ausgabe, z.B. dieser:
```
     entry.password='abcde', entry.policy.is_valid(entry.password)=True
```

g) [4P] Implementieren Sie abschliessend eine Klasse `PasswordValidator`, 
deren Initialisierungsfunktion eine Liste von Strings und eine Passwortrichtlinie 
als Typ (!) akzeptiert. 
Weiter stellt die Klasse eine Methode `count_valid_passwords` bereit, die die 
Anzahl der gültigen Passwörter ermittelt und zurückgibt.

In der Initialisierungsmethode überführen Sie die Liste von Strings mittels 
List Comprehension in ein Attribut `entries`, einer Liste von `PasswordEntry`. 
Dazu nutzen Sie natürlich `PasswordEntry.from_string`. Falls die Funktion fehlerhaft 
ist, erzeugen Sie die `PasswordEntry`-Instanzen über die Initialisierungsmethode 
von `PasswordEntry` (siehe auch f) ).

In `count_valid_passwords` nutzen Sie `entries` und die Anzahl gültiger Passwörter 
zu ermitteln und zurückzugeben.

h) [3P] Testen Sie `PasswordValidator` mit beiden Richtlinien und den Beispieldaten 
von oben in einer `solve` Funktion, die Sie aus dem main-Guard aufrufen.

--


## Aufgabe A2 - Generatoren

Platzieren Sie Ihren Code für Aufgabe A2 nach `solve` aus Aufgabe A1 und dem 
main-Guard am Ende.

### Beschreibung

Sie werden zu Beginn einen Sensor implementieren, der im Laufe der Aufgabe 
modifiziert wird. Damit der ursprüngliche Code erhalten bleibt, kopieren 
Sie diesen in einzelnen Teilaufgaben.

Ein Sensor liefert immer Tupel, bestehend aus einem String, der den Sensor 
bezeichnet, und einem ganzzahligen Zufallswert, beispielsweise `('a', 23)` 
für den Wert `23` des Sensors `'a'`.

### Aufgabenstellung

a) [4P] Implementieren Sie eine Generatorfunktion `sensor_a`, die eine ganze 
Zahl `n` übergeben bekommt und genau `n` Tupel, jeweils bestehend aus der 
Sensorbezeichnung `'a'` und einer Zufallszahl aus dem Bereich `[0..100]` 
(inkl. Ränder), liefert.

Tipp 1: Wenn Sie nicht wissen, was eine Generatorfunktion ausmacht, erzeugen 
Sie in `sensor_a` eine Liste von Tupeln. Das gilt auch für weitere 'Sensoren'.
Tipp 2: Einen Zufallszahlengenerator für ganze Zahlen finden Sie in `random`. 

b) [3P] Testen Sie Ihren Generator in einer Funktion `sensors`, die Sie 
ebenfalls aus dem main-Guard aufrufen, und zwar in dieser Art:
```
    random.seed(0)
    n = 10
    numbers_a = list(sensor_a(n))
    print([...])
```
Vervollständigen Sie das `print`-Kommando in `main` und nutzen Sie 
String-Interpolation und Slicing, sodass genau 5 Tupel ausgegeben werden. 
Die Ausgabe könnte so aussehen:
```
    [('a', 49), ('a', 97), ('a', 53), ('a', 5), ('a', 33)] 
```
Tipp: Die Initialisierung mittels `random.seed` führt dazu, dass immer die 
gleichen Zufallszahlen erzeugt werden. 

c) [4P -> Preview] Kopieren Sie die Generatorfunktion `sensor_a` zu `sensor_b` 
und erzeugen Sie wie zuvor Tupel, nur mit der Sensorbezeichnung `'b'`. 

Implementieren Sie einen Decorator `profiler_decorator` und dekorieren Sie damit
`sensor_b`. Der Decorator soll die Zeit messen, die von der Erzeugung des 
ersten Werts bis zur Erzeugung des letzten Werts vergangen ist und abschliessend 
diese Zeit ausgeben (`dt: ...`). Erweitern Sie `sensors` analog
```
    numbers_b = list(sensor_b(n))
    print([...])
```
Die Ausgabe könnte dann so aussehen:
```
    dt: 5.0067901611328125e-06 s
    [('b', 61), ('b', 45), ('b', 74), ('b', 27), ('b', 64)] 
```

Tipp: `time.time()` liefert einen Zeitpunkt.

d) [5P] Die erzeugten Daten aller Sensoren sollen nun gefiltert werden.
Um unabhängig von den anderen Teilaufgaben zu sein, sei dies die Liste aller 
Sensorwerte:
```
    values = [('a', 23), ('a', 28), ('a', 42), ('b', 48), ('b', 45), ('c', 25)]
```

Definieren Sie eine lokale Funktion `filter_data` in `sensors`, die eine Liste 
von Werten (`values`) und einen Lambdaausdruck `limiter(int)->int` bekommt, 
der die Werte auf Gültigkeit testet (filtert).

Das Ergebnis von `filter_data` soll ein Dictionary sein, welches zu jedem Sensor 
(Schlüssel) eine Liste (Wert) aller gültigen Werte dieses Sensors enthält. Dabei 
sollen leere Listen nicht enthalten sein.
Beispiel: Wir sind nur an den Werten im Bereich `[10..30]` interessiert. Rufen Sie 
`filter_data` in `sensors` entsprechend auf und geben Sie das Ergebnis aus. Das 
lautet hier:
```
    {'c': [('c', 25)], 'a': [('a', 23), ('a', 28)]}
```

Bonus [3P] Erzeugen Sie das Ergebnis in `filter_data` als Dictionary Comprehension 
in genau einer Zeile.

e) [3P] Implementieren Sie eine Klasse `MeasuredRegion`, die das Context Manager 
Protokoll implementiert und die Zeit ermittelt und ausgibt, die zwischen Betreten 
und Verlassen liegen.
Testen Sie Ihre Klasse in `sensors`, z.B. mittels `sensor_a` oder `sensor_b` und 
großem `n`. 

f) [4P -> Preview] Beim Verwenden von `sensor_a` mit mehreren Threads gibt es 
merkwürdige Werte, berichtet jemand. Daher sollen alle Werte, die ein Sensor 
dieser Art generiert, zusätzlich in einer gemeinsamen Liste abgelegt werden.

Legen Sie in `sensors` eine leere Liste `log_numbers` an und kopieren Sie Ihre 
Generatorfunktion `sensor_a` zu `sensor_c`. Erweitern Sie nun `sensor_c` geeignet, 
sodass Ihr Code obige Anforderungen erfüllt und grundsätzlich für diese Art der 
parallelen Nutzung geeignet ist.
Testen Sie Ihre Implementierung in `sensors` aussagekräftig mit zwei Threads.

Tipp: Falls Ihr `sensor_a` keine Generatorfunktion ist, sondern direkt eine Liste generiert, 
können Sie diese Aufgabe dennoch vollkommen analog lösen.

--
