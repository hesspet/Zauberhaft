# Projektübersicht: Zauberhaft

Stand: 05.06.2026

## Zweck

**Zauberhaft** ist die Startseite und der Verteiler für Peter Heß' DIY-Projekte rund um das Zaubern. Die Seite dient als zentrale Anlaufstelle (Landing Page) und wird über **GitHub Pages** mit **Jekyll** publiziert.

## Technischer Rahmen

- **Typ:** Statische Single-Page-Website
- **Generator:** Jekyll (native GitHub-Pages-Integration)
- **Hosting:** GitHub Pages (automatischer Build aus dem `main`-Branch)
- **CSS:** Sass (`assets/css/main.scss`), von Jekyll kompiliert
- **Templates:** Liquid — Layouts und Includes
- **Daten:** `_data/projects.yml` und `_data/downloads.yml`
- **Sprache:** Deutsch (`lang: de`)
- **Abhängigkeiten:** `Gemfile` mit `github-pages`-Gem (nur für lokale Entwicklung)

## Projektstruktur

```
Zauberhaft/
├── _config.yml              # Jekyll-Konfiguration (baseurl, Plugins, Sass)
├── _layouts/
│   └── default.html         # Hauptlayout — ruft alle Includes auf
├── _includes/
│   ├── head.html            # <head> mit Metadaten, CSS-Link, Feed/SEO
│   ├── nav.html             # Fixierte Top-Navigation
│   ├── hero.html            # Intro-Bereich mit Profilbild und Text
│   ├── projects.html        # Projektkarten-Grid aus _data/projects.yml
│   ├── downloads.html       # Download-Links aus _data/downloads.yml
│   ├── impressum.html       # Impressum nach § 55 RStV
│   └── footer.html          # Footer mit Copyright (dynamisches Jahr)
├── _data/
│   ├── projects.yml         # Projektliste (Name, Emoji, Beschreibung, Tags, URL)
│   └── downloads.yml        # Download-Links (Name, Emoji, Beschreibung, URL)
├── assets/
│   ├── css/
│   │   └── main.scss        # Komplettes CSS (Dark-Theme, responsiv)
│   ├── README.md            # Hinweise zum Profilbild
│   └── peter-hess.jpg       # Profilbild (selbst bereitstellen)
├── index.html               # Einstiegsseite (Frontmatter + layout: default)
├── Gemfile                  # Ruby-Abhängigkeiten für lokale Entwicklung
├── .gitignore               # _site/, .jekyll-cache/, Gemfile.lock, vendor/
├── PROJEKTUEBERSICHT.md     # Diese Datei
├── README.md                # Schnelleinstieg
└── LICENSE                  # Public Domain (Unlicense)
```

## Seitenstruktur

| Bereich | ID | Quelle |
|---------|-----|--------|
| Navigation | `nav` | `_includes/nav.html` |
| Intro | `#intro` | `_includes/hero.html` |
| Projekte | `#projekte` | `_includes/projects.html` + `_data/projects.yml` |
| Downloads | `#downloads` | `_includes/downloads.html` + `_data/downloads.yml` |
| Impressum | `#impressum` | `_includes/impressum.html` |
| Footer | `footer` | `_includes/footer.html` |

## Automatismen (durch Jekyll)

- **Projektkarten** werden automatisch aus `_data/projects.yml` generiert — neues Projekt = ein YAML-Eintrag
- **Download-Links** werden automatisch aus `_data/downloads.yml` generiert
- **Copyright-Jahr** wird dynamisch aus `site.time` berechnet
- **CSS** wird von Jekylls Sass-Compiler minifiziert (`style: compressed`)
- **Sitemap** und **RSS-Feed** über `jekyll-sitemap` und `jekyll-feed`
- **`relative_url`-Filter** sorgt für korrekte Pfade unabhängig von `baseurl`

## Veröffentlichung

1. Repository auf GitHub anlegen: `hesspet/Zauberhaft`
2. GitHub Pages ist **standardmäßig aktiv** — Jekyll baut beim Push automatisch
3. In den Repository-Settings unter **Pages** prüfen, dass `main`-Branch ausgewählt ist
4. Die Seite ist unter `https://hesspet.github.io/Zauberhaft/` erreichbar
5. Der Build-Status ist im Tab **Actions** einsehbar

## Lokale Entwicklung (optional)

```bash
# Einmalig
gem install bundler
bundle install

# Entwicklungsserver (mit Live-Reload)
bundle exec jekyll serve --livereload

# Einmaliger Build
bundle exec jekyll build
```

## Vorgestellte Projekte

- Nasreddin's Secret Listener — ESP32 „Which Hand“-Detektor
- Nasreddin's Camera Arcanum — PWA für magische Foto-Effekte
- Nasreddin's Simple Peek Client 2 — Android BLE-Prompter-App
- Nasreddin's Magic Toolbox — Zauber-Helfer fürs Smartphone
- Nasreddin's Magic Card Identifier — Spielkarten-Erkennung
- DiyMagic — Statisches Artikelarchiv

## Projektregeln

- Alle User-facing Strings sind deutsch lokalisiert
- Deutsche Umlaute werden direkt verwendet
- Datumsformate nach EU-Norm: `DD.MM.YYYY`
- Zeilenumbruch: CR/LF (Windows)
- Texte in UTF-8 ohne BOM
- Projekte und Downloads ausschließlich über die YAML-Daten verwalten
