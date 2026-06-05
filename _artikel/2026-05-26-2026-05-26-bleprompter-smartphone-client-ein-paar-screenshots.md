---
layout: diymagic_artikel
title: "2026-05-26 BlePrompter Smartphone Client - Ein paar Screenshots"
date: 2026-05-26
updated: 2026-05-26
type: "Bericht"
topics:
  - BLE-Prompter
  - Smartphone
  - Zauberapp
  - Software
  - Android
summary: "Eine erste Vorstellung der Bedienung des BlePrompter Smartphone Client"
hero:
status: "fertig"
difficulty:
---

# BlePrompter Smartphone Client - Ein paar Screenshots

Wie funktioniert das Ganze Thema mit der Ãœbertragung vom Smartphone auf den BlePrompter?

Hier mal ein kurzer Duchlauf des aktuellen Stands der Smartphone App.

## Android und iOS?

Jaaa... braucht aber noch Zeit mit dem iOS. Die Plattform die ich zum Entwickeln nutze kann Code fÃ¼r Android als auch fÃ¼r iOS erzeugen. Ein iPhone 12 bekomme ich die Tage. Dann brauche ich nur noch einen Entwickleraccount bei Apple. Das schiebe ich aber hinaus, denn erst wenn klar ist, dass ein paar Leute Interesse an der kleinen Hardware haben und bereit sind ein paar Euro fÃ¼r die App auszugeben werden ich die Entwickleraccounts kaufen.

GrundsÃ¤tzlich kann ich im Moment aber nur fÃ¼r iOS einen Testmode verwenden. Also hier ein paar Screenshots meines Android Phones.

## Screenshots

### Verbindungsaufbau und Setup

Die Anwendung selbst ist erst einmal recht unscheinbar. Im Kopfbereich sehen wir "Getrennt". Dies bedeutet, aktuell haben wir keine BLE Verbindung zum BlePrompter.

Der hier gezeigte Teil "Peeker (Videofake)" ist die Implementation einer Showsituation, dass der VorfÃ¼hrende mit einem Zuschauer eine Gedankenleseroutine ausfÃ¼hrt. Ein Helfer hat das Smartphone mit dieser Anwendung und verhÃ¤lt sich wie ein Ã¼blicher Zuschauer und filmt. Schaut jemand auf das Display, so sieht er einfach die typische Optik einer Smartphone Kamera. Das sehen wir dann spÃ¤ter. Daher der Name "Videofake".

Hintergrund ist, dass ich die App vor allem fÃ¼r meinen eigenen Zweck als Bauchredner in der Form eines Streetacts verwende. Zaubern und Bauchreden ist schwierig. Man hat nur eine Hand... also lasse ich mir helfen und habe einen Companion unter den Zuschauern...

<img src="/assets/diy-magic/images/articles/2026-05-26-bleprompter-smartphone-client-ein-paar-screenshots/001-Vor_de_Verbindungsaufbau.jpg" style="zoom: 33%;" />

Wir klicken auf Verbinden und sehen "Gefundene GerÃ¤te". Beim BLE Scan sucht die Anwendung gezielt nach GerÃ¤ten mit unserem speziellen Profil. Normalerweise findet die Anwendung nur ein GerÃ¤t das ausgewÃ¤hlt werden kann.

War das GerÃ¤t bereits beim letzten Anwendungsaufruf schon einmal verbunden, so wird beim App Start, die Verbindung automatisch aufgebaut. Das erspart in einer Livesituation Bedienungsfehler. Hier aber der Grundablauf. "Suche GerÃ¤t"

<img src="/assets/diy-magic/images/articles/2026-05-26-bleprompter-smartphone-client-ein-paar-screenshots/002_Scan_nach BlePrompter.jpg" alt="002_Scan_nach BlePrompter" style="zoom:33%;" />

Wir sehen nun "Verbunden" und bekommen das "HauptmenÃ¼"

* **Anzeige lÃ¶schen**
  LÃ¶schen der Anzeige des Displays im BlePrompter
* **Trennen**
  Abbau der Verbindung zum BlePrompter. Hier Ã¼berlege ich ob das Ã¼berhaupt auf die Hauptseite soll, denn warum sollte man auf die Idee kommen die Verbindung wÃ¤hrend einer Show zu Trennen. Das wandert ggf. noch in die Einstellungen
* **Anzeigen im BlePrompter**
  Dies ist die aktuelle Auswahl von Ideen was man dem Prompter schicken kann. Dies kann recht einfach in der Firmware erweitert werden. Aktuell gibt es vier Darstellungen
  * Pfeile
    Ãœbertragung von Kommandos von Pfeilrichtungen
  * Karten (KartenkÃ¼rzel)
    Ãœbertragung der Farbe und des Wertes einer Karte. Pokerdeck
  * Symbole
    Freier "Text" ein oder zwei Buchstaben per Texteingabe
  * ESP
    Ãœbertragung eines der fÃ¼nf ESP Symbole (aktuell mein Anwendungsfall)

<img src="/assets/diy-magic/images/articles/2026-05-26-bleprompter-smartphone-client-ein-paar-screenshots/003_Verbindung_hergestellt.jpg" alt="003_Verbindung_hergestellt" style="zoom:33%;" />

Ãœber das Drawer MenÃ¼ (Hamburger) oben rechts erreicht man die Einstellungen. Diese werden gespeichert mÃ¼ssen also nur einmal durchgefÃ¼hrt werden.

* **Dunkelmodus** - Je nach Bediener kann eine helle oder dunkle OberflÃ¤che eingestellt werden
* **SchlieÃŸe Buttonansicht nach Senden**
  Wenn das GeheimmenÃ¼ in der Videoanwendung gestartet wird, kann nach dem Senden einer Information an den BlePrompter das MenÃ¼ automatisch geschlossen werden, oder wenn nicht aktiviert geÃ¶ffnet bleiben.
* **Displayanzeige invertiert**
  * Off - BlePrompter: weiÃŸe Schrift auf schwarzem Hintergrund
  * On - BlePrompter: schwarze Schrift auf weiÃŸem Hintergrund
* **Displayanzeige drehen**
  * Off - BlePrompter: Ausrichtung der Anzeige in Boardhauptrichtung
  * On - BlePrompter: Ausrichtung der Anzeige um 180 Grad gedreht. "KopfÃ¼ber". Wird z.B. bei dem Einsatz in der Daumenspitze gebraucht
* **Kameraansicht**
  Anpassungen der Kameraansicht an das jeweilige Betriebssystem, damit die Kamera mÃ¶glichst realistisch aussieht.
* **Kamera-Bedienung**
  Anzeigevariationen des geheimen SendemenÃ¼s in der Fakevideoansicht
  * **Normal**
    Das MenÃ¼ wird komplett sichtbar eingeblendet
  * **Durchsichtig**
    Das MenÃ¼ wird nur mit den Rahmen dargestellt "Durchsichtig"
  * **UnauffÃ¤llig / Anpassbar**
    Experimentelle Optionen, bisher nur rudimentÃ¤r implementiert. Kann auch sein, dass die wieder ausgebaut werden. Der Nutzen ist zweifelhaft.

<img src="/assets/diy-magic/images/articles/2026-05-26-bleprompter-smartphone-client-ein-paar-screenshots/004_Programmeinstellungen.jpg" alt="004_Programmeinstellungen" style="zoom:33%;" />

Umschaltung auf Dunkelmodus erfolgt sofort

<img src="/assets/diy-magic/images/articles/2026-05-26-bleprompter-smartphone-client-ein-paar-screenshots/005_Dunkelmodus aktiviert.jpg" alt="005_Dunkelmodus aktiviert" style="zoom:33%;" />

Hier jetzt die Einstellung der Kamera auf "Android und Normalansicht"

<img src="/assets/diy-magic/images/articles/2026-05-26-bleprompter-smartphone-client-ein-paar-screenshots/006_Setup_durchgefuehrt.jpg" alt="006_Setup_durchgefuehrt" style="zoom:33%;" />

ZurÃ¼ck zur Hauptansicht. Jetzt geht es los. ESP Modus wird angeklickt

<img src="/assets/diy-magic/images/articles/2026-05-26-bleprompter-smartphone-client-ein-paar-screenshots/007_Es_geht_los_ESP.jpg" alt="007_Es_geht_los_ESP" style="zoom:33%;" />

Uns so wÃ¼rde nun ein Betrachter neben des Companion, der auf das Smartphone schaut die das Livevideobild sehen. Vollkommen unverfÃ¤nglich. Sieht einfach so aus wie jemand der die VorfÃ¼hrung filmt.

![008_LivePseudFilen](/assets/diy-magic/images/articles/2026-05-26-bleprompter-smartphone-client-ein-paar-screenshots/008_LivePseudFilen.jpg)

Kurzer Klick auf die Kopfzeile, das GeheimmenÃ¼ erscheint und der Companion kann dem VorfÃ¼hrenden auf den BlePrompter das "gepeekte" ESP Symbol Ã¼bermitteln.

![009_Das_geheimmenue_in_normalansicht](/assets/diy-magic/images/articles/2026-05-26-bleprompter-smartphone-client-ein-paar-screenshots/009_Das_geheimmenue_in_normalansicht.jpg)

Wir schalten auf die noch geheimere Ansicht im Setup um

<img src="/assets/diy-magic/images/articles/2026-05-26-bleprompter-smartphone-client-ein-paar-screenshots/010_Kamera_Bedienung_Showmodus.jpg" alt="010_Kamera_Bedienung_Showmodus" style="zoom:33%;" />

Der gleiche Ablauf wie vorher

![011_Nochmal_Filmen](/assets/diy-magic/images/articles/2026-05-26-bleprompter-smartphone-client-ein-paar-screenshots/011_Nochmal_Filmen.jpg)

Jetzt blendet sich das MenÃ¼ aber fast unsichtbar ein. Selbst ein misstrauischer Zuschauer dÃ¼rfte jetzt nicht mehr erkennen, dass hier "geschummelt" wird. 

![012_Unsichtbares_Menu](/assets/diy-magic/images/articles/2026-05-26-bleprompter-smartphone-client-ein-paar-screenshots/012_Unsichtbares_Menu.jpg)
