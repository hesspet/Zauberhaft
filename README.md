# Zauberhaft

Startseite, Projektverteiler und Blog von Peter Heß — statische Website mit **Jekyll**, publiziert über **GitHub Pages**.

## Auf einen Blick

- **Landingpage:** `https://hesspet.github.io/Zauberhaft/`
- **Blog:** `https://hesspet.github.io/Zauberhaft/diy-magic/`
- **Navigation:** Hauptmenü auf allen Seiten, Blog mit Unternavigation
- **Downloads:** Kapitel-Struktur mit aufklappbaren Accordions
- **CI:** GitHub Actions — Validierung → Build → Deploy → Email

## Lokale Vorschau

```bash
bundle exec jekyll serve --livereload
```

Öffnet `http://localhost:4000/Zauberhaft/`.

## Projekte und Downloads verwalten

Alle Einträge in den YAML-Daten — kein HTML nötig:

- **Projekte:** `_data/projects.yml` (Name, Emoji, Beschreibung, Tags, URL)
- **Downloads:** `_data/downloads.yml` (Kapitel, Unterkapitel, Einträge)

## Artikel schreiben

```powershell
.\tools\New-Article.ps1 -Title "…" -Type "Anleitung" -Topics "ESP32, Zauberei" -Summary "…"
.\tools\Validate-Articles.ps1
```

Artikel in `_artikel/`, Bilder in `assets/diy-magic/images/articles/<slug>/`. Nach Push automatischer Deploy.

## Projektstruktur

```
Zauberhaft/
├── _config.yml              # Jekyll-Konfiguration
├── _layouts/                # Layouts (Hauptseite + Blog)
├── _includes/               # HTML-Komponenten (nav, hero, downloads, …)
├── _data/                   # YAML-Daten (projects, downloads, blog-nav, topics)
├── _artikel/                # Blog-Artikel (Jekyll Collection)
├── diy-magic/               # Blog-Seiten (Archiv, Themen, Suche, …)
├── assets/
│   ├── css/main.scss        # Hauptseiten-CSS (Dark-Theme)
│   └── diy-magic/           # Blog-Assets (CSS, JS, Bilder)
├── tools/                   # PowerShell-Skripte (New-Article, Validate, …)
├── .github/workflows/       # CI: Build + Deploy + Email
└── HowTo.md                 # Anleitung: Artikel schreiben
```
