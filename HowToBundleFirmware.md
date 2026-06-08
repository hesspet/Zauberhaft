# HowTo: Firmware bündeln und bereitstellen

Stand: 08.06.2026

Diese Anleitung beschreibt den aktuellen Weg von einer Releaseversion im PlatformIO-Projekt `C:\dev\TheStampSizeDiyPeekDevice\BlePrompter` bis zu den Dateien, die im Website-Projekt `C:\dev\Zauberhaft` für ESP Web Tools bereitgestellt werden.

Der empfohlene Weg ist heute nicht mehr, `esptool` manuell aufzurufen. Das Firmware-Projekt enthält dafür das Builder-Skript:

```powershell
C:\dev\TheStampSizeDiyPeekDevice\BlePrompter\tools\BuildDownloadBins.ps1
```

Hinweis: Der Dateiname lautet **`BuildDownloadBins.ps1`**. Falls irgendwo `BuildDownloadsBin.ps1` steht, ist das nur ein Vertipper.

Das Skript baut alle veröffentlichbaren Boards, bündelt die einzelnen ESP-Binärdateien zu einem vollständigen Flash-Image und erzeugt pro Board ein fertiges Download-Paket mit:

- zusammengeführter `.bin`
- technischer `.md`-Info-Datei
- statischer `manifest.json`

## Beteiligte Projekte

### Firmware-Projekt

```text
C:\dev\TheStampSizeDiyPeekDevice\BlePrompter
```

Dieses Projekt enthält die Firmware und das Builder-Skript.

Aktuelle PlatformIO-Umgebungen:

| Umgebung | Gerät | Chipfamilie | Bootloader-Offset |
| --- | --- | --- | --- |
| `esp32c3` | ESP32-C3 OLED | `ESP32-C3` | `0x0000` |
| `cyd` | CYB/CYD Board | `ESP32` | `0x1000` |

Die Umgebungen stehen in:

```text
C:\dev\TheStampSizeDiyPeekDevice\BlePrompter\platformio.ini
```

### Website-Projekt

```text
C:\dev\Zauberhaft
```

Dieses Projekt hostet die fertigen Download-Dateien über GitHub Pages. Die Anwenderseite liegt unter:

```text
/downloads/firmware/
```

Die Website nutzt ESP Web Tools. Der Anwender klickt auf `Installieren`, wählt den seriellen Port aus und flasht die Firmware direkt im Browser.

## Warum ein Gesamtimage nötig ist

PlatformIO erzeugt nicht nur eine einzelne Anwendungsdatei. Für einen vollständigen ESP-Flash-Vorgang werden mehrere Dateien an festen Offsets geschrieben:

| Bestandteil | ESP32-C3 OLED | CYB/CYD |
| --- | --- | --- |
| `bootloader.bin` | `0x0000` | `0x1000` |
| `partitions.bin` | `0x8000` | `0x8000` |
| `boot_app0.bin` | `0xe000` | `0xe000` |
| `firmware.bin` | `0x10000` | `0x10000` |

Die Datei `.pio\build\<umgebung>\firmware.bin` ist nur die Anwendung. Sie enthält normalerweise nicht Bootloader, Partitionstabelle und `boot_app0.bin`.

Für die Website wird deshalb ein zusammengeführtes Gesamtimage erzeugt. Dieses Gesamtimage wird von ESP Web Tools als einzelner Manifest-Part mit Offset `0` geflasht:

```json
{
  "path": "BlePrompter-esp32c3-v1.7.0-20260608-104642-download.bin",
  "offset": 0
}
```

## Builder-Skript

Das zentrale Skript ist:

```powershell
C:\dev\TheStampSizeDiyPeekDevice\BlePrompter\tools\BuildDownloadBins.ps1
```

Es wird normalerweise über den Batch-Starter ausgeführt:

```powershell
cd C:\dev\TheStampSizeDiyPeekDevice\BlePrompter
tools\BuildDownloadBins.bat
```

Der Batch-Starter ruft intern das PowerShell-Skript mit passender Execution Policy auf.

Das Skript erledigt:

- Programmname und Version aus `include\config.h` lesen
- `pio run -e <umgebung> --target clean` ausführen
- `pio run -e <umgebung>` ausführen
- `bootloader.bin`, `partitions.bin`, `boot_app0.bin` und `firmware.bin` mit `esptool.py merge_bin` bündeln
- SHA256 der erzeugten Download-Binärdatei berechnen
- technische Markdown-Info erzeugen
- `manifest.json` für ESP Web Tools erzeugen
- alte flache Artefakte direkt unter `download_bins` entfernen
- pro Board ein eigenes Unterverzeichnis erzeugen

## Ausgabe des Builder-Skripts

Nach einem erfolgreichen Lauf liegt die finale Struktur hier:

```text
C:\dev\TheStampSizeDiyPeekDevice\BlePrompter\download_bins\
├── esp32c3\
│   ├── BlePrompter-esp32c3-v<version>-<zeitstempel>-download.bin
│   ├── BlePrompter-esp32c3-v<version>-<zeitstempel>-download.md
│   └── manifest.json
└── cyd\
    ├── BlePrompter-cyd-v<version>-<zeitstempel>-download.bin
    ├── BlePrompter-cyd-v<version>-<zeitstempel>-download.md
    └── manifest.json
```

Diese Ordner sind die finale Zusammenstellung für die Bereitstellung. Für die Website wird ein Board-Ordner komplett in den passenden Asset-Ordner kopiert.

## Manifest-Regel

Die `manifest.json` liegt immer im selben Ordner wie die `.bin`. Deshalb verweist `path` relativ auf die Datei:

```json
{
  "name": "BlePrompter ESP32-C3 OLED 1.7.0",
  "builds": [
    {
      "chipFamily": "ESP32-C3",
      "parts": [
        {
          "path": "BlePrompter-esp32c3-v1.7.0-20260608-104642-download.bin",
          "offset": 0
        }
      ]
    }
  ]
}
```

Das ist wichtig: Die Website darf nicht mehr auf einen Jekyll-generierten Markdown-Manifest-Endpunkt unter `firmware/.../manifest.json` angewiesen sein. Das Manifest wird statisch unter `assets/firmware/.../manifest.json` ausgeliefert.

Für CYB/CYD muss `chipFamily` `ESP32` sein. Für ESP32-C3 OLED muss `chipFamily` `ESP32-C3` sein.

## Firmware in Zauberhaft bereitstellen

Für die aktuell veröffentlichte ESP32-C3-Variante ist der Zielordner:

```text
C:\dev\Zauberhaft\assets\firmware\bleprompter\esp32c3
```

Kopiere den Inhalt des erzeugten Board-Ordners dorthin:

```powershell
Copy-Item `
  -Path "C:\dev\TheStampSizeDiyPeekDevice\BlePrompter\download_bins\esp32c3\*" `
  -Destination "C:\dev\Zauberhaft\assets\firmware\bleprompter\esp32c3" `
  -Recurse `
  -Force
```

Danach müssen im Zielordner mindestens diese Dateien liegen:

```text
assets/firmware/bleprompter/esp32c3/
├── BlePrompter-esp32c3-v<version>-<zeitstempel>-download.bin
├── BlePrompter-esp32c3-v<version>-<zeitstempel>-download.md
└── manifest.json
```

Wenn eine alte `.bin` oder `.md` mit vorherigem Zeitstempel dort liegt, sollte sie entfernt werden, damit die Website nicht mehrere veraltete Artefakte enthält.

## Firmware-Katalog in Zauberhaft

Die Firmware-Seite liest ihre Einträge aus:

```text
C:\dev\Zauberhaft\_data\firmware.yml
```

Für ESP32-C3 sieht der Eintrag sinngemäß so aus:

```yaml
projects:
  - name: BlePrompter
    slug: bleprompter
    description: BLE Prompter Firmware für ESP32-C3 OLED
    chip_family: ESP32-C3
    variants:
      - name: ESP32-C3 OLED 1.7.0
        slug: esp32c3
        description: Stabile Download-Firmware vom 08.06.2026 für das ESP32-C3-OLED-Board
        firmware_file: BlePrompter-esp32c3-v1.7.0-20260608-104642-download.bin
        info_file: BlePrompter-esp32c3-v1.7.0-20260608-104642-download.md
```

Wichtig:

- `slug` muss zum Asset-Ordner passen.
- `info_file` steuert den Info-Link auf der Website.
- Die Installation nutzt `assets/firmware/<projekt>/<variante>/manifest.json`.
- Wenn sich der Zeitstempel im Dateinamen ändert, müssen `firmware_file`, `info_file` und `manifest.json` zusammenpassen.

## Firmware-Seite

Die relevante Seite ist:

```text
C:\dev\Zauberhaft\downloads\firmware.md
```

Der Install-Button muss auf das statische Manifest unter `assets/firmware` zeigen:

```liquid
manifest="{{ '/assets/firmware/' | append: project.slug | append: '/' | append: variant.slug | append: '/manifest.json' | relative_url }}"
```

Der Info-Link zeigt auf die konfigurierte Markdown-Datei:

```liquid
href="{{ '/assets/firmware/' | append: project.slug | append: '/' | append: variant.slug | append: '/' | append: variant.info_file | relative_url }}"
```

## Lokale Prüfung

Wenn Jekyll lokal verfügbar ist:

```powershell
cd C:\dev\Zauberhaft
bundle exec jekyll serve --livereload
```

Dann prüfen:

```text
http://localhost:4000/Zauberhaft/downloads/firmware/
http://localhost:4000/Zauberhaft/assets/firmware/bleprompter/esp32c3/manifest.json
```

Die Manifest-Antwort muss gültiges JSON sein. Der `path` in der Manifest-Datei muss auf eine Datei zeigen, die im selben Ordner existiert.

Schnellprüfung per PowerShell:

```powershell
$manifestPath = "C:\dev\Zauberhaft\assets\firmware\bleprompter\esp32c3\manifest.json"
$manifest = Get-Content -Raw $manifestPath | ConvertFrom-Json
$firmwarePath = Join-Path (Split-Path -Parent $manifestPath) $manifest.builds[0].parts[0].path
Test-Path -LiteralPath $firmwarePath
```

Das Ergebnis muss `True` sein.

## Browser-Flash testen

ESP Web Tools braucht Web Serial. Das funktioniert auf Desktop-Systemen in Chromium-basierten Browsern wie Chrome oder Edge.

Produktiv läuft die Seite über HTTPS:

```text
https://hesspet.github.io/Zauberhaft/downloads/firmware/
```

Testablauf:

1. ESP-Gerät per USB anschließen.
2. Firmware-Seite öffnen.
3. Bei der passenden Variante `Installieren` klicken.
4. Seriellen Port auswählen.
5. Flash-Vorgang abwarten.
6. Gerät neu starten lassen.
7. Startbildschirm, BLE-Name und einfache BLE-Befehle prüfen.

## Typische Fehlerquellen

### `Failed to download manifest`

Ursache: Die Manifest-URL zeigt auf eine Datei, die nicht existiert, nicht veröffentlicht wurde oder nicht als statische JSON-Datei erreichbar ist.

Lösung:

- Prüfen, ob `assets/firmware/<projekt>/<variante>/manifest.json` existiert.
- Manifest-URL direkt im Browser öffnen.
- Prüfen, ob der Install-Button auf `assets/firmware/.../manifest.json` zeigt.
- Nicht mehr auf `firmware/<projekt>/<variante>/manifest.json` aus einer Markdown-Datei setzen.

### Manifest lädt, aber Firmware lädt nicht

Ursache: `path` in `manifest.json` zeigt auf eine Datei, die im Manifest-Ordner nicht existiert.

Lösung:

- `path` nur als relativen Dateinamen setzen.
- `.bin` und `manifest.json` im selben Ordner halten.
- Dateinamen inklusive Zeitstempel exakt vergleichen.

### Falsche Chipfamilie

Ursache: Manifest enthält `ESP32-C3`, angeschlossen ist aber ein klassischer ESP32, oder umgekehrt.

Lösung:

| Gerät | `chipFamily` |
| --- | --- |
| ESP32-C3 OLED | `ESP32-C3` |
| CYB/CYD ESP32-WROOM-32 | `ESP32` |

### Gerät startet nach Flash nicht

Ursache: Reine PlatformIO-App-Datei wurde veröffentlicht oder mit falschem Bootloader-Offset gebündelt.

Lösung:

- Immer die vom Builder-Skript erzeugte `*-download.bin` verwenden.
- ESP32-C3: Bootloader bei `0x0000`.
- ESP32/CYD: Bootloader bei `0x1000`.

### Website zeigt neue Info, flasht aber alte Firmware

Ursache: Alte `.bin`, alte `manifest.json` oder Browser-/GitHub-Pages-Cache.

Lösung:

- Zielordner vor dem Kopieren bereinigen.
- `manifest.json` und `info_file` auf denselben Zeitstempel prüfen.
- Direkt die Manifest-URL öffnen und den `path` kontrollieren.

## Veröffentlichung

Nach dem Kopieren in `C:\dev\Zauberhaft` prüfen:

```powershell
cd C:\dev\Zauberhaft
git status
```

Erwartete Änderungen bei einer neuen ESP32-C3-Version:

```text
assets/firmware/bleprompter/esp32c3/manifest.json
assets/firmware/bleprompter/esp32c3/BlePrompter-esp32c3-v<version>-<zeitstempel>-download.bin
assets/firmware/bleprompter/esp32c3/BlePrompter-esp32c3-v<version>-<zeitstempel>-download.md
_data/firmware.yml
```

Falls alte Artefakte ersetzt werden, erscheinen diese zusätzlich als gelöscht.

Nach Commit und Push nach `main` baut GitHub Pages die Website automatisch.

## Kurzcheckliste

1. Version in `include\config.h` prüfen.
2. Im Firmware-Projekt `tools\BuildDownloadBins.bat` ausführen.
3. Prüfen, ob `download_bins\esp32c3` und `download_bins\cyd` jeweils `.bin`, `.md` und `manifest.json` enthalten.
4. Gewünschten Board-Ordner nach `C:\dev\Zauberhaft\assets\firmware\bleprompter\<variante>` kopieren.
5. Alte Artefakte im Zielordner entfernen.
6. `_data\firmware.yml` auf neuen Dateinamen und Zeitstempel aktualisieren.
7. Manifest direkt öffnen und JSON prüfen.
8. Firmware-Seite öffnen.
9. Browser-Flash mit dem passenden Gerät testen.
10. Änderungen committen und nach GitHub Pages veröffentlichen.
