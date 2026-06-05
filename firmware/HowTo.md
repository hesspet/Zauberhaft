# HowTo: Firmware bereitstellen

## 1. Verzeichnisstruktur

```
Zauberhaft/
├── _data/firmware.yml                ← Firmware-Katalog (Projekte + Varianten)
├── assets/firmware/                   ← Firmware-Dateien (.bin) + Sidecar-READMEs
│   └── <projekt-slug>/
│       └── <variant-slug>/
│           ├── firmware.bin           ← Die eigentliche Firmware
│           └── README.md              ← Versionsinformationen
└── firmware/                          ← Manifest-Generator (eine .md pro Variante)
    └── <projekt-slug>/
        └── <variant-slug>.md         ← Erzeugt manifest.json-Endpunkt
```

## 2. Firmware-Datei bereitstellen

Die kompilierte `.bin`-Datei in das entsprechende Verzeichnis legen:

```
assets/firmware/<projekt-slug>/<variant-slug>/firmware.bin
```

**Wichtig:**

- Der Dateiname **muss** `firmware.bin` lauten (wird vom Manifest so referenziert)
- Die Datei muss f&uuml;r den passenden Chip kompiliert sein (z.&nbsp;B. ESP32-C3, ESP32-S3)
- Der Pfad ab `assets/` wird &uuml;ber GitHub Pages als statische Datei ausgeliefert

## 3. Sidecar-README anlegen

Zu jeder Firmware-Variante geh&ouml;rt eine `README.md` mit Release-Informationen:

```
assets/firmware/<projekt-slug>/<variant-slug>/README.md
```

**Empfohlener Inhalt:**

```markdown
# Projektname — Variante

**Version:** 1.0.0
**Datum:** TT.MM.JJJJ
**Chip:** ESP32-XX

## Beschreibung
Kurze Zusammenfassung, f&uuml;r wen diese Version gedacht ist.

## Enthaltene Features
- Feature 1
- Feature 2

## Installation
1. ESP32 &uuml;ber USB mit dem Computer verbinden
2. Auf der Firmware-Seite den „Installieren"-Button klicken
3. Im Browser-Dialog den seriellen Port ausw&auml;hlen
4. Warten bis der Flash-Vorgang abgeschlossen ist

## Bekannte Einschr&auml;nkungen
- Einschr&auml;nkung 1
```

## 4. Firmware im Katalog registrieren

Jede Variante muss in `_data/firmware.yml` eingetragen sein:

```yaml
projects:
  - name: Projektname           # Anzeigename auf der Webseite
    slug: projekt-slug          # URL-Komponente (Kleinschreibung, Bindestriche)
    description: Kurzbeschreibung des Projekts
    chip_family: ESP32-C3       # G&uuml;ltige Werte: ESP32, ESP32-C3, ESP32-S2, ESP32-S3
    variants:
      - name: Release 1         # Anzeigename der Variante
        slug: release-1         # URL-Komponente (muss mit Verzeichnisnamen &uuml;bereinstimmen)
        description: Kurzbeschreibung der Variante
      - name: Debug
        slug: debug
        description: Debug-Version mit Log-Ausgabe
```

**Regeln f&uuml;r `slug`:**

- Kleinschreibung, Bindestriche statt Leerzeichen
- `slug` in der YAML muss mit dem Verzeichnisnamen unter `assets/firmware/` &uuml;bereinstimmen
- `slug` wird auch f&uuml;r die Manifest-URL verwendet

## 5. Manifest-Generator anlegen

Jede Variante braucht eine kleine Markdown-Datei, die den ESP-Web-Tools-Manifest-Endpunkt erzeugt:

```
firmware/<projekt-slug>/<variant-slug>.md
```

**Inhalt (komplett &uuml;bernehmen, nur Projektname und Chip anpassen):**

```yaml
---
layout: firmware_manifest.json
permalink: /firmware/projekt-slug/variant-slug/manifest.json
---
{
  "name": "Projektname Variante",
  "builds": [
    {
      "chipFamily": "ESP32-C3",
      "parts": [
        { "path": "{{ '/assets/firmware/projekt-slug/variant-slug/firmware.bin' | relative_url }}", "offset": 0 }
      ]
    }
  ]
}
```

**Erkl&auml;rung:**

- `layout: firmware_manifest.json` sorgt daf&uuml;r, dass Jekyll nur das JSON ausgibt (kein HTML-Wrapper)
- `permalink` legt die URL fest, unter der das Manifest erreichbar ist
- `chipFamily` muss mit dem Eintrag in `_data/firmware.yml` &uuml;bereinstimmen
- `path` verwendet `relative_url`, damit der Pfad mit dem `baseurl`-Pr&auml;fix (`/Zauberhaft`) korrigiert wird
- `offset: 0` ist der Standard — Flash-Beginn bei Adresse 0x0. Bei Partitionstabellen oder Bootloadern abweichende Offsets verwenden

## 6. Lokal testen

```bash
bundle exec jekyll serve --livereload
```

**Pr&uuml;fen:**

1. Manifest-Endpunkt im Browser &ouml;ffnen:
   `http://localhost:4000/Zauberhaft/firmware/projekt-slug/variant-slug/manifest.json`
   → Muss sauberes JSON mit `name`, `builds`, `chipFamily` und `parts` zeigen

2. Firmware-Seite aufrufen:
   `http://localhost:4000/Zauberhaft/downloads/firmware/`
   → Die neue Variante erscheint unter dem Projekt

3. Sidecar-README pr&uuml;fen:
   `http://localhost:4000/Zauberhaft/assets/firmware/projekt-slug/variant-slug/README.md`
   → Wird als Markdown gerendert (GitHub Pages Styles) oder als Rohdaten angezeigt

4. ESP Web Tools testen (nur mit angeschlossenem ESP32):
   - Auf „Installieren" klicken
   - Browser-Dialog f&uuml;r seriellen Port best&auml;tigen
   - Flash-Vorgang beobachten

**Hinweis:** Web Serial API funktioniert nur &uuml;ber `https://` — lokal getestet werden kann das nur mit einem selbst-signierten Zertifikat oder indem man `localhost` verwendet (wird von Browsern als sicher eingestuft).

## 7. Ver&ouml;ffentlichen

Nach Commit und Push nach `main` baut GitHub Pages automatisch:

1. `.bin`-Dateien werden unter `assets/firmware/` ausgeliefert
2. Manifest-JSONs werden aus den `.md`-Dateien unter `firmware/` generiert
3. Die Firmware-Seite zeigt die neuen Varianten an
4. ESP Web Tools finden die Manifeste und k&ouml;nnen flashen

## 8. Chip-Family-Referenz

G&uuml;ltige Werte f&uuml;r `chipFamily` in Manifest und YAML:

| Wert | Controller |
|------|-----------|
| `ESP32` | ESP32 (klassisch) |
| `ESP32-C3` | ESP32-C3 (RISC-V) |
| `ESP32-S2` | ESP32-S2 |
| `ESP32-S3` | ESP32-S3 |

## 9. Mehrere Projekte

Die Struktur ist f&uuml;r beliebig viele Projekte ausgelegt. Neues Projekt anlegen:

1. Neuen Eintrag in `_data/firmware.yml` (unter `projects:`)
2. Verzeichnis `assets/firmware/<neuer-slug>/` anlegen
3. Pro Variante: `firmware.bin` + `README.md` + Manifest-`.md`
4. Fertig — die Firmware-Seite iteriert automatisch &uuml;ber alle Projekte
