---
layout: blog_artikel
title: "BlePrompter-Einbau komplette Anleitung"
date: 2026-06-09 10:34
updated: 2026-06-09 10:34
type: "Anleitung"
topics:
  - AppGehoert
  - BLE-Prompter
  - Requisitenbau
  - ESP32
summary: "Eine komplette Fotodokumentation bis hin zum Flashen eines BlePrompters. Der Beispieleinbau erfolgt in eine Streichholzschachtel."
hero:
status: "fertig"
difficulty:
---

[PDF-Version dieses Textes](./../assets/blog/images/articles/bleprompter-einbau-komplette-anleitung/bleprompter-einbau-komplette-anleitung.pdf)

Version 1

# Der Anfang

Dieser Text zeigt den grundsätzlichen Aufbau eines BlePrompters am Beispiel des versteckten Einbaus in eine profane Streichholzschachtel.

* Einkaufsliste
* Beten und Löten
* Einbau und Handling der Streichholzschachtel
* Flashen der Firmware
* Kurzer Test mit der Smartphone-App
* Bezugsquellen

Der gezeigte Aufbau ist die einfachste Variante des BlePrompters. Es wird bewusst auf einen Schalter und andere fancy Mechanismen verzichtet, um den grundsätzlichen Aufbau so einfach wie möglich zu halten.

Hinweis: Im Folgenden spreche ich immer von dem "Board". Gemeint ist damit die kleine Platine mit dem Minidisplay. Dieses Teil:

![](./../assets/blog/images/articles/bleprompter-einbau-komplette-anleitung/001_DasBoard.png)

> Dieser Aufbau benötigt definitiv nur zwei Lötstellen, die auch von einem ungeübten Bastler zu bewerkstelligen sind. Naja, sofern man weiß, an welcher Seite der Lötkolben heiß wird.

**Und wie immer bei solchen Texten: Bitte einmal bis zum Ende durchlesen und dann erst mit dem Basteln anfangen! Schont die Nerven!**

# Einkaufsliste

Beginnen wir mit dem Einkauf der Teile.

## Das Board

Bezugsquellen siehe am Ende dieses Textes.

Suche im Internet nach:

* Aliexpress: *ESP32 0,42 Zoll Entwicklungsboard*
* Amazon.de: *ESP32 OLED 0,42*

Meist kommt das Board dann so verpackt an:

![](./../assets/blog/images/articles/bleprompter-einbau-komplette-anleitung/002_DasBoard.jpg)

Die beiliegenden Stiftleisten brauchen wir für diesen Bau nicht.

## Der Akku (LiPo)

Für diesen Build nutzen wir einen handelsüblichen LiPo-Akku, wie er in Millionen von Kleingeräten bis hin zu E-Zigaretten verwendet wird. Eine häufige Bezeichnung ist "LiPo 1S". Das "1S" bedeutet: eine Zelle mit 3,7 Volt Nennspannung.

* Das teuerste Teil des Baus, wenn man es bei Amazon.de kauft
* Siehe Bezugsquellen unten

> Ja, man kann die Teile sogar aus alten E-Zigaretten ernten. Siehe dazu meinen Text über LiPos in E-Zigaretten. Kein Scherz. Ich habe auf diese Weise zum Basteln schon eine ganze Kiste voll gerettet. Zum Basteln und für erste Experimente ist das eine super Quelle. Auch dazu findet Ihr etwas beim Thema Bezugsquellen.

In der Regel kommen die dann so:

![](./../assets/blog/images/articles/bleprompter-einbau-komplette-anleitung/003_DerLipo.jpg)

Normalerweise sind sie komplett verkabelt, mit einem kleinen Stecker, wie er z. B. auch im Modellbau für kleine Objekte üblich ist. Diese Stecker nennen sich "Micro-JST-1,25-Stecker".

> Und jetzt ein GANZ WICHTIGER HINWEIS! Die Polung ist nicht genormt. Je nach Quelle sind die Stecker unterschiedlich belegt. Hier gleich ein Merksatz:
>
> **"Links ist Rot"**
>
> In meinen Projekten gilt: Wenn man von oben auf den Stecker schaut, also dort, wo die "Buckel" sind, muss das rote Kabel auf der linken Seite hineingehen.

So muss das aussehen:

![](./../assets/blog/images/articles/bleprompter-einbau-komplette-anleitung/004_Links_ist_Rot.jpg)

Habt Ihr einen LiPo, bei dem das umgekehrt ist: kein Problem. Nehmt eine Stecknadel und hebt die Plastiknibbel etwas hoch. Dann kann man die Buchsen vorsichtig nach hinten herausziehen. Bitte ohne Kraft! Danach drückt man die *Nibbel* wieder etwas in das Plastikgehäuse und schiebt die Buchsen, rot links!!!, wieder hinein. Das ist etwas fummelig, aber keine Raketentechnik.

Wichtig beim Einschieben: Die kleine Nase an der Buchse muss nach oben. Sie dient dazu, dass die *Nibbel* die Buchse festhalten.

> Keine Ahnung, wie die *Nibbel* technisch richtig heißen. Aber Nibbel passt ganz gut, denke ich. Ihr wisst, was ich meine ...

## 1,25 mm JST 2 Pin Mikro "Männlicher" Steckverbinder

Ja, der mit dem Stift, also das Gegenstück zum Akku. Die Dinger kosten nur ein paar Cent, aber einzeln bekommt man sie normalerweise nicht. Meist sind 10 oder 20 Stück in einem Paket.

Mal sehen, ob wir einen Weg finden, ein paar davon in kleinen Stückzahlen weiterzugeben. Ansonsten müsst Ihr Euch halt ein Päckchen kaufen. Auch diese Dinger gibt es bei Amazon oder bei Ali.

Sieht so aus:

![](./../assets/blog/images/articles/bleprompter-einbau-komplette-anleitung/005_maenlicher_verbinder.jpg)

> Das ist das Teil, das dann an das Board gelötet werden muss ...

## Die Streichholzschachtel :-)

Naja, die brauchen wir auch für unseren Bau.

> Bezugsquelle: Üblicherweise in dieser magischen Küchenschublade ganz unten, wo nach ein paar Jahren eh keiner mehr weiß, was da alles an Schätzen drin ist.

![](./../assets/blog/images/articles/bleprompter-einbau-komplette-anleitung/006_TheBox.jpg)

## Dinge, die man normalerweise schon hat

* USB-Kabel mit USB-C-Stecker  
  Zum Verbinden des Boards mit dem Desktop

# Beten und Löten

> So, jetzt wird es ernst ...

## Board testen: Funktioniert es?

Aber vorher: Wenn Ihr das Board neu gekauft habt, schließt es einmal per USB-Kabel an Euren Desktoprechner an. Wir wollen doch sicher sein, dass es auch funktioniert. Ich hatte bisher bei 15 Boards keinen Ausfall, aber es gibt durchaus Berichte im Netz, dass so ein Board auch mal nicht will. Bevor wir also den Aufwand treiben und alles verbasteln, sollten wir sicher sein, dass es technisch funktioniert. Sonst suchen wir später den Fehler bei uns, obwohl vielleicht einfach das Board nicht in Ordnung ist.

Also: auspacken und anstecken. Für einen reinen Funktionstest tut es auch ein USB-Ladegerät.

> Ach ja: Legt es bitte auf eine nicht elektrisch leitende Oberfläche. Das Teil ist mit Eurem Rechner verbunden und wir wollen doch keinen Kurzschluss an der USB-Schnittstelle produzieren. Wie Ihr an den Fotos seht, lege ich das Board zum Fotografieren immer auf ein simples Mikrofasertuch :-)

Wenn alles geklappt hat, sieht das dann so aus:

![](./../assets/blog/images/articles/bleprompter-einbau-komplette-anleitung/007_feuer_frei.jpg)

Die Anzeige im Display kann je nach Quelle etwas anders aussehen. Das ist egal. Hauptsache, das Display zeigt etwas an.

Funktionsprüfung:

* Display zeigt etwas an
* Rote LED ist an
* Blaue LED: Ja, meist geht sie an. Sie zeigt an, dass das Teil im Auslieferungszustand gerade ein eigenes WLAN aufspannt. Je nach Firmware kann es aber auch sein, dass sie nicht leuchtet. Keine Panik.
* Taster oben links: Das ist der Resetknopf. Einfach mal drücken. Dann sollte das Display kurz flackern und das Board wird neu gestartet.
* Taste oben rechts: Da gibt es zu diesem Zeitpunkt gerade nichts, was man sinnvoll testen kann :-) Ihr dürft aber ruhig mal draufdrücken ...

### Erweiterter Test

Da ich keinen Apple-Mac besitze, kann ich Euch hier nur für Windows noch einen weiteren Test anbieten. Wenn jemand einen Mac hat: gerne eine Nachricht und ein paar Screenshots an mich. Dann baue ich das hier gerne in den Text ein.

Also zurück zu Windows:

Es gibt in Windows ein Systemprogramm namens Gerätemanager. Das startet Ihr:

![](./../assets/blog/images/articles/bleprompter-einbau-komplette-anleitung/008_Geraetemanager.png)

Dann seht Ihr diese Ansicht.

In der Sektion "Anschlüsse (COM & LPT)" solltet Ihr ...

![009\_Ansicht\_GM](./../assets/blog/images/articles/bleprompter-einbau-komplette-anleitung/009_Ansicht_GM.png)

... in etwa so einen Eintrag sehen. Je nach Anwendung stehen dort aber auch mehrere Einträge. Welches ist nun unser wunderbares Board?

Zieht einfach den USB-Stecker ab. Der Eintrag, der dann verschwindet, das ist das Board. Steckt das USB-Kabel wieder ein und, juhu, unser Board ist wieder sichtbar.

Merkt Euch den Namen, der hinten steht. Also in diesem Fall *COM9*. Windows vergibt diese Nummern selbst.

![010\_GM\_Detail](./../assets/blog/images/articles/bleprompter-einbau-komplette-anleitung/010_GM_Detail.png)

Ihr findet keinen Eintrag "Anschlüsse (COM & LPT)" oder es tut sich überhaupt nichts? Dann habt Ihr keine Verbindung mit dem Board. Das bedeutet: Wir können später keine Firmware aufspielen.

Fehlersuche:

* Anderes USB-Kabel testen. Billige USB-C-Kabel sind oft nur Ladekabel ohne Datenleitung. Das ist eines der häufigsten Probleme.
* Stecker sitzt nicht richtig.
* USB-Port ist ggf. defekt.
* Oder schlichtweg: Das Board funktioniert nicht.
* Sonderfall: Es ist bereits eine Firmware aufgespielt, z. B. BlePrompter, die das Board schlafen legt. Dazu gibt es weiter unten beim Thema Flashen noch ein paar Hinweise.

> Keine Panik: Bis auf Fall 1 und 2 hatte ich da noch nie ein Problem. Naja, und klar, der Sonderfall kann vorkommen, aber der ist unkritisch. Man muss nur kurz die Taster bedienen. Bekommt Ihr hin ...

## Vorbereitung

Nun interessiert uns an unserem Board die Stelle, an der der Strom hineinkommt.

![](./../assets/blog/images/articles/bleprompter-einbau-komplette-anleitung/011_Loetaugen.jpg)

Wir finden:

* 5V - Da lassen wir beim Löten unsere Finger davon. Das sind die 5V, die per USB an das Board geliefert werden. Würden wir da den Akku anschließen: na, keine gute Idee.
* GD - Ja, das ist "Minus", "Ground". Hier löten wir unser schwarzes Kabel an.
* 3V - und klar: 3 Volt. Auf manchen Boards auch BAT. Hier kommt unser Akku dran. Stört Euch nicht an 3V. Der Akku liefert über seine Betriebszeit, bis er leer ist, alles von 4,2 Volt bis zum Betriebsende bei 2,8 Volt. Passt schon.

Je nach Einbau sollten wir jetzt bei unserem "Männchen" die Kabel etwas verkürzen. In unserem Fall liegt der Akku in der Streichholzschachtel ja direkt daneben, da reichen ein paar Zentimeter.

Hier ein Beispiel, wie ich das verschalte, sodass es einfach in die Streichholzschachtel passt.

... kurz weg zum Löten ...

So, das Erste ist geschafft. Ist Euer Akku geladen? Na dann los, das Board springt wieder an. Steckt den Akku mal an.

> Erfolg? Gratulation. Raucht es? Ja, auch das Board-Innere besteht nur aus magischem blauem Rauch. Spaß ... selbst wenn Ihr das verkehrt herum angeschlossen habt, passiert nichts. Im Board ist eine Schutzdiode gegen dusselige Finger ...

**ACHTUNG!!! Wird der Akku heiß, sofort abziehen. Dann habt Ihr ggf. beim Löten nicht aufgepasst und zwischen GD und 3V einen Kurzschluss produziert. Bitte sofort abziehen. Je nach Größe des Akkus kann der in diesem Fall die Kabel durchschmelzen oder sogar zu brennen anfangen.**

## Gelötet

So, Kabel angelötet und gleich mal an den Akku gesteckt. Das Board springt wieder an. Das solltet Ihr auch machen, wenn Ihr das Board und das Kabel verheiratet habt.

![](./../assets/blog/images/articles/bleprompter-einbau-komplette-anleitung/012_Geloetet.jpg)

Hier noch mal ein Blick auf die Rückseite. Man sieht es nicht besonders gut: Ich leite die Kabel in so einem Fall meist an den Lötaugen entlang, nutze einen Hartkleber und klebe die Kabel an die Platine. Es geht hier nicht um Schönheit. Wir bauen etwas, das auf der Bühne auch mal eine etwas rauere Behandlung ertragen kann. Manche Bastler fixieren das mit Heißkleber. Geht auch. Hauptsache, die Lötstelle wird mechanisch entlastet. Die Lötaugen können mit dem Lötzinn zusammen abreißen. Das brauchen wir nicht. Bitte aber keinen Klebstoff auf die Bauteile. Die werden warm und wollen ihre Wärme an die Luft abgeben. Das sollten wir ihnen nicht mit einer Schicht aus Klebstoff verwehren, auch wenn wir das Board später noch mit etwas Klebeband vor Kurzschlüssen sichern.

![013_Geloetet](./../assets/blog/images/articles/bleprompter-einbau-komplette-anleitung/013_Geloetet.jpg)

## Stellprobe

Nun denn, passt noch alles in die Streichholzbox? Ja. Die LiPo-Kabel, die ich jetzt nicht kürzen wollte, habe ich unter dem Board aufgewickelt. Das hat einen netten Nebeneffekt: Sie wirken wie eine Feder und drücken somit das Board nach oben, dort, wo jetzt der Ausschnitt für das Sichtfenster schon grob angezeichnet ist.

![014_rin_de_mit](./../assets/blog/images/articles/bleprompter-einbau-komplette-anleitung/014_rin_de_mit.jpg)

Schnell mal ein Fenster reingeschnitten und ...

![](./../assets/blog/images/articles/bleprompter-einbau-komplette-anleitung/015_nun_isses_drin.jpg)

Fertig ist die Laube.

> Klein? Nein, darum ging es mir hier bei dem Bau auch nicht unbedingt. Weiter unten findet Ihr "kleine Varianten". Hier ging es mir erstmal darum, das Prinzip und die Verschaltung aufzuzeigen.
>
> Gelungen? Für so ein 10-Minuten-Projekt allemal. Die meiste Zeit hat es gekostet, die Bilder zu machen.

## Kein Schalter?

Hardware ist so weit durch. Ausschalten?

In diesem Fall: LiPo abziehen und gut ist. Ja, es gibt noch andere Wege, das zu lösen:

* Mikroschalter ins Kabel basteln. Dumm, habe ich gerade keinen im Haus.
* Steckbrücken. Dazu wird es noch einen gesonderten Blog geben.
* Reed-Kontakte. Das sind kleine Kontakte, die mit Magneten geschaltet werden. Da erwarte ich die Tage ein Paket. Sollte schon da sein, naja, hängt vermutlich irgendwo auf einem Frachter. War eine größere Bestellung. Oder wieder beim Zoll. Auch das werde ich noch mal in einem getrennten Blog zeigen. Dabei ist die Idee: "Solange der Magnet am Gerät ist, ist es aus" bzw. für eine andere Anwendung: "Der Magnet schaltet ein".
* Andere Ideen ... mal sehen. Hier jetzt erstmal die einfachste Variante: LiPo abziehen.

Gehen dann die Stecker nicht schnell kaputt?

Sagen wir es mal so: Ich nutze seit Jahren genau solche Stecker an einer kleinen Drohne mit mehreren Akkus. Bisher ist mir noch keiner kaputtgegangen.

> Angst, dass etwas bei einem Auftritt passiert?
> Hey, die Dinger sind so billig zu bauen ... baut zwei ...

# Software marsch

So, bisher haben wir uns nur um das "*Blech*" gekümmert. Jetzt muss die Firmware auf das Board.

Dazu wenden wir uns an diese Webseite:

https://hesspet.github.io/Zauberhaft/

![](./../assets/blog/images/articles/bleprompter-einbau-komplette-anleitung/020_Web1.png)

Wenn Ihr diesen Text nicht gerade irgendwoher bekommen habt, dann seid Ihr genau auf unserer kleinen Webpräsenz.

Wir gehen auf die Seite "**DOWNLOADS**".

Dort finden wir das Kapitel "**ESP32 Firmware**".

![](./../assets/blog/images/articles/bleprompter-einbau-komplette-anleitung/021_Web2.png)

Wir gehen zur Übersicht ...

Und dort finden wir die aktuelle Version des BlePrompter, also der Software, die Kommandos via "Bluetooth Low Energy" empfangen kann.

![](./../assets/blog/images/articles/bleprompter-einbau-komplette-anleitung/022_Web3.png)

> Was jetzt kommt, geht nur auf dem Desktoprechner, an dem Ihr das Board angeschlossen habt.

Ihr seht den Button "**Installieren**"? Genau den. Funktionieren tut das aber nur in einem Chrome-Browser oder einem Firefox-Browser bzw. in Derivaten davon, wie z. B. Edge, Vivaldi und den vielen anderen.

Wenn Ihr auf "**Installieren**" klickt, öffnet sich ein Modul, das ich nicht geschrieben habe. Leider ist es auf Englisch und kann nicht ohne riesigen Aufwand mit deutschen Texten versehen werden. Also unverzagt: "Klick den Button".

Es erscheint:

![](./../assets/blog/images/articles/bleprompter-einbau-komplette-anleitung/030_ESPFlasher1.png)

Aua, yo, vielleicht sollten wir unser Board auch wieder per USB an unseren Desktoprechner hängen.

**WICHTIG!!! Bitte immer, wenn man das Board an den Rechner hängt: Der LiPo hat da nix zu suchen.**

Die Theorie sagt zwar laut Schaltplan: "Kann nix passieren ..." Aber ich will nicht daran schuld sein, wenn Ihr Euren Rechner beschädigt.

Also: "**LiPo abmachen und dann erst USB anstecken!**"

Nach kurzer Zeit erscheint dann dieser Text:

![](./../assets/blog/images/articles/bleprompter-einbau-komplette-anleitung/031_ESP Fehler1.png)

Also los, steckt das Board wieder an Euren Rechner und klickt "**Try Again**".

![](./../assets/blog/images/articles/bleprompter-einbau-komplette-anleitung/032_ESP.png)

Na, das sieht schon besser aus. Ihr erinnert Euch, die COM? Genau, die taucht hier wieder auf. Die Meldung sollte so in der Art aussehen. Ihr wählt jetzt einfach Euer Board aus und klickt dann "**Verbinden**".

Es kommt kurz eine Anzeige "**Connecting**" ...

Und dann werdet Ihr das letzte Mal gefragt, ob Ihr die Firmware auf das Board schreiben wollt.

![](./../assets/blog/images/articles/bleprompter-einbau-komplette-anleitung/033_ESP.png)

> Wollt Ihr? Bestimmt, wenn Ihr bis hier durchgehalten habt ...
>
> Dann los.

Klickt auf "**Install BlePrompter** ..." und die Magie des Flashens beginnt ...

> Nee, nochmal fragen ... was denken sich manche Programmierer? Anwender sind doof?

![](./../assets/blog/images/articles/bleprompter-einbau-komplette-anleitung/034_ESP.png)

Also ... jetzt noch mal "**Klicke Install**" ...

... und los geht es. Bitte anschnallen, Ihr Pilot übernimmt alles ...

![](./../assets/blog/images/articles/bleprompter-einbau-komplette-anleitung/035_ESP.png)

![036_ESO](./../assets/blog/images/articles/bleprompter-einbau-komplette-anleitung/036_ESO.png)

![037_ESP](./../assets/blog/images/articles/bleprompter-einbau-komplette-anleitung/037_ESP.png)

Wir setzen zur Landung an.

![038_ESP](./../assets/blog/images/articles/bleprompter-einbau-komplette-anleitung/038_ESP.png)

Und so in der Art sollte Euch jetzt direkt **kurz** nach dem Flashen das Display begrüßen ...

![](./../assets/blog/images/articles/bleprompter-einbau-komplette-anleitung/040_hurra.jpg)

Holt Euch eine Lupe - da steht sowas wie:

``````
BlePrompter
1.8.1
Noch 6s
BP-6314
``````

> Gratulation, das Board ist mit der Firmware geflasht!

# Kurzer Test mit der Smartphone-App

## Erstmal noch technische Erläuterungen

> Ist notwendig, um das Verhalten der Firmware zu verstehen. Lest es bitte!

Das gesamte Projekt basiert auf Komponenten die man kaufen kann. Ein BlePrompter kann man für unter 20€ bauen.

Damit erkauft man sich aber auch ein paar Nachteile:

* Keine integriertes LiPo Management
  * insbesondere keine integrierte Ladeschaltung
  * kein On/Off Mechanismus "Out-Of-The Box"
* Einschränkungen in der Akkulaufzeit

Insbesondere die Einschränkungen in der Akkulaufzeit habe mir bei der Entwicklung einiges an Kopfzerbrechen bereitet.

Baut man BlePrompter mit sehr kleinen LiPos wie ich es weiter Unten noch zeigen werde, so haben solche Akkus eine Kapazität von 70mAh. Funkverkehr auch wenn es BLE ist braucht eine gewisse Menge. Im reinen Betrieb baucht das Board ca. 100 mAh. Das ergibt mit einer Akkuladung eine Betriebszeit von nicht ganz eine halben Stunde.

Das ist für eine normale Auftrittspraxis einfach nicht tauglich.

Glücklicherweise haben die Entwickler des Microcontrollers ESP32 einen Mechanismus erfunden, der sich DeepSleep nennt. Setzt man also den Prozessor in den DeepSleep, so würde er mit einem solchen Akku rein rechnerisch gut und gerne 500 Stunden "leben". Nur in der zeit kann er keine BLE Kommunikation! Das hilft dann nicht weiter. Oder aber doch?

Was wäre, wenn sich das kleine Board einfach immer eine Zeit schlafen legt und nur innerhalb einer Minute immer mal aufwacht, die Smartphoneapp diesen Vorgang überwacht und nur wenn es notwendig wird das Board in einen dauernden Wachzustand überführt.

Bei einem Auftritt weiß man schon lange vorher wann das Board gebraucht wird. Der Helfer, der das Smartphone bedient kann rechtzeitig eine Verbindung aufbauen und nach dem Ablauf der Routine und dem Reval schalten wir das kleine Gerät wieder in den Schlafzustand.

Testläufe haben ergeben, dass man so mit dem kleinen Akku sicher auf 3-4 Stunden Betrieb kommt. 

Das dürfte in der Praxis reichen. Der Akku in der Streichholzschachtelt schafft ohne Probleme im Test 24 Stunden.

Wenn man vor dem Auftritt beim Funktionstest die Verbindung 1x aufgebaut hat, so wird der Verbindungsaufbau mit einem Tastendruck durchgeführt.

## Die Smartphone App

https://hesspet.github.io/Nasreddins-Simple-Peek-Client2Web/ direkt gestartet werden.

Da es sich um eine Webanwendung handelt kann der Anwender sie mit den Browserfunktionen auf seinen Startbildschirm installieren und braucht so beim Betrieb keine Internetverbindung mehr.

**Generell: Bluetooth muss auf dem Smartphone aktiviert sein**

### Unter Android

Zum Aufrufen einen Chrome basierten Browser nutzen. 

* Chrome
* Kivi
* Vivaldi
* und viele mehr stellen die WebBluetooth Schnittstelle der Anwendung zur Verfügung

### Unter iOS (Der Bluefy Web)

Hier ist es etwas problematischer. Appel weigert sich die WebBluetooth Standard in den normalen Safari Browser einzubauen. Somit ist mit dem Safari Browser es nicht möglich eine Kommunikation via Bluetooth in einer Webapp zu etablieren.

Es gibt aber Abhilfe...

https://apps.apple.com/de/app/bluefy-web-ble-browser/id1492822055

**Bluefy** ist ein Browser der kostenfrei aus dem App Store heruntergeladen werden kann. 

Bluefy gibt es schon ein paar Jahre, ist also keine "esotherische" Software. Viele große Hersteller lassen sich von der Softwareschmiede "PNN Soft" für ihre technische Steuerungen spezielle Browser für iOS bauen. 

Hier ist also mein Weg ohne großen Kostenaufwand für iOS eine Bluetooth Webapplikation bereit zu stellen.

---

TBD -> Video - Bildschirm Teilen mit 

---

Dieser Text wird noch fortgesetzt, aber vorerst versuche ich die Funktion in diesem Video zu erläutern.



































Bezugsquellen:

TBD:

* LiPo-Hinweis auf E-Zigaretten
* LiPo-Quellen -> z. B. Pollin, Ali etc.

Kabel:

https://www.amazon.de/dp/B0CTLHF8B5?ref=ppx_yo2ov_dt_b_fed_asin_title&th=1

# 20 Paare 1,25 mm JST 2 Pin Mikro Elektronik männliche und weibliche Steckverbinder mit 10 cm Drahtkabel

# TBD

* TODO: markdig ertüchtigen, dass der Link in einem neuen Reiter geöffnet wird