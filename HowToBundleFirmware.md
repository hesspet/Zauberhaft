# HowTo: Firmware bündeln und bereitstellen

Stand: 08.06.2026

Diese Anleitung beschreibt den Weg von einer fertigen Releaseversion im PlatformIO-Projekt `C:\dev\TheStampSizeDiyPeekDevice\BlePrompter` bis zu einem Firmwarepaket in diesem Website-Projekt. Ziel ist eine Datei, die ein Anwender über die Zauberhaft-Website per Browser auf sein ESP-Gerät flashen kann.

Der wichtige Gedanke ist: PlatformIO baut nicht nur eine einzelne Anwendung. Für ESP32-Geräte besteht ein vollständiger Flash-Vorgang aus mehreren Binärdateien an festen Flash-Adressen. Für ESP Web Tools ist es am einfachsten und robustesten, diese Dateien vorher zu einer einzigen `firmware.bin` zusammenzuführen und diese Datei dann im Zauberhaft-Projekt bereitzustellen.

## Beteiligte Projekte

### Firmware-Projekt

Pfad:

```powershell
C:\dev\TheStampSizeDiyPeekDevice\BlePrompter
```

Dieses Projekt enthält die eigentliche Firmware. Es ist ein PlatformIO-Projekt mit Arduino Framework und zwei Build-Umgebungen:

| Umgebung | Gerät | Chipfamilie | Ergebnis |
| --- | --- | --- | --- |
| `esp32c3` | ESP32-C3 OLED | `ESP32-C3` | Firmware für das kleine OLED-Board |
| `cyd` | CYB/CYD Board | `ESP32` | Firmware für das ESP32-WROOM-32-Board mit ILI9341-TFT |

Die Umgebungen stehen in `platformio.ini`. PlatformIO verwendet diese Datei, um Board, Framework, Bibliotheken, Build-Flags und Upload-Einstellungen festzulegen.

### Website-Projekt

Pfad:

```powershell
C:\dev\Zauberhaft
```

Dieses Projekt hostet die fertige Firmware über GitHub Pages. Die Anwenderseite liegt unter:

```text
/downloads/firmware/
```

Die Website nutzt ESP Web Tools. Dadurch kann ein Anwender im Browser auf `Installieren` klicken, den seriellen Port auswählen und die Firmware ohne lokal installiertes PlatformIO oder Arduino IDE flashen.

## Grundbegriffe

### PlatformIO

PlatformIO ist hier das Build-System. Es liest `platformio.ini`, lädt passende Toolchains und Bibliotheken und erzeugt aus `src/`, `include/` und den eingebundenen Bibliotheken die Firmware-Artefakte.

Der wichtigste Befehl ist:

```powershell
pio run -e esp32c3
```

`-e esp32c3` bedeutet: Baue die Umgebung `[env:esp32c3]` aus `platformio.ini`.

### Arduino Framework

Das Arduino Framework stellt die Arduino-typischen APIs für ESP32 bereit, zum Beispiel `setup()`, `loop()`, serielle Ausgabe, GPIO, I2C, SPI und BLE-nahe Bibliotheksintegration. Der Code wird trotzdem für den konkreten ESP32-Chip kompiliert.

Im Projekt steht das in `platformio.ini` so:

```ini
framework = arduino
```

### Firmware-Artefakte

Nach einem erfolgreichen Build liegen die wichtigsten Dateien unter:

```text
.pio/build/<umgebung>/
```

Für `esp32c3` also:

```text
C:\dev\TheStampSizeDiyPeekDevice\BlePrompter\.pio\build\esp32c3\
```

Wichtige Dateien:

| Datei | Bedeutung |
| --- | --- |
| `bootloader.bin` | Startprogramm des ESP-Chips. Es startet nach Reset und lädt die Anwendung. |
| `partitions.bin` | Partitionstabelle. Sie beschreibt, wo Anwendung, Datenbereiche und weitere Partitionen im Flash liegen. |
| `firmware.bin` | Die eigentliche Anwendung aus deinem Quellcode. |
| `firmware.elf` | Debug- und Symbol-Datei für Entwickler. Nicht für den Anwender-Download nötig. |
| `firmware.map` | Speicherkarte des Builds. Hilfreich für Analyse, nicht für den Anwender-Download nötig. |

Zusätzlich braucht der ESP32-Arduino-Build meist `boot_app0.bin`. Diese Datei liegt nicht im Projektordner, sondern im PlatformIO-Paket:

```text
C:\Users\hesspet\.platformio\packages\framework-arduinoespressif32\tools\partitions\boot_app0.bin
```

## Warum die PlatformIO-`firmware.bin` nicht allein reicht

Die Datei `.pio/build/<umgebung>/firmware.bin` ist die Anwendung. Sie enthält normalerweise nicht Bootloader, Partitionstabelle und `boot_app0.bin`.

Beim normalen Upload macht PlatformIO deshalb einen mehrteiligen Flash-Vorgang mit `esptool`. Aus den aktuellen Build-Ausgaben ergeben sich diese Adressen:

### ESP32-C3 OLED

```text
0x0000   bootloader.bin
0x8000   partitions.bin
0xe000   boot_app0.bin
0x10000  firmware.bin
```

### CYB/CYD

```text
0x1000   bootloader.bin
0x8000   partitions.bin
0xe000   boot_app0.bin
0x10000  firmware.bin
```

Die Website-Manifestdateien in Zauberhaft zeigen aktuell auf eine einzige Datei mit Offset `0`:

```json
{ "path": ".../firmware.bin", "offset": 0 }
```

Das ist korrekt, wenn diese veröffentlichte `firmware.bin` ein zusammengeführtes Gesamtimage ist. Es wäre nicht korrekt, einfach die reine PlatformIO-App-Datei nach Zauberhaft zu kopieren und bei Offset `0` zu flashen.

## Prozessübersicht

Der vollständige Ablauf sieht so aus:

1. Version im Firmware-Projekt festlegen.
2. Firmware sauber bauen.
3. Optional auf echter Hardware testen.
4. Mehrere ESP-Binärdateien zu einem Gesamtimage bündeln.
5. Gesamtimage als `firmware.bin` ins Zauberhaft-Projekt kopieren.
6. Release-README aktualisieren.
7. Manifest und Firmware-Katalog prüfen.
8. Jekyll lokal starten und Manifest testen.
9. Über GitHub Pages veröffentlichen.
10. Anwender flasht über die Website mit ESP Web Tools.

## 1. Releaseversion festlegen

Im BlePrompter-Projekt steht die Programmversion in:

```text
C:\dev\TheStampSizeDiyPeekDevice\BlePrompter\include\config.h
```

Aktuell:

```cpp
constexpr const char *programVersion = "1.7.0";
```

Diese Version wird im Startbildschirm und in der seriellen Ausgabe verwendet. Vor einem Release sollte sie bewusst gesetzt werden.

Empfehlung:

```text
1.7.0
```

für stabile Releases, oder:

```text
1.7.0-test.1
1.7.0-debug.1
```

für Test- oder Debugstände. Wichtig ist nicht das konkrete Schema, sondern dass Quellcode, README, Website-Katalog und veröffentlichte Datei dieselbe Version meinen.

## 2. Arbeitsstand prüfen

Vor einem Release sollte klar sein, welcher Quellstand gebaut wird.

Im Firmware-Projekt:

```powershell
cd C:\dev\TheStampSizeDiyPeekDevice\BlePrompter
git status
```

Wenn das Projekt nicht als Git-Repository genutzt wird, ersetze diesen Schritt durch eine manuelle Prüfung: Welche Dateien wurden geändert? Ist `include/config.h` aktuell? Ist `platformio.ini` korrekt?

## 3. Sauber bauen

Für das ESP32-C3-OLED-Board:

```powershell
cd C:\dev\TheStampSizeDiyPeekDevice\BlePrompter
pio run -e esp32c3 --target clean
pio run -e esp32c3
```

Für das CYB/CYD-Board:

```powershell
cd C:\dev\TheStampSizeDiyPeekDevice\BlePrompter
pio run -e cyd --target clean
pio run -e cyd
```

Der Clean-Schritt löscht alte Build-Artefakte für diese Umgebung. Das ist vor einem Release sinnvoll, weil du dann nicht versehentlich eine alte Binärdatei weiterverwendest.

Nach dem Build sollten diese Dateien vorhanden sein:

Für `esp32c3`:

```text
.pio/build/esp32c3/bootloader.bin
.pio/build/esp32c3/partitions.bin
.pio/build/esp32c3/firmware.bin
```

Für `cyd`:

```text
.pio/build/cyd/bootloader.bin
.pio/build/cyd/partitions.bin
.pio/build/cyd/firmware.bin
```

## 4. Auf echter Hardware testen

Der Build allein sagt nur, dass der Code kompiliert. Vor einem öffentlichen Release sollte mindestens ein Gerät geflasht und kurz getestet werden.

ESP32-C3 OLED:

```powershell
cd C:\dev\TheStampSizeDiyPeekDevice\BlePrompter
pio run -e esp32c3 --target upload --upload-port COM6
pio device monitor --port COM6 --baud 115200
```

CYB/CYD:

```powershell
cd C:\dev\TheStampSizeDiyPeekDevice\BlePrompter
pio run -e cyd --target upload --upload-port COM11
pio device monitor --port COM11 --baud 115200
```

Kurz prüfen:

- Startbildschirm zeigt Programmname, Version und Builddatum.
- BLE-Gerät erscheint als `BlePrompter-xxxx`.
- Ein einfacher BLE-Befehl wie `TEXT Hallo` wird angezeigt.
- Bei Debug- oder Testversionen sind die erwarteten Logausgaben vorhanden.

## 5. Flash-Adressen mit PlatformIO nachvollziehen

Wenn du unsicher bist, welche Offsets zu einer Umgebung gehören, kannst du PlatformIO im Verbose-Modus starten. Mit einem ungültigen Port wird nichts geflasht, aber PlatformIO zeigt den geplanten `esptool`-Befehl.

Beispiel:

```powershell
cd C:\dev\TheStampSizeDiyPeekDevice\BlePrompter
pio run -e esp32c3 --target upload --upload-port COM0 --verbose
```

Am Ende steht ein Befehl mit `write_flash`. Daraus liest du die Paare aus Offset und Datei ab.

Für den aktuellen Stand gilt:

| Umgebung | Chip | Bootloader | Partitionen | Boot-App | Anwendung |
| --- | --- | --- | --- | --- | --- |
| `esp32c3` | `esp32c3` | `0x0000` | `0x8000` | `0xe000` | `0x10000` |
| `cyd` | `esp32` | `0x1000` | `0x8000` | `0xe000` | `0x10000` |

Diese Offsets sind nicht frei gewählt. Sie kommen aus der ESP32-Plattform, dem Board und der Partitionstabelle.

## 6. Gesamtimage mit esptool erzeugen

ESP Web Tools kann mehrere `parts` flashen. Für dieses Zauberhaft-Projekt ist aber die einfachste Regel:

```text
Veröffentliche eine zusammengeführte Datei namens firmware.bin und flashe sie bei Offset 0.
```

Dafür nutzt du `esptool merge_bin`. Das Tool ist bereits über PlatformIO installiert.

### ESP32-C3 OLED bündeln

```powershell
cd C:\dev\TheStampSizeDiyPeekDevice\BlePrompter

python "C:\Users\hesspet\.platformio\packages\tool-esptoolpy\esptool.py" --chip esp32c3 merge_bin `
  -o ".pio\build\esp32c3\BlePrompter-esp32c3-1.7.0-merged.bin" `
  --flash-mode dio `
  --flash-freq 80m `
  --flash-size 4MB `
  0x0000 ".pio\build\esp32c3\bootloader.bin" `
  0x8000 ".pio\build\esp32c3\partitions.bin" `
  0xe000 "C:\Users\hesspet\.platformio\packages\framework-arduinoespressif32\tools\partitions\boot_app0.bin" `
  0x10000 ".pio\build\esp32c3\firmware.bin"
```

Ergebnis:

```text
.pio/build/esp32c3/BlePrompter-esp32c3-1.7.0-merged.bin
```

### CYB/CYD bündeln

```powershell
cd C:\dev\TheStampSizeDiyPeekDevice\BlePrompter

python "C:\Users\hesspet\.platformio\packages\tool-esptoolpy\esptool.py" --chip esp32 merge_bin `
  -o ".pio\build\cyd\BlePrompter-cyd-1.7.0-merged.bin" `
  --flash-mode dio `
  --flash-freq 40m `
  --flash-size 4MB `
  0x1000 ".pio\build\cyd\bootloader.bin" `
  0x8000 ".pio\build\cyd\partitions.bin" `
  0xe000 "C:\Users\hesspet\.platformio\packages\framework-arduinoespressif32\tools\partitions\boot_app0.bin" `
  0x10000 ".pio\build\cyd\firmware.bin"
```

Wichtig: Im CYB/CYD-Beispiel muss der Pfad zu `boot_app0.bin` zu deinem Benutzerprofil passen. Auf diesem Rechner ist es:

```text
C:\Users\hesspet\.platformio\packages\framework-arduinoespressif32\tools\partitions\boot_app0.bin
```

Die lokal installierte PlatformIO-`esptool.py`-Version akzeptiert `merge_bin`. In neuerer Dokumentation taucht teils auch die Schreibweise `merge-bin` auf. Wenn du eine andere `esptool`-Version verwendest, prüfe bei Bedarf die Hilfe:

```powershell
python "C:\Users\hesspet\.platformio\packages\tool-esptoolpy\esptool.py" --chip esp32c3 --help
```

Einige `esptool`-Versionen verwenden den Unterstrich, andere den Bindestrich. Die Funktion ist dieselbe.

## 7. Optional: Gesamtimage prüfen

Du kannst die Datei mit `image-info` prüfen:

```powershell
python "C:\Users\hesspet\.platformio\packages\tool-esptoolpy\esptool.py" --chip esp32c3 image-info ".pio\build\esp32c3\BlePrompter-esp32c3-1.7.0-merged.bin"
```

Außerdem ist ein Hash sinnvoll:

```powershell
Get-FileHash ".pio\build\esp32c3\BlePrompter-esp32c3-1.7.0-merged.bin" -Algorithm SHA256
```

Der Hash ist kein Muss für ESP Web Tools. Er hilft aber, später zu erkennen, ob eine Datei wirklich unverändert ist.

## 8. Firmware in Zauberhaft bereitstellen

Wechsle ins Website-Projekt:

```powershell
cd C:\dev\Zauberhaft
```

Für die aktuelle BlePrompter-Releasevariante ist dieser Zielpfad vorgesehen:

```text
assets/firmware/bleprompter/release-1/firmware.bin
```

Kopiere das zusammengeführte ESP32-C3-Image dorthin:

```powershell
Copy-Item `
  "C:\dev\TheStampSizeDiyPeekDevice\BlePrompter\.pio\build\esp32c3\BlePrompter-esp32c3-1.7.0-merged.bin" `
  "C:\dev\Zauberhaft\assets\firmware\bleprompter\release-1\firmware.bin" `
  -Force
```

Wichtig: Der Zielname muss `firmware.bin` bleiben, weil das Manifest genau diese Datei referenziert.

## 9. Release-README aktualisieren

Zu jeder Firmwarevariante gehört eine README-Datei:

```text
assets/firmware/bleprompter/release-1/README.md
```

Aktualisiere dort mindestens:

- Version
- Datum im Format `DD.MM.YYYY`
- Chip
- kurze Beschreibung
- wichtige Änderungen
- bekannte Einschränkungen

Beispiel:

```markdown
# BlePrompter - Release 1

**Version:** 1.7.0
**Datum:** 08.06.2026
**Chip:** ESP32-C3

## Beschreibung

Stabile Releaseversion für das ESP32-C3-OLED-Board.

## Enthaltene Funktionen

- BLE-UART über Nordic UART Service
- Anzeige von Text, Symbolen, Pfeilen, Karten und Würfeln
- Zyklischer Tiefschlaf für bessere Batterielaufzeit

## Installation

1. ESP32-C3 per USB anschließen.
2. Auf der Firmware-Seite `Installieren` klicken.
3. Im Browser den seriellen Port auswählen.
4. Warten, bis der Flash-Vorgang abgeschlossen ist.
```

## 10. Firmware-Katalog prüfen

Die Firmware-Seite liest ihre Projekte und Varianten aus:

```text
_data/firmware.yml
```

Aktuell gibt es:

```yaml
projects:
  - name: BlePrompter
    slug: bleprompter
    description: BLE Prompter Firmware für ESP32-C3
    chip_family: ESP32-C3
    variants:
      - name: Release 1
        slug: release-1
        description: Stabile Version für den produktiven Einsatz
```

Wenn du nur die bestehende ESP32-C3-Releaseversion ersetzt, muss hier nichts geändert werden.

Wenn du eine neue Variante anlegen willst, zum Beispiel `release-2`, brauchst du:

```yaml
      - name: Release 2
        slug: release-2
        description: Stabile Version 2 für den produktiven Einsatz
```

Dann muss auch dieser Ordner existieren:

```text
assets/firmware/bleprompter/release-2/
```

## 11. Manifest prüfen oder anlegen

Für jede Variante gibt es eine Manifest-Datei unter:

```text
firmware/bleprompter/<varianten-slug>.md
```

Für `release-1`:

```text
firmware/bleprompter/release-1.md
```

Der Inhalt sieht aktuell so aus:

```json
{
  "name": "BlePrompter Release 1",
  "builds": [
    {
      "chipFamily": "ESP32-C3",
      "parts": [
        { "path": "{{ '/assets/firmware/bleprompter/release-1/firmware.bin' | relative_url }}", "offset": 0 }
      ]
    }
  ]
}
```

Das passt zu einem zusammengeführten Image. `offset: 0` bedeutet: Das Gesamtimage beginnt am Anfang des Flash-Speichers. Die internen Bestandteile liegen bereits an den richtigen Positionen, weil `esptool merge_bin` die Lücken passend aufgefüllt hat.

Wenn du eine CYB/CYD-Variante veröffentlichen willst, darf sie nicht dieselbe `chipFamily` wie ESP32-C3 verwenden. Für CYB/CYD brauchst du `ESP32`.

Beispiel:

```json
{
  "name": "BlePrompter CYD Release 1",
  "builds": [
    {
      "chipFamily": "ESP32",
      "parts": [
        { "path": "{{ '/assets/firmware/bleprompter-cyd/release-1/firmware.bin' | relative_url }}", "offset": 0 }
      ]
    }
  ]
}
```

## 12. Warum das Manifest so wichtig ist

ESP Web Tools lädt nicht einfach irgendeine Datei herunter. Es liest zuerst das Manifest.

Das Manifest sagt:

- Wie die Firmware heißt.
- Für welche Chipfamilie sie gedacht ist.
- Welche Datei oder Dateien geflasht werden.
- An welchen Flash-Offset jede Datei geschrieben wird.

ESP Web Tools erkennt den angeschlossenen Chip. Wenn im Manifest `ESP32-C3` steht, wird diese Firmware nur für ein ESP32-C3-Gerät ausgewählt. Für ein klassisches ESP32-Gerät muss `ESP32` angegeben werden.

## 13. Lokale Website prüfen

Starte Jekyll:

```powershell
cd C:\dev\Zauberhaft
bundle exec jekyll serve --livereload
```

Dann im Browser prüfen:

```text
http://localhost:4000/Zauberhaft/downloads/firmware/
```

Das Manifest direkt prüfen:

```text
http://localhost:4000/Zauberhaft/firmware/bleprompter/release-1/manifest.json
```

Die Manifest-Antwort muss gültiges JSON sein. Sie muss den korrekten Pfad zur Firmware enthalten:

```text
/Zauberhaft/assets/firmware/bleprompter/release-1/firmware.bin
```

Die Firmware-Datei direkt prüfen:

```text
http://localhost:4000/Zauberhaft/assets/firmware/bleprompter/release-1/firmware.bin
```

Der Browser sollte die Datei herunterladen oder als Binärdatei anzeigen.

## 14. Browser-Flash lokal testen

ESP Web Tools braucht Web Serial. Das funktioniert auf Desktop-Systemen in Chromium-basierten Browsern wie Chrome oder Edge. Die Seite muss über HTTPS geladen werden. `localhost` gilt für Browser als sichere Ausnahme.

Lokaler Test:

1. ESP-Gerät per USB anschließen.
2. `http://localhost:4000/Zauberhaft/downloads/firmware/` öffnen.
3. Bei der gewünschten Variante `Installieren` klicken.
4. Seriellen Port auswählen.
5. Flash-Vorgang beobachten.
6. Gerät nach Abschluss neu starten lassen.
7. BLE-Gerät und Startbildschirm prüfen.

Wenn der Flash-Vorgang fehlschlägt:

- Anderen USB-Port testen.
- USB-Kabel prüfen. Manche Kabel liefern nur Strom.
- Seriellen Monitor und andere Programme schließen.
- Bei manchen Boards beim Start des Flash-Vorgangs die Boot-Taste halten.
- Prüfen, ob die Manifest-`chipFamily` zum Gerät passt.

## 15. Veröffentlichen

Wenn lokal alles passt:

```powershell
cd C:\dev\Zauberhaft
git status
```

Erwartete Änderungen:

```text
assets/firmware/bleprompter/release-1/firmware.bin
assets/firmware/bleprompter/release-1/README.md
```

Falls neue Varianten angelegt wurden, zusätzlich:

```text
_data/firmware.yml
firmware/bleprompter/<varianten-slug>.md
assets/firmware/bleprompter/<varianten-slug>/
```

Nach Commit und Push nach `main` baut GitHub Pages die Website automatisch. Die produktive Seite liegt unter:

```text
https://hesspet.github.io/Zauberhaft/downloads/firmware/
```

GitHub Pages liefert HTTPS aus. Damit erfüllt die produktive Seite die Web-Serial-Anforderung von ESP Web Tools.

## 16. Anwenderprozess

Der Anwender braucht danach kein PlatformIO und keine Arduino IDE.

Für ihn sieht der Prozess so aus:

1. Firmware-Seite öffnen.
2. ESP-Gerät per USB anschließen.
3. `Installieren` klicken.
4. Seriellen Port auswählen.
5. Flash-Vorgang abwarten.
6. Gerät verwenden.

Die Website übernimmt dabei:

- Laden des ESP-Web-Tools-Skripts.
- Laden des passenden Manifests.
- Laden der `firmware.bin`.
- Schreiben in den Flash-Speicher über Web Serial.

## 17. Typische Fehlerquellen

### Reine PlatformIO-App-Datei wurde veröffentlicht

Symptom: Flash läuft durch, Gerät startet aber nicht korrekt.

Ursache: `.pio/build/<umgebung>/firmware.bin` wurde direkt nach Zauberhaft kopiert, obwohl das Manifest Offset `0` verwendet.

Lösung: Gesamtimage mit `esptool merge_bin` erzeugen und dieses als `assets/firmware/.../firmware.bin` veröffentlichen.

### Falsche Chipfamilie im Manifest

Symptom: ESP Web Tools wählt die Firmware nicht aus oder flasht nicht.

Ursache: Manifest enthält `ESP32-C3`, angeschlossen ist aber ein klassisches ESP32-Board, oder umgekehrt.

Lösung: `chipFamily` passend setzen:

| Gerät | `chipFamily` |
| --- | --- |
| ESP32-C3 OLED | `ESP32-C3` |
| CYB/CYD ESP32-WROOM-32 | `ESP32` |

### Falscher Bootloader-Offset beim Bündeln

Symptom: Gerät startet nicht oder bleibt im Bootloader hängen.

Ursache: ESP32-C3 und klassischer ESP32 haben unterschiedliche Bootloader-Offsets.

Lösung:

- ESP32-C3: Bootloader bei `0x0000`
- ESP32: Bootloader bei `0x1000`

### Alte Datei im Website-Projekt

Symptom: Website zeigt neue README, flasht aber alte Firmware.

Ursache: `firmware.bin` wurde nicht ersetzt oder Browser-/GitHub-Pages-Cache liefert noch alte Datei.

Lösung:

- Dateigröße und Hash prüfen.
- Build erneut veröffentlichen.
- URL mit Cache-Busting testen, zum Beispiel `firmware.bin?v=1.7.0`.

### Web Serial wird nicht angeboten

Symptom: Button zeigt, dass der Browser nicht unterstützt wird.

Ursache: Browser unterstützt Web Serial nicht oder Seite läuft nicht in einem sicheren Kontext.

Lösung:

- Chrome oder Edge auf Desktop nutzen.
- Produktivseite über HTTPS öffnen.
- Lokal `localhost` nutzen.

## 18. Dokumentationslinks

- [PlatformIO `pio run`](https://docs.platformio.org/en/latest/core/userguide/cmd_run.html)
- [ESP Web Tools](https://esphome.github.io/esp-web-tools/)
- [Espressif esptool: Basic Commands und `merge-bin`/`merge_bin`](https://docs.espressif.com/projects/esptool/en/latest/esp32/esptool/basic-commands.html)

## 19. Kurzcheckliste für ein BlePrompter-Release

1. `include/config.h` Version setzen.
2. `pio run -e esp32c3 --target clean` ausführen.
3. `pio run -e esp32c3` ausführen.
4. Optional mit `pio run -e esp32c3 --target upload --upload-port COM6` testen.
5. Mit `esptool merge_bin` ein Gesamtimage erzeugen.
6. Gesamtimage nach `C:\dev\Zauberhaft\assets\firmware\bleprompter\release-1\firmware.bin` kopieren.
7. `assets/firmware/bleprompter/release-1/README.md` aktualisieren.
8. Manifest unter `firmware/bleprompter/release-1.md` prüfen.
9. `bundle exec jekyll serve --livereload` starten.
10. Manifest und Firmware-Seite lokal prüfen.
11. Commit und Push nach `main`.
12. Produktivseite öffnen und Testflash durchführen.
