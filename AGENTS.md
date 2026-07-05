# Zauberhaft — AGENTS.md

Jekyll-Website (GitHub Pages). Sprache: Deutsch. Kein Node/npm — Ruby+Bundler+Gems.

## codebase-memory

Projekt ist über codebase-memory indexiert (Name: `C-dev-Zauberhaft`). Vor Such-/Änderungsfragen immer `search_graph` oder `trace_path` nutzen statt grep.

## Commands

```powershell
.\JekyllInstallieren.bat          # Einmalig: `bundle install` mit vendor/bundle
.\WebStarten.bat                   # Lokale Vorschau → http://127.0.0.1:4000/Zauberhaft/
.\WebBauen.bat                     # Einmaliger Build ohne Server
.\tools\Validate-Articles.ps1     # Artikelschema prüfen (vor Commit!)
.\tools\New-Article.ps1 -Title "…" -Type "…" -Topics "…" -Summary "…"
```

GitHub Actions CI: `.github/workflows/pages.yml` — validate → build → deploy → email.

## Content-Arbeit

- **Artikel:** Markdown in `_artikel/`, Dateiname `YYYY-MM-DD-slug.md`, YAML-Frontmatter mit `title`, `date`, `updated`, `type`, `topics`, `summary`, `status`. Validierung via `Validate-Articles.ps1` prüft Schema, Typen, Themen, BOM, Bildpfade.
- **Puppen:** Markdown in `_puppen/`, Frontmatter: `name`, `kurztext`, `passbild`, `reihenfolge`. Bilder im Body zwingend als `<img src="{{ '/assets/puppen/steckbriefe/...' | relative_url }}">` (kein Markdown `![]()`).
- **Projekte/Downloads/Navigation:** YAML-Dateien in `_data/` — kein HTML.
- **Artikel-Bildpfade:** in Quellen Typora-kompatibel `../assets/blog/images/articles/<slug>/…`; `blog_artikel` schreibt sie beim Rendern auf `../../assets/...` um.
- **Puppen-Bildpfade:** absolut `/assets/puppen/…` (mit `relative_url` im Template)
- **Artikel-Umbenennung:** `BlogArtikelBearbeiten.py` (Tk-GUI) passt Dateiname, Bildverzeichnis und Bildreferenzen an.

## Konventionen

- UTF-8 **ohne BOM** (Jekyll erkennt BOM nicht im YAML-Header)
- CR/LF (Windows), Umlaute direkt, Datum `DD.MM.YYYY`
- Dateinamen-Slug: Kleinbuchstaben, Bindestriche, `ä→ae ö→oe ü→ue ß→ss`
- Asset-URLs mit `?v=Build-Version` (Cache-Busting)
- `vendor/`, `Gemfile.lock`, `__pycache__`, `graphify-out/` in `.gitignore`

## GUI-Tools

`BlogArtikelAnlegen.py` / `BlogArtikelBearbeiten.py` — Tkinter-GUIs, rufen `tools/New-Article.ps1` auf bzw. editieren `_artikel/`-Dateien direkt.
