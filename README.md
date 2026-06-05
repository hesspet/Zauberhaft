# Zauberhaft

Startseite und Verteiler für Peters verrückte Ideen — eine statische Single-Page-Website mit **Jekyll**, publiziert über **GitHub Pages**.

## Lokale Vorschau

### Ohne Jekyll (schnellster Weg)

```powershell
start index.html
```

Ohne Jekyll wird nur das rohe HTML ohne Layouts/Includes angezeigt. Besser:

### Mit Jekyll (volle Vorschau)

```bash
bundle exec jekyll serve --livereload
```

Öffnet `http://localhost:4000/Zauberhaft/`.

## Veröffentlichung

1. Repository auf GitHub anlegen: `hesspet/Zauberhaft`
2. GitHub Pages baut beim Push **automatisch** mit Jekyll
3. In den Repository-Settings unter **Pages** den `main`-Branch als Source bestätigen
4. Die Seite ist unter `https://hesspet.github.io/Zauberhaft/` erreichbar
5. Optional: Custom Domain in den Pages-Settings konfigurieren

## Projekte und Downloads verwalten

Neue Einträge werden **ausschließlich** in den YAML-Daten angelegt — kein HTML editieren nötig:

- **Projekte:** `_data/projects.yml` (Name, Emoji, Beschreibung, Tags, URL)
- **Downloads:** `_data/downloads.yml` (Name, Emoji, Beschreibung, URL)

Nach dem Push werden Projektkarten und Download-Links automatisch aktualisiert.

## Projektstruktur

```
Zauberhaft/
├── _config.yml              # Jekyll-Konfiguration
├── _layouts/default.html    # Hauptlayout
├── _includes/               # HTML-Komponenten (nav, hero, projects, …)
├── _data/                   # YAML-Daten (projects.yml, downloads.yml)
├── assets/
│   ├── css/main.scss        # Sass-Stylesheet (Dark-Theme)
│   └── peter-hess.jpg       # Profilbild (selbst bereitstellen)
├── index.html               # Startseite (Frontmatter)
├── Gemfile                  # Ruby-Abhängigkeiten
└── LICENSE                  # Public Domain (Unlicense)
```
