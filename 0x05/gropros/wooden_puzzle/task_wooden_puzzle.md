[© 2025, Alexander Voß, FH Aachen, codebasedlearning.dev](mailto:info@codebasedlearning.dev)

# Task `Wooden Puzzle`

Sie sollen ein Holzpuzzle modellieren, und zwar dieses [Rombol](https://rombol.de/en/products/9-loch-puzzle-mittelschweres-interessantes-logik-puzzle-mit-praktischem-verschlussband) bzw. diese [LOGOPLAY Golf Puzzle](https://www.amazon.de/-/en/Wooden-Golf-Puzzle-Jigsaw-Intelligence/dp/B005PWAFQM).

> Ermitteln Sie zu einer gegebenen Menge von Puzzleteilen eine mögliche Lösung des Puzzles, d.h. eine passende Anordnung der Puzzleteile.

(Abschlussprüfung MATSE)


## Beschreibung

Jedes Puzzlestück besteht aus `n` 'Plätzen', die wie folgt aussehen können:
- Halbkugel nach oben (Code 1)
- Halbkugel nach unten (Code 2)
- Halbkugel zu beiden Seiten (Code 3)
- Keine Kugel, kein Loch, nur Holz (Code 4)
- Ein Loch, welches genau eine Halbkugel aufnehmen kann (nicht beide) (Code 0).

Beispiel: Ein Puzzleteil mit drei Plätzen, welches zuerst eine
Halbkugel nach oben, dann nach unten und dann ein Loch besitzt,
wird demnach mit `[1,2,0]` codiert. Dreht man es auf den Kopf,
ist die Codierung `[2,1,0]`. Dreht man es noch um eine Seite, sind es 
die Codierungen `[0,2,1]` bzw. `[0,1,2]`.

Das erste IHK-Beispiel modelliert ein 3x3*2-Puzzle, d.h. zwei Ebenen a 3x3.
Dazu gibt es noch Kommentarzeilen und die Angabe der Dimensionen
(die sich aber auch aus den Puzzleteilen ergeben).

```
// IHK 1
//-------
Dimension 3,3,2
A 1,2,1
B 2,0,1
C 2,1,0
D 2,0,0
E 2,2,1
F 0,1,2
```


## Weitere Randbedingungen

- Beachten Sie, dass in einer Ebene die Puzzleteile nebeneinander liegen
und die einzelnen Ebenen jeweils um 90° gedreht sind (wie bei Jenga).
- Jedes Puzzleteil darf natürlich passend gedreht werden, falls hilfreich.
- Sie können davon ausgehen, dass die Datei syntaktisch korrekt ist.
- Es gibt immer mehrere Lösungen. Es reicht, eine anzugeben.


# Beispiel

Eine mögliche Lösung (und Ausgabe) des IHK-Beispiels ist diese.
Man beachte, dass hier Puzzleteile gedreht wurden.

```
// IHK 1
//-------
Dimension 3,3,2
Anordnung der Teile
Ebene 2
2 1 1 E
1 2 0 C
0 0 1 D
Ebene 1
0 2 2
2 0 1
1 1 2
F B A
```

Die Ausgabe beginnt mit der obersten Ebene und die Puzzleteile
werden von links nach rechts, bzw. von vorne nach hinten ausgegeben.


## Weitere Beispiele

Im Ordner 'data' finden Sie weitere Beispiele.


## Aufgabe

Implementieren Sie unter Einhaltung der beschriebenen Randbedingungen ein Program, das eine passende Anordnung der Puzzleteile bestimmt.

Viel Erfolg!
