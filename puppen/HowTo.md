# HowTo: Puppen-Steckbriefe pflegen

## 1. Verzeichnisstruktur

```
Zauberhaft/
├── _puppen/                          ← Hier liegen die Steckbrief-Dateien
│   ├── nasreddin.md
│   ├── alrich.md
│   └── elmse.md
├── _data/
│   ├── puppen.yml                    ← Überschrift und Einleitung der Übersicht
│   └── texte.yml                     ← Beschriftungen (mehrsprachig vorbereitet)
├── _layouts/puppen.html              ← Rahmen für Übersicht und Steckbrief-Seiten
├── _includes/
│   ├── puppen_uebersicht.html        ← Passbild-Raster (Übersicht und Deep Link)
│   └── footer.html                   ← Fußzeile mit Build-Datum
├── assets/puppen/
│   ├── passbilder/                   ← Portrait-Fotos (quadratisch, min. 400×400px)
│   │   ├── nasreddin.jpg
│   │   ├── alrich.jpg
│   │   └── elmse-wetterwachs.jpg
│   ├── steckbriefe/                  ← Bilder für die Steckbrief-Inhalte
│   │   ├── nasreddin/
│   │   │   └── show.jpg
│   │   ├── alrich/
│   │   │   └── portrait.jpg
│   │   └── elmse/
│   │       └── teetasse.jpg
│   ├── css/puppen.css                ← Aussehen von Raster und Overlay
│   └── js/puppen.js                  ← Overlay und Deep-Link-Logik
└── puppen/
    ├── index.md                      ← Übersichtsseite (nicht manuell ändern)
    └── HowTo.md                      ← Diese Datei
```

## 2. Neuen Steckbrief anlegen

Eine neue Markdown-Datei in `_puppen/` erstellen. Der Dateiname wird Teil der Adresse:

```
_puppen/neue-figur.md  →  /Zauberhaft/puppen/neue-figur/
```

### 2.1 Frontmatter (Pflichtfelder)

Jeder Steckbrief beginnt mit einem YAML-Header zwischen `---`:

```yaml
---
name: Name der Figur
kurztext: Ein Satz, der die Figur beschreibt (max. 120 Zeichen)
passbild: /assets/puppen/passbilder/dateiname.jpg
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

<img src="{{ '/assets/puppen/steckbriefe/neue-figur/bild.jpg' | relative_url }}" alt="Beschreibung">
```

**Wichtig bei Bildpfaden:** Im Markdown-Body **keine** Markdown-Syntax (`![...](...)`) für Bilder verwenden, sondern HTML mit dem Liquid-Filter `relative_url` — nur so wird `site.baseurl` korrekt vorangestellt. Der Pfad beginnt **ohne** `/Zauberhaft/`, also z.B. `/assets/puppen/steckbriefe/neue-figur/bild.jpg`. Das `relative_url`-Filter im Template setzt die Baseurl automatisch davor.

## 3. Deep Links: einzelne Figuren verlinken

Jeder Steckbrief hat eine eigene, teilbare Adresse:

```
https://hesspet.github.io/Zauberhaft/puppen/nasreddin/
```

Diese Adresse zeigt **keine** isolierte Textseite, sondern die komplette Puppen-Ansicht
(Navigation, Einleitung, Passbild-Raster, Fußzeile) — genau wie beim Aufruf von
`https://hesspet.github.io/Zauberhaft/puppen/`, nur mit bereits geöffnetem Steckbrief.
Damit sind die Adressen für Publikationen, Flyer, Social Media und Werbung geeignet.

- Der Dateiname in `_puppen/` bestimmt die Adresse: `_puppen/neue-figur.md` → `/puppen/neue-figur/`.
- Für gedruckte Veröffentlichungen den Dateinamen **nicht nachträglich ändern** —
  sonst verschwindet die Adresse.
- Auf der Übersicht schreibt ein Klick auf ein Passbild die Steckbrief-Adresse in die
  Adresszeile. Einfach kopieren und veröffentlichen.
- Ohne JavaScript bleibt alles nutzbar: Jedes Passbild ist ein normaler Verweis, und der
  Schließen-Knopf führt zur Übersicht `/puppen/`.

## 4. Passbilder vorbereiten

- **Format:** Quadratisch (1:1), JPG oder WebP
- **Mindestgröße:** 400×400 Pixel (wird im Browser auf 150px skaliert, aber höhere Auflösung sieht auf HiDPI-Displays besser aus)
- **Ablage:** `assets/puppen/passbilder/`
- **Dateiname:** Kleinschreibung, Bindestriche statt Leerzeichen, z. B. `elmse-wetterwachs.jpg`

Ein Bildbearbeitungsprogramm mit kreisförmigem Freisteller ist hilfreich, aber nicht zwingend — das CSS macht die Ecken von selbst rund.

## 5. Reihenfolge beachten

Die `reihenfolge`-Werte müssen nicht lückenlos sein (10, 20, 30 geht auch), sollten aber eindeutig sein. Bei gleicher Reihenfolge entscheidet Jekyll nach Dateiname.

**Empfehlung:** In 10er-Schritten nummerieren (10, 20, 30 …), dann kann man später leicht eine Figur einschieben ohne alle Nummern ändern zu müssen.

## 6. Steckbrief löschen oder ausblenden

- **Löschen:** Datei aus `_puppen/` entfernen, Passbild und Steckbrief-Bilder aus `assets/puppen/` löschen.
- **Vorübergehend ausblenden:** Die Datei aus `_puppen/` in einen Ordner außerhalb verschieben (z. B. `_puppen_entwuerfe/`), solange das nicht als Collection konfiguriert ist.

Ein `status: entwurf`-Feld wie bei den Blog-Artikeln gibt es für Puppen nicht — die Collection ist bewusst einfach gehalten.

## 7. Lokal testen

```bash
bundle exec jekyll serve --livereload
```

Dann im Browser öffnen:

- Übersicht: `http://localhost:4000/Zauberhaft/puppen/`
- Deep Link (Steckbrief innerhalb der Ansicht): `http://localhost:4000/Zauberhaft/puppen/neue-figur/`

Klick auf ein Passbild testen, ob das Overlay aufgeht, die Adresszeile die Steckbrief-Adresse
zeigt und der Zurück-Knopf des Browsers den Steckbrief wieder schließt.

## 8. Veröffentlichen

Nach dem Commit und Push nach `main` baut GitHub Pages automatisch. Die neue Figur erscheint ohne weiteres Zutun auf der Übersichtsseite.

## 9. Texte und Gestaltung

- **Überschrift und Einleitung** der Übersichtsseite stehen in `_data/puppen.yml`.
  Jeder Eintrag unter `absaetze` wird ein Absatz; `<br>` erzeugt einen harten Umbruch.
- **Beschriftungen** (Schließen, Ladehinweis, Fehlertext) stehen in `_data/texte.yml`
  unter `de.puppen`. Ein weiterer Sprachblock (z. B. `en:`) genügt, damit eine zweite
  Sprache ohne Codeänderung möglich ist.
- **Aussehen** von Raster und Overlay: `assets/puppen/css/puppen.css`. Die wichtigsten Klassen:
  - `.puppen-steckbrief` — Container für den Steckbrief-Inhalt
  - `.puppen-overlay` — abgedunkelter Hintergrund
  - Überschriften (`h1`, `h2`, `h3`), Absätze, Listen, Zitate (`blockquote`), Bilder sind gestylt

Eigene Anpassungen am CSS sind möglich, aber bitte konsistent zum Rest der Zauberhaft-Seite im Dark-Theme mit Goldakzenten halten.
