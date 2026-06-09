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

# Ziel

Dieser Text zeigt den grundsätzlichen Aufbau eines BlePrompters am Beispiel des versteckten Einbaus in eine profane Streichholzschachtel.

* Einkaufsliste
* Beten und Löten
* Einbau und Handling der Streichholzschachtel
* Flashen der Firmware
* Kurzer Test mit der Smartphone-App
* Bezugsquellen

Der gezeigte Aufbau ist die einfachste Variante des BlePrompters. Es wird bewusst auf einen Schalter und andere fancy Mechanismen verzichtet, um den grundsätzlichen Aufbau so einfach wie möglich zu halten.

Hinweis: Im Folgenden spreche ich immer von dem "Board". Gemeint ist damit die kleine Platine mit dem Minidisplay. Dieses Teil:

![](../../assets/blog/images/articles/bleprompter-einbau-komplette-anleitung/001_DasBoard.png)

> Dieser Aufbau benötigt definitiv nur zwei Lötstellen, die auch von einem ungeübten Bastler zu bewerkstelligen sind. Naja, sofern man weiß, an welcher Seite der Lötkolben heiß wird.

# Einkaufsliste

Beginnen wir mit dem Einkauf der Teile.

## Das Board

Bezugsquellen siehe am Ende dieses Textes.

Suche im Internet nach:

* Aliexpress: *ESP32 0,42 Zoll Entwicklungsboard*
* Amazon.de: *ESP32 OLED 0,42*

Meist kommt das Board dann so verpackt an:

![](../../assets/blog/images/articles/bleprompter-einbau-komplette-anleitung/002_DasBoard.jpg)

Die beiliegenden Stiftleisten brauchen wir für diesen Bau nicht.

## Der Akku (LiPo)

Für diesen Build nutzen wir einen handelsüblichen LiPo-Akku, wie er in Millionen von Kleingeräten bis hin zu E-Zigaretten verwendet wird. Eine häufige Bezeichnung ist "LiPo 1S". Das "1S" bedeutet: eine Zelle mit 3,7 Volt Nennspannung.

* Das teuerste Teil des Baus, wenn man es bei Amazon.de kauft
* Siehe Bezugsquellen unten

> Ja, man kann die Teile sogar aus alten E-Zigaretten ernten. Siehe dazu meinen Text über LiPos in E-Zigaretten. Kein Scherz. Ich habe auf diese Weise zum Basteln schon eine ganze Kiste voll gerettet. Zum Basteln und für erste Experimente ist das eine super Quelle. Auch dazu findet Ihr etwas beim Thema Bezugsquellen.

In der Regel kommen die dann so:

![](../../assets/blog/images/articles/bleprompter-einbau-komplette-anleitung/003_DerLipo.jpg)

Normalerweise sind sie komplett verkabelt, mit einem kleinen Stecker, wie er z. B. auch im Modellbau für kleine Objekte üblich ist. Diese Stecker nennen sich "Micro-JST-1,25-Stecker".

> Und jetzt ein GANZ WICHTIGER HINWEIS! Die Polung ist nicht genormt. Je nach Quelle sind die Stecker unterschiedlich belegt. Hier gleich ein Merksatz:
>
> **"Links ist Rot"**
>
> In meinen Projekten gilt: Wenn man von oben auf den Stecker schaut, also dort, wo die "Buckel" sind, muss das rote Kabel auf der linken Seite hineingehen.

So muss das aussehen:

![](../../assets/blog/images/articles/bleprompter-einbau-komplette-anleitung/004_Links_ist_Rot.jpg)

Habt Ihr einen LiPo, bei dem das umgekehrt ist: kein Problem. Nehmt eine Stecknadel und hebt die Plastiknibbel etwas hoch. Dann kann man die Buchsen vorsichtig nach hinten herausziehen. Bitte ohne Kraft! Danach drückt man die *Nibbel* wieder etwas in das Plastikgehäuse und schiebt die Buchsen, rot links!!!, wieder hinein. Das ist etwas fummelig, aber keine Raketentechnik.

Wichtig beim Einschieben: Die kleine Nase an der Buchse muss nach oben. Sie dient dazu, dass die *Nibbel* die Buchse festhalten.

> Keine Ahnung, wie die *Nibbel* technisch richtig heißen. Aber Nibbel passt ganz gut, denke ich. Ihr wisst, was ich meine ...

## 1,25 mm JST 2 Pin Mikro "Männlicher" Steckverbinder

Ja, der mit dem Stift, also das Gegenstück zum Akku. Die Dinger kosten nur ein paar Cent, aber einzeln bekommt man sie normalerweise nicht. Meist sind 10 oder 20 Stück in einem Paket.

Mal sehen, ob wir einen Weg finden, ein paar davon in kleinen Stückzahlen weiterzugeben. Ansonsten müsst Ihr Euch halt ein Päckchen kaufen. Auch diese Dinger gibt es bei Amazon oder bei Ali.

Sieht so aus:

![](../../assets/blog/images/articles/bleprompter-einbau-komplette-anleitung/005_maenlicher_verbinder.jpg)

> Das ist das Teil, das dann an das Board gelötet werden muss ...

## Die Streichholzschachtel :-)

Naja, die brauchen wir auch für unseren Bau.

> Bezugsquelle: Üblicherweise in dieser magischen Küchenschublade ganz unten, wo nach ein paar Jahren eh keiner mehr weiß, was da alles an Schätzen drin ist.

![](../../assets/blog/images/articles/bleprompter-einbau-komplette-anleitung/006_TheBox.jpg)

## Dinge, die man normalerweise schon hat

* USB-Kabel mit USB-C-Stecker
  Zum Verbinden des Boards mit dem Desktop

# Beten und Löten

> So, jetzt wird es ernst ...

# Board testen: Funktioniert es?

Aber vorher: Wenn Ihr das Board neu gekauft habt, schließt es einmal per USB-Kabel an Euren Desktoprechner an. Wir wollen doch sicher sein, dass es auch funktioniert. Ich hatte bisher bei 15 Boards keinen Ausfall, aber es gibt durchaus Berichte im Netz, dass so ein Board auch mal nicht will. Bevor wir also den Aufwand treiben und alles verbasteln, sollten wir sicher sein, dass es technisch funktioniert. Sonst suchen wir später den Fehler bei uns, obwohl vielleicht einfach das Board nicht in Ordnung ist.

Also: auspacken und anstecken. Für einen reinen Funktionstest tut es auch ein USB-Ladegerät.

> Ach ja: Legt es bitte auf eine nicht elektrisch leitende Oberfläche. Das Teil ist mit Eurem Rechner verbunden und wir wollen doch keinen Kurzschluss an der USB-Schnittstelle produzieren. Wie Ihr an den Fotos seht, lege ich das Board zum Fotografieren immer auf ein simples Mikrofasertuch :-)

Wenn alles geklappt hat, sieht das dann so aus:

![](../../assets/blog/images/articles/bleprompter-einbau-komplette-anleitung/007_feuer_frei.jpg)

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

![](../../assets/blog/images/articles/bleprompter-einbau-komplette-anleitung/008_Geraetemanager.png)

Dann seht Ihr diese Ansicht.

In der Sektion "Anschlüsse (COM&LPT)" solltet Ihr ...

![009\_Ansicht\_GM](../../assets/blog/images/articles/bleprompter-einbau-komplette-anleitung/009_Ansicht_GM.png)

... in etwa so einen Eintrag sehen. Je nach Anwendung stehen dort aber auch mehrere Einträge. Welches ist nun unser wunderbares Board?

Zieht einfach den USB-Stecker ab. Der Eintrag, der dann verschwindet, das ist das Board. Steckt das USB-Kabel wieder ein und, juhu, unser Board ist wieder sichtbar.

Merkt Euch den Namen, der hinten steht. Also in diesem Fall *COM9*. Windows vergibt diese Nummern selbst.

![010\_GM\_Detail](../../assets/blog/images/articles/bleprompter-einbau-komplette-anleitung/010_GM_Detail.png)

Ihr findet keinen Eintrag "Anschlüsse (COM & LPT)" oder es tut sich überhaupt nichts? Dann habt Ihr keine Verbindung mit dem Board. Das bedeutet: Wir können später keine Firmware aufspielen.

Fehlersuche:

* Anderes USB-Kabel testen. Billige USB-C-Kabel sind oft nur Ladekabel ohne Datenleitung. Das ist eines der häufigsten Probleme.
* Stecker sitzt nicht richtig.
* USB-Port ist ggf. defekt.
* Oder schlichtweg: Das Board funktioniert nicht.
* Sonderfall: Es ist bereits eine Firmware aufgespielt, z. B. BlePrompter, die das Board schlafen legt. Dazu gibt es weiter unten beim Thema Flashen noch ein paar Hinweise.

> Keine Panik: Bis auf Fall 1 und 2 hatte ich da noch nie ein Problem. Naja, und klar, der Sonderfall kann vorkommen, aber der ist unkritisch. Man muss nur kurz die Taster bedienen. Bekommt Ihr hin ...

# Bezugsquellen:

TBD:

* LiPo-Hinweis auf E-Zigaretten
* LiPo-Quellen -> z. B. Pollin, Ali etc.

Kabel:

https://www.amazon.de/dp/B0CTLHF8B5?ref=ppx_yo2ov_dt_b_fed_asin_title&th=1

# 20 Paare 1,25 mm JST 2 Pin Mikro Elektronik Männlichen und Weiblichen Steckverbinder Stecker mit 10 cm Draht Kabel
