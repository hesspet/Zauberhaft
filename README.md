# Zauberhaft

Startseite, Projektverteiler und Blog von Peter Heß — statische Website mit **Jekyll**, publiziert über **GitHub Pages**.

## Auf einen Blick

- **Landingpage:** `https://hesspet.github.io/Zauberhaft/`
- **Blog:** `https://hesspet.github.io/Zauberhaft/blog/`
- **Puppen & Charaktere:** `https://hesspet.github.io/Zauberhaft/puppen/`
- **Deep Links:** jede Figur einzeln unter `https://hesspet.github.io/Zauberhaft/puppen/<figur>/`
- **Navigation:** Hauptmenü auf allen Seiten, Blog mit stabiler Unternavigation
- **Blog-Wechsel:** Blog-interne Links und Wechsel vom Blog zur Hauptseite laufen clientseitig ohne vollständigen Dokumentwechsel
- **Cache-Busting:** CSS, Blog-JavaScript und Suchindex werden mit Build-Version geladen
- **Downloads:** Kapitel-Struktur mit aufklappbaren Accordions
- **CI:** GitHub Actions — Validierung → Build → Deploy → Email

## Lokale Vorschau

Einmalig RubyInstaller mit DevKit installieren, zum Beispiel:

```powershell
winget install RubyInstallerTeam.RubyWithDevKit.3.3
```

Danach ein neues Terminal öffnen und die lokalen Projektabhängigkeiten installieren:

```powershell
.\JekyllInstallieren.bat
```

Lokale Vorschau starten:

```powershell
.\WebStarten.bat
```

Öffnet `http://127.0.0.1:4000/Zauberhaft/`.

Einmaliger Build ohne Vorschau-Server:

```powershell
.\WebBauen.bat
```

## Projekte und Downloads verwalten

Alle Einträge in den YAML-Daten — kein HTML nötig:

- **Projekte:** `_data/projects.yml` (Name, Emoji, Beschreibung, Tags, URL)
- **Downloads:** `_data/downloads.yml` (Kapitel, Unterkapitel, Einträge)
- **Puppen & Charaktere:** `_puppen/` (Steckbriefe als Markdown-Dateien, Übersicht unter `/puppen/`)

## Artikel schreiben

```powershell
.\tools\New-Article.ps1 -Title "…" -Type "Anleitung" -Topics "ESP32, Zauberei" -Summary "…"
.\tools\Validate-Articles.ps1
```

Artikel in `_artikel/`, Bilder in `assets/blog/images/articles/<slug>/`. Nach Push automatischer Deploy.

## Puppen-Steckbriefe pflegen

Jede Figur bekommt eine Markdown-Datei in `_puppen/` mit YAML-Frontmatter (Name, Kurztext, Passbild, Reihenfolge) und einem ausführlichen Steckbrief als Markdown-Body. Die Übersichtsseite `/puppen/` zeigt alle Figuren in einem responsiven Grid mit kreisrunden Passbildern. Ein Klick öffnet den Steckbrief in einem Overlay.

**Deep Links:** Jeder Steckbrief ist zusätzlich eine eigene Adresse — zum Beispiel
`https://hesspet.github.io/Zauberhaft/puppen/nasreddin/`. Diese Adresse zeigt die komplette
Puppen-Ansicht mit bereits geöffnetem Steckbrief, nicht eine einzelne Textseite. Ein Klick
auf ein Passbild schreibt die Adresse in die Adresszeile, sodass sie sich direkt kopieren
lässt. Ohne JavaScript funktionieren alle Verweise als normale Links.

Überschrift und Einleitung der Übersicht stehen in `_data/puppen.yml`.

Details siehe `puppen/HowTo.md`.

## Buy me a coffee (Unterstützen-Button)

Der Button „Buy me a coffee“ steht in allen Fußzeilen (Startseite, Downloads, Blog,
Puppen-Übersicht und Puppen-Deep-Links). Er ist vollständig zentral konfiguriert:

- **Schalter und Zieladresse:** `_data/buymeacoffee.yml` (`aktiv: true|false`, `url`)
- **Beschriftung und Vorlesetext:** `_data/texte.yml` unter `de.spenden`
- **Markup:** `_includes/buymeacoffee.html` (eigenes SVG-Symbol, kein externes Bild)
- **Aussehen:** `.kaffee-button` in `assets/css/main.scss` und `assets/blog/css/site.css`

### Was noch zu tun ist

1. `_data/buymeacoffee.yml` prüfen: `aktiv: true` setzen und die eigene Ko-fi-Adresse eintragen.
2. In Ko-fi Auszahlung (Bank oder PayPal) und Währung einrichten, damit Trinkgelder ankommen.
3. Danke-Nachricht und optional ein Spendenziel in Ko-fi hinterlegen.
4. Impressum prüfen: Hinweis auf Trinkgelder („freiwillig, keine Gegenleistung“) ergänzen,
   wenn gewünscht.
5. Lokal mit `.\WebStarten.bat` prüfen, dann committen und pushen — GitHub Pages baut
   automatisch.

## Projektstruktur
```
Zauberhaft/
├── _config.yml              # Jekyll-Konfiguration
├── _layouts/                # Layouts (Hauptseite + Blog + Puppen)
├── _includes/               # HTML-Komponenten (nav, hero, downloads, …)
├── _data/                   # YAML-Daten (projects, downloads, blog-nav, topics, puppen, texte, buymeacoffee)
├── _artikel/                # Blog-Artikel (Jekyll Collection)
├── _puppen/                 # Steckbriefe der Puppen und Charaktere (Jekyll Collection)
├── blog/                    # Blog-Seiten (Archiv, Themen, Suche, …)
├── puppen/                  # Puppen-Übersichtsseite und HowTo
├── assets/
│   ├── css/main.scss        # Hauptseiten-CSS (Dark-Theme, Kaffee-Button)
│   ├── blog/                # Blog-Assets (CSS, Suche, Navigation, Bilder)
│   └── puppen/              # Puppen-Assets (CSS, JS, Passbilder, Steckbrief-Bilder)
├── tools/                   # PowerShell-Skripte (New-Article, Validate, …)
├── .github/workflows/       # CI: Build + Deploy + Email
├── HowTo.md                 # Anleitung: Artikel schreiben
└── puppen/HowTo.md          # Anleitung: Steckbriefe pflegen
```

## Navigation und Cache

Der Blog bleibt als statische Jekyll-Seite ohne Serverlogik gebaut. Im Browser verbessert `assets/blog/js/blog-navigation.js` aber die Bedienung: Blog-interne Links und Hauptmenü-Links vom Blog zur Startseite werden per `fetch`, Stylesheet-Vorladung und History API geladen. Ohne JavaScript funktionieren alle Links normal als klassische Seitenaufrufe.

Asset-URLs enthalten eine Build-Version, damit Browser nach einem Deploy nicht versehentlich alte CSS-, JavaScript- oder Suchindex-Dateien weiterverwenden.
