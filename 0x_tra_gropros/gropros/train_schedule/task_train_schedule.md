[© 2026 Alexander Voß, FH Aachen, codebasedlearning.dev](mailto:info@codebasedlearning.dev)

# Task `Fahrplan für eingleisige Eisenbahnstrecken`

(Idee und Beispiele übernommen aus der Abschlussprüfung MATSE)

In dieser Aufgabe geht es um die Erzeugung von Fahrplänen für eine Eisenbahnstrecke, 
die außer in Bahnhöfen eingleisig ist, z.B. in bergigen Regionen.
Das bedeutet, dass sich entgegenkommende Züge nur in den mehrgleisig ausgebauten **Bahnhöfen** 
begegnen dürfen, nicht jedoch auf der Strecke.

## Eingabedaten

Zur Erzeugung eines Fahrplans sind gegeben:
- die **Bahnhöfe** als `Strecke` (in Buchstaben)
- die **Fahrtzeiten** zwischen den jeweiligen Bahnhöfen (`Abstände` in Minuten)
- die **Abfahrtszeit der Hinfahrt** am ersten Bahnhof (`Start` in Minuten).

Hier im ersten Beispiel zu sehen:

```
Strecke:
A B C
Abstaende:
5 7
Start Hinfahrt:
17
```

## Ausgabedaten

Auszugeben sind die jeweiligen **Abfahrtszeiten** sowie **Wartezeiten** und 
**statistische Daten**, siehe Ausgabeformat.

## Fahrplan-Eigenschaften

### Getakteter Fahrplan

Der Fahrplan ist **getaktet**, d.h. gleiche Züge mit gleichem Ziel fahren an jedem Bahnhof 
immer um genau 60 Minuten versetzt. Ein Zug, der an einem Bahnhof um 7:13 Uhr abfährt, 
fährt auch um 8:13 Uhr, um 9:13 Uhr usw. 

Bei der Planung ist daher zu beachten, dass ein Zug nicht nur einem Gegenzug, sondern auch 
den Folgezügen später begegnen kann.

### Begegnungen und Kollisionsvermeidung

- **In Bahnhöfen** sind Begegnungen unproblematisch.
- **Zwischen Bahnhöfen** ist die Strecke eingleisig, d.h. Begegnungen sind hier nicht 
  zulässig (Kollision).
- Ist der jeweils folgende Streckenabschnitt durch einen Zug belegt, kann der Zug 
  **nicht losfahren** und es entstehen **Wartezeiten**. Diese sollen minimiert werden. 
  Dabei kann es sein, dass Wartezeiten manchmal unvermeidbar sind.

### Mindesthaltezeit am Bahnhof

- An jedem Bahnhof müssen Personen ein- und aussteigen können, d.h. es gibt einen 
  **festen Aufenthaltszeitraum** von zunächst **1 Minute** (weitere Wartezeiten sind möglich).
- Dieser Aufenthaltszeitraum kann ggf. später angepasst werden.

### Sicherheitswartezeit

- Bei Begegnung von Zügen ist eine **Sicherheitswartezeit von 1 Minute** einzuhalten. 
  Das bedeutet, fährt ein Zug in einen Bahnhof ein, kann der wartende Gegenzug frühestens 
  1 Minute später losfahren. 
- Auch dieser Wert soll ggf. später anpassbar sein.

### Sollfahrplan

- Es geht um die Erstellung eines **Sollfahrplans**, d.h. es werden keine möglichen Verspätungen
  einkalkuliert. Die Wartezeiten zählen in diesem Sinne nicht als Verspätung.

## Drei Strategien

Sie sollen mind. diese drei Strategien implementieren.

### 1. Einfache Fahrt

- Diese Strategie bestimmt den **einfachsten Fahrplan** ohne Rücksicht auf Kollisionen.
  Züge in beiden Richtungen fahren nach jedem Halt so schnell es geht weiter.
- In der Regel ist dieser Fahrplan wegen möglicher Kollisionen ungültig, aber er dient 
  als **Referenzplan** für die minimal mögliche Fahrtzeit, die mit keinem gültigen Fahrplan 
  unterschritten werden kann.
- Das Programm markiert in der Ausgabe durch ein `x` zwischen den Bahnhöfen, in deren 
  Streckenabschnitt sich Züge treffen würden, falls der Fahrplan ungültig ist.

### 2. Einseitiges Warten

- Diese Strategie entwirft einen **gültigen Fahrplan** ohne Kollisionen.
  - **Hinfahrt**: schnellstmögliche Verbindung wie bei "Einfache Fahrt".
  - **Rückfahrt**: ein Zug startet nur an einem Bahnhof, wenn sich im folgenden
    Abschnitt gerade kein Zug befindet. 
    Sonst muss er warten, bis der Gegenzug aus diesem Abschnitt eingelaufen ist.
  - Die Sicherheitswartezeit ist immer einzuhalten. 
- Dies führt zu kleinen Wartezeiten, allerdings nur bei Zügen in Rückrichtung.
  Für die Kunden ist dies nicht zufriedenstellend.

### 3. Beidseitiges Warten

- Diese Strategie soll die Schwächen von "Einseitiges Warten" durch eine 
  **'sinnvolle' Verteilung** der Wartezeiten auf beide Richtungen beheben. 
  Dies erhöht die Kundenzufriedenheit.
- Die **Startzeit der Rückfahrt ist frei wählbar**.
- Die Strategie ist ebenso frei wählbar (Ihre Aufgabe), soll aber auch 
  'schnell' ein Ergebnis liefern.

## Bewertung (Score)

- Strategien werden — abgesehen von der Gültigkeit — anhand ihrer 
  **kumulierten zusätzlichen Wartezeiten** für beide Richtungen bewertet. 
- Die zusätzlichen Wartezeiten gehen **quadratisch** in einen möglichst 
  niedrigen Score ein, d.h. eine möglichst **gleichmäßige, auf beide Richtungen verteilte**
  Strategie ist vielversprechend.

### Beispiel

- Angenommen, ein Zug wartet nur in einer Richtung 4 Minuten. Dann ergibt 
  sich ein Score von `4² = 16`.
- Verteilen sich jedoch die Wartezeiten auf beide Richtungen, z.B. jeweils 2 Minuten,
  führt das zu einem niedrigeren Score von `2² + 2² = 8`.

> Hinweis: Fahrpläne nach dieser Strategie sind **nicht eindeutig**.

## Eingabeformat

Wie zuvor schon gesehen, gibt es drei Abschnitte, jeweils mit Header-Zeile:

```
Strecke:
A B C
Abstaende:
5 7
Start Hinfahrt:
17
```

- `Strecke:` — Bahnhofsnamen, Whitespace-getrennt.
- `Abstaende:` — Fahrtzeiten zwischen aufeinanderfolgenden Bahnhöfen (ohne Wartezeiten).
- `Start Hinfahrt:` — Abfahrtszeit der Hinfahrt am ersten Bahnhof, **nur Minutenangabe**.

Die Abfahrtszeit der Rückfahrt hängt von der Strategie ab.

## Ausgabeformat

Zu Beginn werden die Eingabedaten, die **Anzahl der Bahnhöfe** und die **Mindestdauer** 
ausgegeben. Die Mindestdauer ist die Summe der Fahrtdauern der Teilstrecken zuzüglich 
der obligatorischen Haltezeiten an den Zwischenbahnhöfen.

Beispiel: Strecke A–B–C mit Abständen 5 und 7 ergibt eine Mindestdauer von `5 + 1 + 7 = 13` 
(eine Minute Aufenthalt in B).

Anschließend folgen die Fahrpläne (reine Minutenangabe) und Werte zu allen drei Strategien. 
Die Ausgabe zu jeder Strategie beginnt mit dem Namen der Strategie. Die folgenden Zeilen sind:

- `An` — die **Ankunftszeiten** der Hinfahrt
- `Wa` — die **zusätzlichen Wartezeiten** der Hinfahrt
- `Ab` — die **Abfahrtszeiten** der Hinfahrt
- die Namen der Bahnhöfe (Spaltenüberschriften)
- `Ab` — die **Abfahrtszeiten** der Rückfahrt
- `Wa` — die **zusätzlichen Wartezeiten** der Rückfahrt
- `An` — die **Ankunftszeiten** der Rückfahrt

Tabellenform: in der Spalte eines Bahnhofs stehen alle Werte zu diesem Bahnhof.

Anschließend folgen die Kennwerte:

- `Gesamtdauer Hinfahrt, Rückfahrt`
- `Summe Wartezeiten Hinfahrt, Rückfahrt`
- `Summe Strafen` (Score)

## Beispiel 1 — triviale Strecke

Eingabe:

```
Strecke:
A B C
Abstaende:
5 7
Start Hinfahrt:
17
```

Hier liefert bereits "Einfache Fahrt" einen Fahrplan ohne Begegnungen,
d.h. alle drei Strategien sind identisch.

Ausgabe:

```
Strecke:
A B C

Abstaende:
5 7

Start Hinfahrt:
17

Anzahl Bahnhöfe : 3
Mindestdauer    : 13

Einfache Fahrt:
An       22 30
Wa
Ab    17 23
      A  B  C
Ab       39 31
Wa
An    44 38

Gesamtdauer Hinfahrt, Rückfahrt          : 13, 13
Summe Wartezeiten Hinfahrt, Rückfahrt    : 0, 0
Summe Strafen                            : 0

Einseitiges Warten:
An       22 30
Wa
Ab    17 23
      A  B  C
Ab       39 31
Wa
An    44 38

Gesamtdauer Hinfahrt, Rückfahrt          : 13, 13
Summe Wartezeiten Hinfahrt, Rückfahrt    : 0, 0
Summe Strafen                            : 0

Beidseitiges Warten:
An       22 30
Wa
Ab    17 23
      A  B  C
Ab       39 31
Wa
An    44 38

Gesamtdauer Hinfahrt, Rückfahrt          : 13, 13
Summe Wartezeiten Hinfahrt, Rückfahrt    : 0, 0
Summe Strafen                            : 0
```

## Beispiel 2 — (eine) Begegnung unvermeidbar

Eingabe:

```
Strecke:
A B C D E F G
Abstaende:
5 8 6 7 3 2
Start Hinfahrt:
17
```

Mindestdauer = 36 (Summe Fahrtzeiten 31 + 5 Halte in B, C, D, E und F).

Ausgabe:

```
Strecke:
A B C D E F G

Abstaende:
5 8 6 7 3 2

Start Hinfahrt:
17

Anzahl Bahnhöfe : 7
Mindestdauer    : 36

Einfache Fahrt:
An       22 31 38 46 50 53
Wa
Ab    17 23 32 39 47 51
      A  B x C  D  E  F  G
Ab       25 16 09 01 57 54
Wa
An    30 24 15 08 00 56

Gesamtdauer Hinfahrt, Rückfahrt          : 36, 36
Summe Wartezeiten Hinfahrt, Rückfahrt    : 0, 0
Summe Strafen                            : 0

Einseitiges Warten:
An       22 31 38 46 50 53
Wa
Ab    17 23 32 39 47 51
      A  B  C  D  E  F  G
Ab       41 32 09 01 57 54
Wa          (16)
An    46 40 15 08 00 56

Gesamtdauer Hinfahrt, Rückfahrt          : 36, 52
Summe Wartezeiten Hinfahrt, Rückfahrt    : 0, 16
Summe Strafen                            : 256

Beidseitiges Warten:
An       22 31 38 46 50 53
Wa
Ab    17 23 32 39 47 51
      A  B  C  D  E  F  G
Ab       11 02 55 47 43 40
Wa
An    16 10 01 54 46 42

Gesamtdauer Hinfahrt, Rückfahrt          : 36, 36
Summe Wartezeiten Hinfahrt, Rückfahrt    : 0, 0
Summe Strafen                            : 0
```

### Beobachtungen

- "Einfache Fahrt": `x` zwischen B und C. Züge würden sich auf diesem Streckenabschnitt 
  treffen (ungültig).
- "Einseitiges Warten": Begegnung vermeidbar, wenn der Rückfahrt-Zug zusätzlich zu seiner 
  Mindesthaltezeit **16 Minuten in C wartet**. 
  Die 16 Minuten ergeben sich, weil die Hinfahrt erst zu Minute 31 in C eintrifft und der 
  Rückfahrt-Zug die 1 Min Sicherheitswartezeit abwarten muss.
- "Beidseitiges Warten": Geschicktere Wahl der Abfahrtszeit der Rückfahrt eliminiert die 
  zusätzliche Wartezeit.
  Hier verlagert sich der Treffpunkt nach Bahnhof E, wo die Begegnung ohne zusätzliche 
  Wartezeit stattfindet.

## Beispiel 3 — mehrere Begegnungen

Eingabe:

```
Strecke:
A B C D E F G H I J
Abstaende:
12 8 14 3 5 21 13 6 8
Start Hinfahrt:
17
```

Mindestdauer = 98. Jeder Zug der Hinfahrt begegnet 
**mindestens 3 entgegenfahrenden Zügen** der Rückfahrt.

Ausgabe:

```
Strecke:
A B C D E F G H I J

Abstaende:
12 8 14 3 5 21 13 6 8

Start Hinfahrt:
17

Anzahl Bahnhöfe : 10
Mindestdauer    : 98

Einfache Fahrt:
An        29 38 53 57 03 25 39 46 55
Wa
Ab    17  30 39 54 58 04 26 40 47
      A x B  C  D x E  F  G  H  I  J
Ab        22 13 58 54 48 26 12 05 56
Wa
An    34  21 12 57 53 47 25 11 04

Gesamtdauer Hinfahrt, Rückfahrt          : 98, 98
Summe Wartezeiten Hinfahrt, Rückfahrt    : 0, 0
Summe Strafen                            : 0

Einseitiges Warten:
An        29 38 53 57 03 25 39 46 55
Wa
Ab    17  30 39 54 58 04 26 40 47
      A   B  C  D  E  F  G  H  I  J
Ab        30 17 02 58 48 26 12 05 56
Wa       (04)         (04)
An    42  25 16 01 53 47 25 11 04

Gesamtdauer Hinfahrt, Rückfahrt          : 98, 106
Summe Wartezeiten Hinfahrt, Rückfahrt    : 0, 8
Summe Strafen                            : 64

Beidseitiges Warten:
An        29 40 55 59 07 29 43 50 59
Wa       (02)        (02)
Ab    17  32 41 56 02 08 30 44 51
      A   B  C  D  E  F  G  H  I  J
Ab        30 19 04 00 52 30 16 09 00
Wa       (02)        (02)
An    42  27 18 03 57 51 29 15 08

Gesamtdauer Hinfahrt, Rückfahrt          : 102, 102
Summe Wartezeiten Hinfahrt, Rückfahrt    : 4, 4
Summe Strafen                            : 32
```

### Beobachtungen

- "Einfache Fahrt" ungültig (`x` zwischen A–B und D–E). Zufällig auch eine Begegnung im Bahnhof G.
- "Einseitiges Warten" und "Beidseitiges Warten" liefern in Summe die gleichen zusätzlichen 
  Wartezeiten (8 Minuten), aber für die Kunden sind die auf Hin- und Rückfahrt aufgeteilten 
  Wartezeiten angenehmer. Das spiegelt auch der halbierte Score wieder (64 → 32).
- Es kann auch andere Fahrpläne mit gleichem Score geben.
