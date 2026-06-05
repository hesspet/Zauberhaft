# Projektübersicht: Zauberhaft

Stand: 05.06.2026

## Zweck

**Zauberhaft** ist die Startseite und der Verteiler für Peter Heß' DIY-Projekte rund um das Zaubern. Die Seite dient als zentrale Anlaufstelle (Landing Page) und wird über **GitHub Pages** publiziert.

## Technischer Rahmen

- **Typ:** Statische Single-Page-Website
- **Hosting:** GitHub Pages (aus dem `main`-Branch)
- **Dateien:** `index.html` (HTML5 + eingebettetes CSS), `assets/` (Bilder)
- **Abhängigkeiten:** Keine — kein Framework, kein Build-Schritt, keine externen CSS/JS-Ressourcen
- **Design:** Dark-Theme, responsiv, system fonts
- **Sprache:** Deutsch (lang="de")

## Seitenstruktur

| Bereich | ID | Inhalt |
|---------|-----|--------|
| Navigation | `nav` | Fixierte Top-Leiste mit Smooth-Scroll-Links |
| Intro | `#intro` | Profilbild + Name + Tagline + Einleitungstext |
| Projekte | `#projekte` | Sechs Projektkarten mit Beschreibung, Tags und GitHub-Links |
| Downloads | `#downloads` | Vier Download-Links zu Releases und PWAs |
| Impressum | `#impressum` | Rechtliche Angaben nach § 55 RStV |

## Veröffentlichung

1. Repository auf GitHub anlegen: `hesspet/Zauberhaft`
2. In den Repository-Settings unter **Pages** den `main`-Branch als Source auswählen
3. Die Seite ist dann unter `https://hesspet.github.io/Zauberhaft/` erreichbar
4. Optional: Custom Domain `zauberhaft.dev` in den Pages-Settings konfigurieren

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
