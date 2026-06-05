# Projektübersicht: Zauberhaft

Stand: 05.06.2026

## Zweck

**Zauberhaft** ist die zentrale Website von Peter Heß — Startseite, Projektverteiler und Blog in einem. Alle Bereiche werden über **GitHub Pages** mit **Jekyll** aus einem einzigen Repository publiziert.

## Technischer Rahmen

- **Typ:** Statische Website mit Single-Page-Landingpage und integriertem Blog
- **Generator:** Jekyll (native GitHub-Pages-Integration)
- **Hosting:** GitHub Pages (automatischer Build + Deploy aus `main`-Branch)
- **CSS:** `main.scss` (Hauptseite) + `site.css` (Blog)
- **Templates:** Liquid — Layouts und Includes, gemeinsame Navigation
- **Daten:** YAML-Dateien für Projekte, Downloads, Blog-Navigation, Artikeltypen, Themen
- **Sprache:** Deutsch (`lang: de`, `timezone: Europe/Berlin`)
- **Blog:** Jekyll Collection `artikel` mit eigenem Layout-Set (`diymagic_*`)
- **Suche:** Clientseitig via `search.json` + `search.js`
- **CI:** GitHub Actions mit Artikelvalidierung, Jekyll-Build und Email-Benachrichtigung
- **Abhängigkeiten:** `Gemfile` mit `github-pages`-Gem (nur für lokale Entwicklung)

## Navigationsstruktur

```
┌─ Hauptnavigation (alle Seiten) ────────────────────┐
│  Start  │  Projekte  │  Downloads  │  Blog  │  Impressum  │
└────────────────────────────────────────────────────┘
┌─ Blog-Unternavigation (nur /diy-magic/) ───────────┐
│        Archiv  │  Themen  │  Suche  │  Über         │
└────────────────────────────────────────────────────┘
```

- Hauptnav-Links funktionieren von jeder Seite aus (absolute Pfade mit `relative_url`)
- Blog-Seiten nutzen einen stabilen gemeinsamen Blog-Header mit Hauptnavigation und Blog-Unternavigation
- Footer einheitlich auf allen Seiten mit Build-Datum und Zeitzone

## Projektstruktur

```
Zauberhaft/
├── _config.yml                  # Jekyll-Konfiguration (baseurl, collections, timezone)
├── index.html                   # Haupt-Landingpage (layout: default)
├── _layouts/
│   ├── default.html             # Hauptlayout — Landingpage
│   ├── diymagic_default.html    # Blog-Basislayout — mit Hauptnav + Unternav
│   ├── diymagic_home.html       # Blog-Startseite
│   ├── diymagic_artikel.html    # Einzelartikel
│   └── diymagic_page.html       # Blog-Standardseiten (Archiv, Themen, …)
├── _includes/
│   ├── head.html                # <head> für Hauptseite (Meta, CSS, View-Transition)
│   ├── nav.html                 # Hauptnavigation (alle Seiten)
│   ├── hero.html                # Intro-Bereich mit Profilbild
│   ├── projects.html            # Projektkarten aus _data/projects.yml
│   ├── downloads.html           # Download-Kapitel (Accordion) aus _data/downloads.yml
│   ├── impressum.html           # Impressum
│   ├── footer.html              # Footer (Copyright + Build-Datum)
│   ├── diymagic_header.html     # Stabiler Blog-Header mit Hauptnav + Blog-Unternav
│   ├── diymagic_footer.html     # Blog-Footer (identisch zum Hauptfooter)
│   ├── diymagic_navigation.html # Blog-Nav-Links (aus diymagic_site_navigation.yml)
│   ├── diymagic_article-card.html # Artikelkarte für Listen
│   └── diymagic_tag-list.html   # Themen-Tags
├── _data/
│   ├── projects.yml             # Projektliste
│   ├── downloads.yml            # Download-Kapitel mit Unterkapiteln
│   ├── diymagic_site_navigation.yml # Blog-Navigation (Archiv, Themen, Suche, Über)
│   ├── diymagic_article_types.yml   # Erlaubte Artikeltypen
│   └── diymagic_topics.yml      # Kontrollierte Themenliste
├── _artikel/                    # Blog-Artikel (Jekyll Collection)
│   ├── 2026-05-16-esp32-c3-trinket.md
│   ├── 2026-05-26-ds-prompter.md
│   └── 2026-05-26-…-bleprompter-….md
├── diy-magic/                   # Blog-Seiten
│   ├── index.md                 # Blog-Start
│   ├── archiv.md                # Artikel-Archiv (nach Jahren)
│   ├── themen.md                # Themen-Übersicht
│   ├── suche.md                 # Suchseite
│   ├── ueber.md                 # Über DiyMagic
│   ├── impressum.md             # Blog-Impressum
│   └── search.json              # Suchindex (Liquid-generiert)
├── assets/
│   ├── css/main.scss            # Hauptseiten-CSS (Dark-Theme)
│   ├── diy-magic/
│   │   ├── css/site.css         # Blog-CSS (Dark-Theme, Accordion)
│   │   ├── js/
│   │   │   └── search.js        # Clientseitige Suche
│   │   └── images/              # Blog-Bilder
│   └── peter-hess.jpg           # Profilbild
├── tools/                       # PowerShell-Hilfsskripte
│   ├── New-Article.ps1          # Neuen Artikel anlegen
│   ├── Validate-Articles.ps1    # Artikel-Metadaten validieren
│   ├── Build-Local.ps1          # Lokaler Jekyll-Build
│   ├── Serve-Local.ps1          # Lokaler Dev-Server
│   └── Optimize-Images.ps1      # Bilder komprimieren
├── .github/workflows/pages.yml  # CI: Build, Deploy, Email
├── HowTo.md                     # Anleitung: Artikel schreiben
├── Gemfile                      # Ruby-Abhängigkeiten
├── .gitignore
├── PROJEKTUEBERSICHT.md         # Diese Datei
├── README.md
└── LICENSE
```

## Download-Bereich

Der Download-Bereich verwendet native HTML `<details>`-Accordions mit Kapiteln und Unterkapiteln:

- **Magische Webanwendungen** → Camera Arcanum (PWA)
- **Firmware zur direkten Installation**
  - **BlePrompter** (Unterkapitel) → NSL Firmware, Peek Client APK
- **Texte** → DiyMagic Archiv

Alle Daten in `_data/downloads.yml` — neue Kapitel/Einträge nur dort anlegen.

## Veröffentlichung

1. Push nach `main` triggert GitHub Actions Workflow
2. Workflow: `Validate-Articles.ps1` → Jekyll-Build → Deploy → Email
3. Seite unter `https://hesspet.github.io/Zauberhaft/`
4. Blog unter `https://hesspet.github.io/Zauberhaft/diy-magic/`

## Email-Benachrichtigung

Nach jedem Build wird eine Status-Mail an die in den GitHub-Secrets hinterlegte Adresse gesendet. Betreff: ✅/❌ mit Build-Ergebnis, Link zum Workflow-Log.

## Lokale Entwicklung

```bash
gem install bundler
bundle install
bundle exec jekyll serve --livereload    # http://localhost:4000/Zauberhaft/
```

Ohne Jekyll: `start index.html` (ohne Layouts/Includes).

## Artikel-Workflow

1. `.\tools\New-Article.ps1 -Title "…" -Type "…" -Topics "…" -Summary "…"`
2. Artikel in `_artikel/` schreiben, Bilder nach `assets/diy-magic/images/articles/<slug>/`
3. `.\tools\Validate-Articles.ps1` vor dem Commit
4. Push → automatischer Build + Deploy

## Design-Entscheidungen

- **Kein klassisches Blogsystem** — statische Markdown-Dateien mit YAML-Frontmatter
- **Eine gemeinsame Navigation** — kein isoliertes Blog-Menü
- **Native HTML-Accordions** — kein JavaScript für Downloads
- **Clientseitige Suche** — kein Server, kein externer Dienst
- **Blog ohne View Transition API** — Blog-Navigation ist stabil aufgebaut und deaktiviert Browser-Übergänge gezielt
- **Inline dark mode hints** — `color-scheme`, `theme-color`, Inline-Styles

## Projektregeln

- Alle User-facing Strings deutsch lokalisiert
- Deutsche Umlaute direkt verwendet
- Datumsformate nach EU-Norm: `DD.MM.YYYY`
- Zeilenumbruch: CR/LF (Windows)
- Texte in UTF-8 ohne BOM
- Projekte und Downloads ausschließlich über YAML-Daten verwalten
- Artikel-Bildpfade relativ (`../../assets/diy-magic/images/…`)
