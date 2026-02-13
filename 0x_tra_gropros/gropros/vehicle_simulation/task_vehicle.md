[2025, Alexander Voß, FH Aachen, codebasedlearning.dev](mailto:info@codebasedlearning.dev)

# Task `Vehicle Simulation`

based on GroPro IHK 2025.

## Aufgabenstellung Verkehrssimulation

Die Firma **MATSE Inc.** bietet Beratungsleistungen im Bereich Straßenverkehr 
an und unterstützt Städte bei der Identifikation stauanfälliger Straßenabschnitte. 
Um die Wirkung baulicher Maßnahmen zur Staureduktion besser bewerten zu können, 
sollen Sie eine **Verkehrssimulation** entwickeln.

## Modell und Annahmen

Die Simulation basiert auf einem Stadtplan mit Straßen, die als Verbindungen 
zwischen bestimmten Punkten (Einfallspunkte oder Kreuzungen) dargestellt sind. 
Dabei gilt:

- **Straßen** haben keine Breite, sondern verbinden nur diese Punkte.
- **Fahrtrichtung**: es kann in beide Richtungen gefahren werden, die Darstellung
erfolgt etwas rechts versetzt.
- **Einfallspunkte** sind externe Zufahrten, an denen Fahrzeuge 
**in konstanten Takten** erscheinen. Jeder Einfallspunkt ist mit genau einer 
Kreuzung verbunden.
- **Kreuzungen** leiten Fahrzeuge gemäß einer bestimmten **Gewichtung** weiter
  (Regel folgt). Dabei kehren Fahrzeuge **nie direkt um, also zur Herkunftskreuzung** zurück.
- **Fahrzeuge**:
  - haben eine **eindeutige id**, 
  - fahren mit individueller, **konstanter Geschwindigkeit**,
  - ihre Geschwindigkeit ist **normalverteilt**: Mittelwert 45 km/h, Standardabweichung 10 km/h,
  - können **durch andere hindurchfahren**.
- Beim Verlassen der Karte verschwinden Fahrzeuge.

---

## Eingabeformat (Textdatei)

### Allgemeines

- Kommentarzeilen beginnen mit `#`
- Koordinaten sind **100-m-Einheiten**
- Zeitangaben in **Sekunden**

```
# Simpelfeld
Zeitraum:
50 1

Einfallspunkte:
A 1 1 D 10
B 0 0 D 15
C 2 0 D 16

Kreuzungen:
D 1 0 A 1 B 1 C 2
```

### Abschnitt `Zeitraum:`

Die erste Zahl ist der Endzeitpunkt der Simulation, der Start ist bei t=0.
Die zweite Zahl gibt an, in welchen Zeitschritten eine Ausgabe gemacht werden soll (.s.u).

### Abschnitt `Einfallspunkte:`

Jede Zeile, z.B. `A 1 1 D 10`, enthält den Namen des Einfallspunktes (`A`), 
die XY-Koordinaten (`1 1`), den Namen der folgenden Kreuzung (`D`)
und den Takt (`10`), in dem an diesem Punkt ein neuer Wagen erscheint.

### Abschnitt `Kreuzungen:`

Jede Zeile, z.B. `D 1 0 A 1 B 1 C 2`, enthält den Namen der Kreuzung (`D`),
die XY-Koordinaten (`1 0`), und eine Liste von Punkten, jeweils mit Gewicht, die mit der Kreuzung verbunden sind (`A 1`, `B 1`, `C 2`).

Die Gewichte sind für die Wahl der folgenden Strasse relevant, wenn ein Fahrzeug
an einer Kreuzung ankommt. Das Fahrzeug wählt eine der verfügbaren Straßen zufällig
aus. Allerdings nicht die, aus der es kommt. Dabei sollen die Gewichte
berücksichtigt werden, d.h. im Beispiel ist `D` mit `A`, `B` und `C` verbunden.
Kommt das Fahrzeug von `A`, stehen nur `B` und `C` zur Auswahl, und zwar
mit den Chancen 1:2.

---

## Ausgabeformate

Erstellen Sie pro Testfall einen Ordner mit folgenden Dateien:

### `Plan.txt`

Beispiel
```
0.0 0.0 0.0 1.0
0.0 1.0 0.0 0.0
0.0 1.0 0.0 2.0
0.0 1.0 4.0 1.0
0.0 2.0 0.0 1.0
```
usw.

Diese Datei enthält alle Strassen. Jede Zeile, z.B. `0.0 0.0 0.0 1.0`,
beschreibt eine Strasse durch Angabe der Koordinaten der beiden Endpunkte
(Einfallspunkte oder Kreuzungen).

### `Fahrzeuge.txt`

Beispiel
```
*** t = 0 
*** t = 1
*** t = 2
4.0 2.0 4.0 1.0 0
0.0 0.0 0.0 1.0 1
*** t = 3
4.0 1.87 4.0 1.0 0
```
usw.

Diese Datei enthält für alle Zeitschritte alle jeweils dann sichtbaren Fahrzeuge.
Im Detail: Jede Zeile beschreibt entweder den Zeitschritt (`*** t = 0`) oder 
ein in dem Zeitschritt aktuell existierendes Fahrzeug, 
z.B. `4.0 2.0 4.0 1.0 0`. Hier finden sich zuerst die Koordinaten des Fahrzeugs 
(`4.0 2.0`), dann die Koordinaten des angefahrenen Punktes (`4.0 1.0`) und 
zuletzt die id des Fahrzeugs (`0`).


## Abweichungen zur Originalaufgabe der IHK

Im IHK Original sollen Sie zusätzlich Statistiken über die Auslastung der Strassen
führen, etwa die maximale Anzahl von Fahrzeugen auf einer Strasse je 100m.

Weiterhin soll die Architektur Ihrer Simulation folgende Erweiterungen (ohne
Umsetzung im Original) vorsehen:
- es gibt einen Mindestabstand zum vorausfahrenden Fahrzeug, der eingehalten 
werden muss, ggf. mehrspurige Fahrbahnen, die zum Überholen genutzt werden können.
- es gibt Ampeln oder andere Vorangsregeln an Kreuzungen.
- es gibt max. Geschwindigkeiten je Streckenabschnitt bzw. unterschiedliche
Geschwindigkeiten, die ein Fahrzeug fahren kann.

Da die Erweiterbarkeit Ihres Designs explizit eine Rolle in der Bewertung 
spielt, betrachten wir hier die oben genannte Statistik als optional und 
nehmen folgende konkrete Erweiterungen mit auf:
- es gibt Ampeln an Kreuzungen, die in festen konfigurierbaren Abständen
zwischen Rot und Grün wechseln. Bei Rot bleiben die Fahrzeuge natürlich
stehen (normalerweise).
- es gibt unterschiedliche Fahrzeuge, nämlich die, die sich auch
an rote Ampeln halten, und es gibt Einsatzfahrzeuge, die diese ignorieren.

Überlegen Sie sich, wie Sie die Erweiterungen im Eingabeformat beschreiben.

---

## Visualisierung

Derzeit sind das bereitgestellte Tool `Plot.py` zur Visualisierung und 
die Eingabedaten noch unter dem
[Link](https://www.ihk-zpa.de/opencms/pages/download/pruefungsunterlagen.html)
abrufbar:
- Darstellung der Simulation über die Zeit
- Erstellung eines PNG pro Zeitschritt
- Positionierung der Fahrzeuge abhängig von Fahrtrichtung
- Farbgebung anhand der Fahrzeug-ID

Die Anleitung dazu finden Sie in `Plot_howto.txt`.

### IHK 2

Das zweite IHK-Beispiel könnte so aussehen

[IHK 2](./one_solution/docs/ihk2_t16.png)

`Plan.txt`
``` 
1.00 0.00 2.00 0.00
1.00 0.00 1.00 1.00
1.00 0.00 0.00 0.00
```


## Tipp

- Fangen Sie klein an und testen Sie an einfachen und nachvollziehbaren
Beispielen.

---


