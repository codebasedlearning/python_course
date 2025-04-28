[© 2025, Alexander Voß, FH Aachen, codebasedlearning.dev](mailto:info@codebasedlearning.dev)

# Task `Crossword Puzzle`

> Für einen Zeitschriftenverlag soll ein Programm zur Erstellung von Kreuzworträtseln realisiert werden. 

Sie bekommen eine Menge von Wörtern vorgegeben und sollen diese dann horizontal und 
vertikal so anordnen, dass sie miteinander verbunden sind und möglichst **wenig Platz** einnehmen (minimales Kompaktheitsmass).
Die übrigen Felder werden mit zufälligen Buchstaben aufgefüllt. Die oder der Leser:in
der Zeitschrift muss dann später diese Wörter in dem Buchstabensalat finden. Das Finden ist aber hier 
jetzt _nicht_ die Aufgabe, sondern das _Erstellen_.

(Abschlussprüfung MATSE)


## Beispiel

Zu den Wörtern MATSE, NETT, ESSEN und HUNGER findent man u.a. diese Anordnungen:

```
 H | U | N | G | E | R       H | U | N | G | E | R |   |
---|---|---|---|---|---     ---|---|---|---|---|---|---|---
   |   | E |   | S |           |   |   |   | S |   |   |
---|---|---|---|---|---     ---|---|---|---|---|---|---|---
   |   | T |   | S |           |   |   |   | S |   |   | 
---|---|---|---|---|---     ---|---|---|---|---|---|---|---
 M | A | T | S | E |         M | A | T | S | E |   |   |
---|---|---|---|---|---     ---|---|---|---|---|---|---|---
   |   |   |   | N |           |   |   |   | N | E | T | T
```

Die erste Anordnung nimmt 5 · 6 = 30 Felder ein (Kompaktheitsmass) und ist damit besser als die zweite 
mit 5 · 8 = 40 Feldern.

Zufällig aufgefüllt sieht die erste Variante z.B. so aus:

```
 H | U | N | G | E | R  
---|---|---|---|---|--- 
 A | R | E | F | S | Z  
---|---|---|---|---|--- 
 L | K | T | S | S | B   
---|---|---|---|---|---  
 M | A | T | S | E | G   
---|---|---|---|---|---  
 M | A | Q | V | N | U   
```

Die nachfolgende Anordnung ist ebenfalls erlaubt, denn es müssen keine 'Leerzeilen' zwischen den Wörtern
stehen. Sie ist mit 40 benötigten Feldern allerdings auch schlechter.

```
   |   |   |   | M | 
---|---|---|---|---|---|---|---
   |   |   |   | A | 
---|---|---|---|---|---|---|---
   |   | N | E | T | T 
---|---|---|---|---|---|---|---
   |   |   | E | S | S | E | N
---|---|---|---|---|---|---|---
 H | U | N | G | E | R |   |  
```

Nicht erlaubt hingegen ist die folgende Variante, da es keine Verbindungen zwischen den Wörtern gibt:

```
 M | A | T | S | E | 
---|---|---|---|---|---
 N | E | T | T |   | 
---|---|---|---|---|---
 E | S | S | E | N |  
---|---|---|---|---|---
 H | U | N | G | E | R
```


## Eingabeformat

Die Wörter werden Ihnen in einer Datei in der nachfolgend zu sehenden Form zur Verfügung gestellt:

```
# Beispiel 1, Platz<=28
MATSE, NETT, ESSEN, HUNGER
```

Es gibt eine Kommentarzeile und die Wörter werden als eine 
durch Komma getrennte Aufzählung in einer Zeile angegeben.

Die Angabe 'Platz<=28' im Kommentar soll Ihnen einen Hinweis auf ein mindestens zu erreichendes
Kompaktheitsmass geben. Evtl. finden Sie noch bessere Lösungen (vielleicht aber auch nicht).


## Ausgabeformat

Die Ausgabe auf den Bildschirm soll zunächst die nicht versteckte Anordnung und danach, optional, die
mit zufälligen Buchstaben aufgefüllte Lösung sowie das erreichte Kompaktheitsmass zeigen:

```
# Beispiel 1, Platz<=28
Wörter: MATSE, NETT, ESSEN, HUNGER

Lösung:

 H | U | N | G | E | R 
---|---|---|---|---|---
   |   | E |   | S |   
---|---|---|---|---|---
   |   | T |   | S |   
---|---|---|---|---|---
 M | A | T | S | E |   
---|---|---|---|---|---
   |   |   |   | N |   

Aufgefüllt:
 
 H | U | N | G | E | R  
---|---|---|---|---|--- 
 A | R | E | F | S | Z  
---|---|---|---|---|--- 
 L | K | T | S | S | B   
---|---|---|---|---|---  
 M | A | T | S | E | G   
---|---|---|---|---|---  
 M | A | Q | V | N | U   
 
Diese Lösung nimmt 30 Felder ein (das geht besser).
```

## Weitere Randbedingungen

- Haben die Wörter keine gemeinsamen Buchstaben, z.B. bei SACHE und WORT, dann gibt es auch keine Lösung.
- Haben Sie Wörter, die in anderen enthalten sind, könnten Sie das durchaus ausnutzen, z.B. bei
ECHT und KNECHT.
Die Lösung wird dadurch nicht notwendigerweise besser, denn das 
enthaltene Wort steht als verbindendes Wort nicht mehr zur Verfügung. Daher sollen die Wörter nicht 'eingebettet'
werden.
- Sie brauchen bei mehreren gefundenen Anordnungen mit gleichem minimalen Platzbedarf
nur eine Lösung auszugeben.
- Es ist nicht gefordert, eine Ausgabedatei zu schreiben.
- Wörter werden grossgeschrieben ausgegeben.
- In den Wörtern gibt es keine Umlaute, d.h. diese sind bereits vorab wie üblich ersetzt (Ä=AE usw.)
- In der Implementierung für den Verlag wird zwar gefordert, die Buchstaben noch zu verstecken. In Ihrer
realisierten Lösung können Sie aber auch zunächst darauf verzichten. 


## Weitere Beispiele

Im Ordner 'data' finden Sie Beispiele.


## Aufgabe

Implementieren Sie unter Einhaltung der beschriebenen Randbedingungen ein Programm zur Erstellung von Kreuzworträtseln mit möglichst geringer Kompaktheit.

Viel Erfolg!
