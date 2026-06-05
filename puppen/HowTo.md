# HowTo: Puppen-Steckbriefe pflegen

## 1. Verzeichnisstruktur

```
Zauberhaft/
├── _puppen/                          ← Hier liegen die Steckbrief-Dateien
│   ├── nasreddin.md
│   ├── alrich.md
│   └── emse-wetterwachs.md
├── assets/puppen/
│   ├── passbilder/                   ← Portrait-Fotos (quadratisch, min. 400×400px)
│   │   ├── nasreddin.jpg
│   │   ├── alrich.jpg
│   │   └── emse-wetterwachs.jpg
│   └── steckbriefe/                  ← Bilder für die Steckbrief-Inhalte
│       ├── nasreddin/
│       │   └── show.jpg
│       ├── alrich/
│       │   └── portrait.jpg
│       └── emse/
│           └── teetasse.jpg
└── puppen/
    ├── index.md                      ← Übersichtsseite (nicht manuell ändern)
    └── HowTo.md                      ← Diese Datei
```

## 2. Neuen Steckbrief anlegen

Eine neue Markdown-Datei in `_puppen/` erstellen. Der Dateiname wird Teil der URL:

```
_puppen/neue-figur.md  →  /Zauberhaft/puppen/neue-figur/
```

### 2.1 Frontmatter (Pflichtfelder)

Jeder Steckbrief beginnt mit einem YAML-Header zwischen `---`:

```yaml
---
name: Name der Figur
kurztext: Ein Satz, der die Figur beschreibt (max. 120 Zeichen)
passbild: /Zauberhaft/assets/puppen/passbilder/dateiname.jpg
reihenfolge: 4
---
```

| Feld | Pflicht | Beschreibung |
|------|---------|-------------|
| `name` | Ja | Anzeigename unter dem Passbild und als Steckbrief-Überschrift |
| `kurztext` | Ja | Kurzbeschreibung unter dem Passbild (1–2 Zeilen) |
| `passbild` | Nein | Pfad zum Portrait-Foto. Wenn nicht gesetzt, erscheint ein Platzhalter mit „?" |
| `reihenfolge` | Ja | Zahl, die die Sortierung auf der Übersichtsseite bestimmt (1 erscheint zuerst) |

### 2.2 Steckbrief-Inhalt (Markdown)

Unterhalb des YAML-Headers folgt der Steckbrief als ganz normales Markdown:

```markdown
## Überschrift

Fließtext mit **Formatierung** und *Betonung*.

### Unterüberschrift

- Aufzählung
- mit
- Punkten

> Ein schönes Zitat der Figur

![Beschreibung](/Zauberhaft/assets/puppen/steckbriefe/neue-figur/bild.jpg)
```

**Wichtig bei Bildpfaden:** Immer mit `/Zauberhaft/assets/puppen/…` beginnen (absoluter Pfad ab Website-Wurzel). Relative Pfade funktionieren im Overlay nicht zuverlässig.

## 3. Passbilder vorbereiten

- **Format:** Quadratisch (1:1), JPG oder WebP
- **Mindestgröße:** 400×400 Pixel (wird im Browser auf 150px skaliert, aber höhere Auflösung sieht auf HiDPI-Displays besser aus)
- **Ablage:** `assets/puppen/passbilder/`
- **Dateiname:** Kleinschreibung, Bindestriche statt Leerzeichen, z. B. `emse-wetterwachs.jpg`

Ein Bildbearbeitungsprogramm mit kreisförmigem Freisteller ist hilfreich, aber nicht zwingend — das CSS macht die Ecken von selbst rund.

## 4. Reihenfolge beachten

Die `reihenfolge`-Werte müssen nicht lückenlos sein (10, 20, 30 geht auch), sollten aber eindeutig sein. Bei gleicher Reihenfolge entscheidet Jekyll nach Dateiname.

**Empfehlung:** In 10er-Schritten nummerieren (10, 20, 30 …), dann kann man später leicht eine Figur einschieben ohne alle Nummern ändern zu müssen.

## 5. Steckbrief löschen oder ausblenden

- **Löschen:** Datei aus `_puppen/` entfernen, Passbild und Steckbrief-Bilder aus `assets/puppen/` löschen.
- **Vorübergehend ausblenden:** Die Datei aus `_puppen/` in einen Ordner außerhalb verschieben (z. B. `_puppen_entwuerfe/`), solange das nicht als Collection konfiguriert ist.

Ein `status: entwurf`-Feld wie bei den Blog-Artikeln gibt es für Puppen nicht — die Collection ist bewusst einfach gehalten.

## 6. Lokal testen

```bash
bundle exec jekyll serve --livereload
```

Dann im Browser öffnen:

- Übersicht: `http://localhost:4000/Zauberhaft/puppen/`
- Steckbrief direkt: `http://localhost:4000/Zauberhaft/puppen/neue-figur/`

Klick auf ein Passbild testen, ob das Overlay aufgeht und der Steckbrief-Inhalt korrekt erscheint.

## 7. Veröffentlichen

Nach dem Commit und Push nach `main` baut GitHub Pages automatisch. Die neue Figur erscheint ohne weiteres Zutun auf der Übersichtsseite.

## 8. Gestaltungsfreiheit

Das Overlay-CSS (`assets/puppen/css/puppen.css`) definiert das Aussehen der Steckbriefe im Popup. Die wichtigsten Klassen:

- `.puppen-steckbrief` — Container für den Steckbrief-Inhalt
- Überschriften (`h1`, `h2`, `h3`), Absätze, Listen, Zitate (`blockquote`) und Bilder sind gestylt

Eigene Anpassungen am CSS sind möglich, aber bitte konsistent zum Rest der Zauberhaft-Seite im Dark-Theme mit Goldakzenten halten.
