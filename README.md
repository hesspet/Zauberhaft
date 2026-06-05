# Zauberhaft

Startseite, Projektverteiler und Blog von Peter Heß — statische Website mit **Jekyll**, publiziert über **GitHub Pages**.

## Auf einen Blick

- **Landingpage:** `https://hesspet.github.io/Zauberhaft/`
- **Blog:** `https://hesspet.github.io/Zauberhaft/blog/`
- **Navigation:** Hauptmenü auf allen Seiten, Blog mit stabiler Unternavigation
- **Blog-Wechsel:** Blog-interne Links und Wechsel vom Blog zur Hauptseite laufen clientseitig ohne vollständigen Dokumentwechsel
- **Cache-Busting:** CSS, Blog-JavaScript und Suchindex werden mit Build-Version geladen
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

Artikel in `_artikel/`, Bilder in `assets/blog/images/articles/<slug>/`. Nach Push automatischer Deploy.

## Projektstruktur

```
Zauberhaft/
├── _config.yml              # Jekyll-Konfiguration
├── _layouts/                # Layouts (Hauptseite + Blog)
├── _includes/               # HTML-Komponenten (nav, hero, downloads, …)
├── _data/                   # YAML-Daten (projects, downloads, blog-nav, topics)
├── _artikel/                # Blog-Artikel (Jekyll Collection)
├── blog/               # Blog-Seiten (Archiv, Themen, Suche, …)
├── assets/
│   ├── css/main.scss        # Hauptseiten-CSS (Dark-Theme)
│   └── blog/           # Blog-Assets (CSS, Suche, clientseitige Navigation, Bilder)
├── tools/                   # PowerShell-Skripte (New-Article, Validate, …)
├── .github/workflows/       # CI: Build + Deploy + Email
└── HowTo.md                 # Anleitung: Artikel schreiben
```

## Navigation und Cache

Der Blog bleibt als statische Jekyll-Seite ohne Serverlogik gebaut. Im Browser verbessert `assets/blog/js/blog-navigation.js` aber die Bedienung: Blog-interne Links und Hauptmenü-Links vom Blog zur Startseite werden per `fetch`, Stylesheet-Vorladung und History API geladen. Ohne JavaScript funktionieren alle Links normal als klassische Seitenaufrufe.

Asset-URLs enthalten eine Build-Version, damit Browser nach einem Deploy nicht versehentlich alte CSS-, JavaScript- oder Suchindex-Dateien weiterverwenden.
