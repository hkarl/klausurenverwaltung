***************************
Wie benutzt man TestMacher?
***************************


Grundidee
*********

TestMacher soll Lehrern das Erstellen von Tests erleichtern und beschleunigen. 

- In einer Datenbank werden Frage/Antwortpaare eingepflegt. 
- Es gibt derzeit 

  - Frage mit freier Antwort 
  - Multiple-Choice-Fragen 

- Beim Eingeben von Fragen und Antworten wird LaTeX eingegeben. 

  - Das kann man entweder nutzen (sehr zu empfehlen!) oder (fast) komplett ignorieren. Wenn man es ignorieren möchte, muss man nur bei einigen wenigen Sonderzeichen aufpassen, z.B. ein % Zeichen kann nicht direkt eingeben werden sondern muss als \\% geschrieben werden, ebenso das Kaufmannsund &. Siehe LaTeX-Beschreibungen. 

- Selbst angelegte Frage-/Antwortpaare können editiert werden; Paare von Kollegen nur angeschaut und benutzt werden.
- Frage/Antwort-Paare können klassifiziert werden nach: 

  - Fach 
  - Stufe 
  - Reihe 
  - Frei vergebbaren Schlagworten 

- Aus den vorhandenen Frage/Antwortpaaren kann ein Test zusammengestellt werden. Dabei können die Fragen nach Ersteller, Fach, Stufe, Reihe, und Schlagworten (bzw. Kombinationen davon) gefiltert werden. 
- Aus den so vorgefilterten Paaren kann eine Auswahl getroffen werden, die dann den eigentlichen Test bilden  
- Für einen Test können weitere Parameter angegeben werden, z.B. 

  - die Anzahl der Schüler 
  - die Anzahl der Varianten (Varianten unterscheiden sich durch zufällig gewählte Reihenfolge der Fragen und, bei multiple-choice-Fragen, durch zufällig gewählte Reihenfolge der Antwort-Alternativen)

- Auf Grundlage dieser Werte wird der eigentliche Test erstellt. Dann wird eine Webseite angezeigt mit Links zu PDF files, in verschiedenen Varianten: die gesamte Klausur, Klausur mit Lösungen, Klassensatz (mit und ohne Lösungen), etc. Ebenso, die generierten TeX-Files, galls hemand genauer nachschauen möchte. Typischerweise, einfach den Klassensatz anklicken und ausdrucken. 


Nutzungsmodelle
***************

Eigene Installation
===================

TestMacher wurde mit python, Django, und LaTeX entwickelt. Unter Linux und OSX (die eigentlich Heimat von TestMacher) ist es kein Problem, eine eigene  Instanz aufzusetzen und lokal damit zu arbeiten. Details sind im Kapitel :ref:`installation-link` beschrieben. 

Vorteile: 

- Volle Kontrolle 
- Netzunabhängig, schneller 
- Ggf. bessere Sicherheit 


Nachteile: 

- Aufwändig 





Nutzung einer Web-Instanz
=========================


Bekannte Unzulänglichkeiten
***************************

- Derzeit können noch keine Bilder zu Fragen/Antworten hinzugefügt werden. Das ist in Arbeit. 

Bekannte Fehler
***************

- Wenn man beim Erstellen einer Frage ein Fach, eine Reihe, oder ein Schlagwort hinzufügt, dann kann der neue Eintrag nicht direkt ausgewählt werden. Man kann die Seite neu laden, aber dann sind ggf. schon getätigte Eingaben verloren. Abhilfe: VOR dem Eintippen der Frage die entsprechenden Einträge überlegen. Das sollte für Fach und Reihe kein Problem sein (davon gibt es ja nicht sooo viele), aber für Schlagwörter schon. Hier ist Vorsicht geboten. 
  - (Für den technisch Interessierten: das liegt an dem Javascript-Modul, das das Eingabefelf mit der Suchfunktion versieht. Das ist leider schlecht mit dem Django-Admin-Werkzeug zur Dateneingabe intergriert. Ggf. wird hier eine separate Eingabefunktion entstehen.) 





