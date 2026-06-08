"""
BlogArtikelBearbeiten – GUI zum Bearbeiten eines Blog-Artikels.
Verwendung: pythonw BlogArtikelBearbeiten.py  (kein Konsolenfenster)
"""
from __future__ import annotations

import os
import re
import shutil
import subprocess
import yaml
from datetime import date, datetime
from pathlib import Path
from tkinter import Tk, Frame, Label, Entry, Button, Text, StringVar, BooleanVar
from tkinter import ttk
from tkinter.messagebox import showinfo, showerror, askyesno, showwarning

PROJECT_ROOT = Path(__file__).resolve().parent
ARTIKEL_VERZEICHNIS = PROJECT_ROOT / "_artikel"
BILDER_VERZEICHNIS = PROJECT_ROOT / "assets" / "blog" / "images" / "articles"

ARTIKELTYPEN: list[str] = []
THEMEN: list[str] = []


# ---------------------------------------------------------------------------
# Hilfsfunktionen
# ---------------------------------------------------------------------------

def lade_referenzdaten() -> None:
    """Liest erlaubte Artikeltypen und Themen aus den YAML-Dateien."""
    global ARTIKELTYPEN, THEMEN

    pfad_typen = PROJECT_ROOT / "_data" / "blog_article_types.yml"
    if pfad_typen.is_file():
        with open(pfad_typen, encoding="utf-8") as datei:
            ARTIKELTYPEN = yaml.safe_load(datei) or []

    pfad_themen = PROJECT_ROOT / "_data" / "blog_topics.yml"
    if pfad_themen.is_file():
        with open(pfad_themen, encoding="utf-8") as datei:
            THEMEN = yaml.safe_load(datei) or []


def slug_erzeugen(titel: str) -> str:
    """Erzeugt aus einem Titel einen URL-Slug (wie New-Article.ps1)."""
    slug = titel.lower()
    slug = slug.replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("ß", "ss")
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    slug = re.sub(r"-+", "-", slug)
    return slug.strip("-")


def slug_aus_dateiname(dateiname: str) -> str:
    """Extrahiert den Slug aus einem Dateinamen wie '2026-05-16-esp32-c3-trinket.md'."""
    name_ohne_endung = Path(dateiname).stem
    # Entferne das Datum-Präfix (YYYY-MM-DD-), also 11 Zeichen
    if re.match(r"^\d{4}-\d{2}-\d{2}-", name_ohne_endung):
        return name_ohne_endung[11:]
    return name_ohne_endung


def datum_normalisieren(datum_str: str) -> str:
    """Stellt sicher, dass ein Datums-String das Format YYYY-MM-DD HH:MM hat.
    Fehlt die Uhrzeit, wird 00:00 angehängt."""
    if not datum_str:
        return datum_str
    datum_str = datum_str.strip()
    if re.match(r"^\d{4}-\d{2}-\d{2}$", datum_str):
        return datum_str + " 00:00"
    return datum_str


def artikel_auflisten() -> list[tuple[str, str, str]]:
    """Liefert Liste von (dateiname, titel, datum) aller Artikel."""
    ergebnis: list[tuple[str, str, str]] = []
    if not ARTIKEL_VERZEICHNIS.is_dir():
        return ergebnis

    for dateipfad in sorted(ARTIKEL_VERZEICHNIS.glob("*.md")):
        try:
            meta, _ = frontmatter_lesen(dateipfad)
            titel = meta.get("title", dateipfad.stem)
            artikel_datum = meta.get("date", "")
        except Exception:
            titel = dateipfad.stem
            artikel_datum = ""
        ergebnis.append((dateipfad.name, titel, artikel_datum))

    return ergebnis


def frontmatter_lesen(dateipfad: Path) -> tuple[dict, str]:
    """Liest Frontmatter (dict) und Body (str) aus einer Artikel-Markdown-Datei."""
    with open(dateipfad, encoding="utf-8") as datei:
        inhalt = datei.read()

    teile = inhalt.split("---", 2)
    if len(teile) < 3:
        raise ValueError("Kein gültiges Frontmatter gefunden (--- fehlt).")

    yaml_text = teile[1].strip()
    meta = yaml.safe_load(yaml_text) or {}
    body = teile[2]
    return meta, body


def frontmatter_erzeugen(meta: dict) -> str:
    """Erzeugt einen Frontmatter-Block aus einem dict im projektüblichen Stil."""
    zeilen = ["---"]
    zeilen.append("layout: blog_artikel")

    titel = str(meta.get("title", "")).replace('"', '\\"')
    zeilen.append(f'title: "{titel}"')

    datum = meta.get("date", "")
    zeilen.append(f"date: {datum}")

    aktualisiert = meta.get("updated", "")
    zeilen.append(f"updated: {aktualisiert if aktualisiert else ''}")

    typ = str(meta.get("type", "")).replace('"', '\\"')
    zeilen.append(f'type: "{typ}"')

    zeilen.append("topics:")
    for thema in meta.get("topics", []):
        zeilen.append(f"  - {thema}")

    zusammenfassung = str(meta.get("summary", "")).replace('"', '\\"')
    zeilen.append(f'summary: "{zusammenfassung}"')

    hero = meta.get("hero", "")
    zeilen.append(f"hero: {hero if hero else ''}")

    status = meta.get("status", "entwurf")
    zeilen.append(f'status: "{status}"')

    schwierigkeit = meta.get("difficulty", "")
    zeilen.append(f"difficulty: {schwierigkeit if schwierigkeit else ''}")

    zeilen.append("---")
    return "\n".join(zeilen) + "\n"


def artikel_schreiben(dateipfad: Path, meta: dict, body: str) -> None:
    """Schreibt den Artikel (Frontmatter + Body) als UTF-8 ohne BOM."""
    fm_block = frontmatter_erzeugen(meta)
    inhalt = fm_block + body

    with open(dateipfad, "w", encoding="utf-8", newline="\n") as datei:
        datei.write(inhalt)


def bildreferenzen_ersetzen(text: str, alter_slug: str, neuer_slug: str) -> tuple[str, int]:
    """Ersetzt alle Bildpfade, die den alten Slug enthalten, durch den neuen Slug.
    Liefert (neuer_text, anzahl_ersetzungen)."""
    # Muster: articles/<alter_slug>/ in Pfaden
    # Matcht in Markdown-Bildern: ![alt](path) und HTML: src="path"
    muster = re.compile(r"(articles/)(" + re.escape(alter_slug) + r")(/)")
    neuer_text, anzahl = muster.subn(r"\1" + neuer_slug + r"\3", text)
    return neuer_text, anzahl


# ---------------------------------------------------------------------------
# GUI
# ---------------------------------------------------------------------------

class ArtikelBearbeitenGui:
    """Hauptfenster der Artikel-Bearbeitungs-GUI."""

    def __init__(self, root: Tk) -> None:
        self.root = root
        self.root.title("Blog-Artikel bearbeiten")
        self.root.resizable(width=True, height=True)

        # Zustand
        self.aktueller_dateiname: str = ""
        self.aktueller_dateipfad: Path | None = None
        self.metadaten: dict = {}
        self.body: str = ""
        self.aenderungen_vorhanden: bool = False
        self.artikel_liste: list[tuple[str, str, str]] = []

        # Variablen
        self.auswahl_var = StringVar()
        self.titel_var = StringVar()
        self.typ_var = StringVar()
        self.themen_var = StringVar()
        self.zusammenfassung_text: Text | None = None
        self.status_var = StringVar()
        self.updated_var = BooleanVar()
        self.neuer_titel_var = StringVar()
        self.slug_vorschau_var = StringVar()

        # Statuszeile
        self.status_label: Label | None = None

        self._gui_aufbauen()
        self._artikel_liste_laden()

    # ------------------------------------------------------------------
    # GUI-Aufbau
    # ------------------------------------------------------------------

    def _gui_aufbauen(self) -> None:
        """Baut das gesamte GUI-Layout auf."""
        haupt_frame = Frame(self.root)
        haupt_frame.pack(fill="both", expand=True, padx=12, pady=12)

        self._abschnitt_auswahl(haupt_frame)
        self._abschnitt_metadaten(haupt_frame)
        self._abschnitt_umbenennen(haupt_frame)
        self._abschnitt_aktionen(haupt_frame)

    def _abschnitt_auswahl(self, parent: Frame) -> None:
        """Artikel-Auswahl (Dropdown + Laden)."""
        frame = Frame(parent)
        frame.pack(fill="x", pady=(0, 8))

        Label(frame, text="Artikel:", anchor="w").pack(anchor="w")

        auswahl_frame = Frame(frame)
        auswahl_frame.pack(fill="x", pady=(2, 0))

        self.auswahl_combo = ttk.Combobox(
            auswahl_frame, textvariable=self.auswahl_var, state="readonly", width=80
        )
        self.auswahl_combo.pack(side="left", fill="x", expand=True)
        self.auswahl_combo.bind("<<ComboboxSelected>>", self._artikel_geladen)

        Button(auswahl_frame, text="Laden", command=self._artikel_laden, width=10).pack(
            side="left", padx=(8, 0)
        )

    def _abschnitt_metadaten(self, parent: Frame) -> None:
        """Metadaten-Bearbeitungsbereich."""
        container = Frame(parent, relief="groove", borderwidth=1)
        container.pack(fill="x", pady=(0, 8))

        Label(
            container, text="── Metadaten ──", anchor="w", fg="#8888cc"
        ).pack(fill="x", padx=8, pady=(6, 4))

        inner = Frame(container)
        inner.pack(fill="x", padx=8, pady=(0, 8))

        # Titel
        Label(inner, text="Titel:", anchor="w").pack(fill="x")
        self.titel_entry = Entry(inner, textvariable=self.titel_var, width=80)
        self.titel_entry.pack(fill="x", pady=(0, 6))
        self.titel_var.trace_add("write", self._aenderung_markieren)

        # Typ
        Label(inner, text="Artikeltyp:", anchor="w").pack(fill="x")
        self.typ_combo = ttk.Combobox(
            inner, textvariable=self.typ_var, values=ARTIKELTYPEN, state="readonly", width=30
        )
        self.typ_combo.pack(anchor="w", pady=(0, 6))
        self.typ_combo.bind("<<ComboboxSelected>>", self._aenderung_markieren)

        # Themen
        Label(inner, text="Themen (kommagetrennt):", anchor="w").pack(fill="x")
        self.themen_entry = Entry(inner, textvariable=self.themen_var, width=80)
        self.themen_entry.pack(fill="x", pady=(0, 2))
        self.themen_var.trace_add("write", self._aenderung_markieren)

        if THEMEN:
            ref_frame = Frame(inner)
            ref_frame.pack(fill="x", pady=(0, 6))
            Label(ref_frame, text="Verfügbar:", anchor="w", fg="gray").pack(side="left")
            Label(
                ref_frame,
                text=", ".join(THEMEN),
                anchor="w",
                fg="gray",
                wraplength=580,
                justify="left",
            ).pack(side="left", padx=(6, 0))

        # Zusammenfassung
        Label(inner, text="Zusammenfassung:", anchor="w").pack(fill="x")
        self.zusammenfassung_text = Text(inner, height=3, width=70, wrap="word")
        self.zusammenfassung_text.pack(fill="x", pady=(0, 6))
        self.zusammenfassung_text.bind("<KeyRelease>", self._aenderung_markieren)

        # Status
        status_frame = Frame(inner)
        status_frame.pack(fill="x", pady=(0, 6))

        Label(status_frame, text="Status:", anchor="w").pack(side="left")
        self.status_combo = ttk.Combobox(
            status_frame,
            textvariable=self.status_var,
            values=["entwurf", "fertig"],
            state="readonly",
            width=12,
        )
        self.status_combo.pack(side="left", padx=(6, 20))
        self.status_combo.bind("<<ComboboxSelected>>", self._aenderung_markieren)

        # updated-Checkbox
        self.updated_check = ttk.Checkbutton(
            status_frame, text="Heute aktualisieren", variable=self.updated_var
        )
        self.updated_check.pack(side="left")
        self.updated_var.trace_add("write", self._aenderung_markieren)

    def _abschnitt_umbenennen(self, parent: Frame) -> None:
        """Umbenennen-Bereich."""
        container = Frame(parent, relief="groove", borderwidth=1)
        container.pack(fill="x", pady=(0, 8))

        Label(
            container, text="── Umbenennen ──", anchor="w", fg="#8888cc"
        ).pack(fill="x", padx=8, pady=(6, 4))

        inner = Frame(container)
        inner.pack(fill="x", padx=8, pady=(0, 8))

        Label(inner, text="Neuer Titel:", anchor="w").pack(fill="x")
        self.neuer_titel_entry = Entry(inner, textvariable=self.neuer_titel_var, width=80)
        self.neuer_titel_entry.pack(fill="x", pady=(0, 2))
        self.neuer_titel_var.trace_add("write", self._slug_vorschau_aktualisieren)

        Label(inner, text="Slug-Vorschau:", anchor="w").pack(fill="x")
        self.slug_label = Label(inner, textvariable=self.slug_vorschau_var, anchor="w", fg="gray")
        self.slug_label.pack(fill="x", pady=(0, 6))

        Button(
            inner,
            text="Umbenennen & Bildpfade anpassen",
            command=self._umbenennen,
            width=35,
            height=2,
        ).pack(anchor="w")

    def _abschnitt_aktionen(self, parent: Frame) -> None:
        """Aktions-Buttons (Speichern / Abbrechen) und Statuszeile."""
        frame = Frame(parent)
        frame.pack(fill="x")

        self.status_label = Label(frame, text="", anchor="w", fg="gray")
        self.status_label.pack(fill="x", pady=(0, 6))

        button_frame = Frame(frame)
        button_frame.pack(fill="x")

        Button(
            button_frame,
            text="Änderungen speichern",
            command=self._speichern,
            width=22,
            height=2,
        ).pack(side="left")
        Button(
            button_frame,
            text="Abbrechen",
            command=self.root.destroy,
            width=10,
            height=2,
        ).pack(side="left", padx=(8, 0))

    # ------------------------------------------------------------------
    # Event-Handler
    # ------------------------------------------------------------------

    def _aenderung_markieren(self, *args: object) -> None:
        """Markiert, dass Änderungen zum Speichern vorliegen."""
        self.aenderungen_vorhanden = True

    def _slug_vorschau_aktualisieren(self, *args: object) -> None:
        """Aktualisiert die Slug-Vorschau beim Tippen."""
        titel = self.neuer_titel_var.get().strip()
        if titel:
            self.slug_vorschau_var.set(slug_erzeugen(titel))
        else:
            self.slug_vorschau_var.set("")

    def _artikel_liste_laden(self) -> None:
        """Befüllt das Artikel-Dropdown mit allen Artikeln."""
        self.artikel_liste = artikel_auflisten()

        eintraege = []
        for dateiname, titel, datum in self.artikel_liste:
            anzeige = f"{titel}  ({dateiname})"
            eintraege.append(anzeige)

        self.auswahl_combo["values"] = eintraege
        if eintraege:
            self.auswahl_combo.current(0)

    def _artikel_geladen(self, event: object = None) -> None:
        """Wird ausgelöst, wenn ein Artikel im Dropdown ausgewählt wird."""
        self._artikel_laden()

    def _artikel_laden(self) -> None:
        """Lädt den ausgewählten Artikel und befüllt die Felder."""
        index = self.auswahl_combo.current()
        if index < 0 or index >= len(self.artikel_liste):
            return

        dateiname, _, _ = self.artikel_liste[index]
        dateipfad = ARTIKEL_VERZEICHNIS / dateiname

        if not dateipfad.is_file():
            showerror("Fehler", f"Artikel nicht gefunden:\n{dateipfad}")
            return

        try:
            self.metadaten, self.body = frontmatter_lesen(dateipfad)
        except Exception as fehler:
            showerror("Fehler", f"Artikel konnte nicht geladen werden:\n{fehler}")
            return

        self.aktueller_dateiname = dateiname
        self.aktueller_dateipfad = dateipfad
        self.aenderungen_vorhanden = False

        # Felder befüllen
        self.titel_var.set(str(self.metadaten.get("title", "")))
        self.typ_var.set(str(self.metadaten.get("type", "")))
        themen = self.metadaten.get("topics", [])
        if isinstance(themen, list):
            self.themen_var.set(", ".join(str(t) for t in themen))
        else:
            self.themen_var.set(str(themen))

        self.zusammenfassung_text.delete("1.0", "end")
        self.zusammenfassung_text.insert("1.0", str(self.metadaten.get("summary", "")))

        status = self.metadaten.get("status", "entwurf")
        self.status_var.set(status if status else "entwurf")
        self.updated_var.set(False)

        # Neuer-Titel-Feld mit aktuellem Titel vorbelegen
        self.neuer_titel_var.set(str(self.metadaten.get("title", "")))
        self.slug_vorschau_var.set(slug_erzeugen(str(self.metadaten.get("title", ""))))

        self._status_setzen(f"Artikel geladen: {dateiname}")

    def _metadaten_aus_gui_lesen(self) -> dict:
        """Liest die aktuellen GUI-Werte und gibt ein Metadaten-dict zurück."""
        meta = dict(self.metadaten)  # Kopie

        meta["title"] = self.titel_var.get().strip()
        meta["type"] = self.typ_var.get().strip()
        meta["summary"] = self.zusammenfassung_text.get("1.0", "end-1c").strip()
        meta["status"] = self.status_var.get().strip()

        # Themen parsen
        themen_roh = self.themen_var.get().strip()
        if themen_roh:
            meta["topics"] = [t.strip() for t in themen_roh.split(",") if t.strip()]
        else:
            meta["topics"] = []

        # updated
        if self.updated_var.get():
            meta["updated"] = datetime.now().strftime("%Y-%m-%d %H:%M")

        return meta

    def _validieren(self, meta: dict) -> list[str]:
        """Validiert die Metadaten. Liefert Liste von Fehlermeldungen."""
        fehler: list[str] = []
        if not meta.get("title"):
            fehler.append("- Titel ist erforderlich.")
        if not meta.get("type"):
            fehler.append("- Artikeltyp ist erforderlich.")
        if meta.get("type") and meta["type"] not in ARTIKELTYPEN:
            fehler.append(f"- Unbekannter Artikeltyp: {meta['type']}")
        if not meta.get("topics"):
            fehler.append("- Mindestens ein Thema ist erforderlich.")
        for thema in meta.get("topics", []):
            if thema not in THEMEN:
                fehler.append(f"- Unbekanntes Thema: {thema}")
        if not meta.get("summary"):
            fehler.append("- Zusammenfassung ist erforderlich.")
        return fehler

    def _speichern(self) -> None:
        """Speichert die aktuellen Metadaten-Änderungen."""
        if not self.aktueller_dateipfad:
            showerror("Fehler", "Kein Artikel geladen.")
            return

        meta = self._metadaten_aus_gui_lesen()
        fehler = self._validieren(meta)
        if fehler:
            showerror("Eingabefehler", "Bitte korrigieren:\n\n" + "\n".join(fehler))
            return

        # Datumsfelder normalisieren (Uhrzeit ergänzen falls nötig)
        if meta.get("date"):
            meta["date"] = datum_normalisieren(meta["date"])
        if meta.get("updated"):
            meta["updated"] = datum_normalisieren(meta["updated"])

        # Body: aktualisiere title in der ersten H1, falls vorhanden
        body = self.body
        alter_titel = self.metadaten.get("title", "")
        neuer_titel = meta.get("title", "")
        if alter_titel and neuer_titel and alter_titel != neuer_titel:
            # Ersetze die erste #-Überschrift, die dem alten Titel ähnelt
            body = re.sub(
                r"^#\s+" + re.escape(alter_titel) + r"\s*$",
                "# " + neuer_titel,
                body,
                count=1,
                flags=re.MULTILINE,
            )

        try:
            artikel_schreiben(self.aktueller_dateipfad, meta, body)
        except Exception as fehler:
            showerror("Fehler", f"Artikel konnte nicht gespeichert werden:\n{fehler}")
            return

        # Zustand aktualisieren
        self.metadaten = meta
        self.body = body
        self.aenderungen_vorhanden = False
        self.updated_var.set(False)

        self._status_setzen("Gespeichert.", "green")
        showinfo("Gespeichert", "Die Änderungen wurden gespeichert.")

        # Artikelliste neu laden (Titel könnte sich geändert haben)
        self._artikel_liste_laden()

    def _umbenennen(self) -> None:
        """Benennt den Artikel um: Datei, Bildverzeichnis, Bildreferenzen."""
        if not self.aktueller_dateipfad:
            showerror("Fehler", "Kein Artikel geladen.")
            return

        neuer_titel = self.neuer_titel_var.get().strip()
        if not neuer_titel:
            showerror("Eingabefehler", "Neuer Titel ist erforderlich.")
            return

        neuer_slug = slug_erzeugen(neuer_titel)
        if not neuer_slug:
            showerror("Eingabefehler", "Aus dem neuen Titel konnte kein gültiger Slug erzeugt werden.")
            return

        alter_slug = slug_aus_dateiname(self.aktueller_dateiname)
        if alter_slug == neuer_slug:
            showinfo("Hinweis", "Der neue Titel ergibt denselben Slug. Keine Umbenennung nötig.")
            return

        # Datumspräfix aus altem Dateinamen extrahieren
        datum_praefix = ""
        altes_stem = Path(self.aktueller_dateiname).stem
        match = re.match(r"^(\d{4}-\d{2}-\d{2})-", altes_stem)
        if match:
            datum_praefix = match.group(1)

        neuer_dateiname = f"{datum_praefix}-{neuer_slug}.md"
        neuer_dateipfad = ARTIKEL_VERZEICHNIS / neuer_dateiname
        altes_bildverzeichnis = BILDER_VERZEICHNIS / alter_slug
        neues_bildverzeichnis = BILDER_VERZEICHNIS / neuer_slug

        # Prüfen, ob Zieldatei bereits existiert
        if neuer_dateipfad.exists() and neuer_dateipfad != self.aktueller_dateipfad:
            showerror(
                "Fehler",
                f"Eine Datei mit diesem Namen existiert bereits:\n{neuer_dateiname}",
            )
            return

        # Prüfen, ob Zielverzeichnis bereits existiert
        if neues_bildverzeichnis.exists():
            showerror(
                "Fehler",
                f"Ein Bildverzeichnis mit diesem Namen existiert bereits:\n{neues_bildverzeichnis}",
            )
            return

        # Zusammenfassung der Änderungen
        meldung = (
            f"Folgende Änderungen werden durchgeführt:\n\n"
            f"• Datei umbenennen:\n"
            f"  {self.aktueller_dateiname}\n"
            f"  → {neuer_dateiname}\n\n"
            f"• Bildreferenzen im Artikel ersetzen:\n"
            f"  articles/{alter_slug}/  →  articles/{neuer_slug}/\n"
        )
        if altes_bildverzeichnis.is_dir():
            meldung += (
                f"\n• Bildverzeichnis umbenennen:\n"
                f"  {altes_bildverzeichnis.name}\n"
                f"  → {neues_bildverzeichnis.name}\n"
            )
        else:
            meldung += "\n• Kein Bildverzeichnis vorhanden (nichts umzubenennen).\n"

        meldung += "\nWirklich fortfahren?"

        if not askyesno("Umbenennen bestätigen", meldung):
            return

        # 1. Bildreferenzen im Body ersetzen
        neuer_body, anzahl = bildreferenzen_ersetzen(self.body, alter_slug, neuer_slug)

        # 2. Artikel mit aktualisiertem Body speichern (unter altem Namen)
        try:
            artikel_schreiben(self.aktueller_dateipfad, self.metadaten, neuer_body)
        except Exception as fehler:
            showerror("Fehler", f"Artikel konnte nicht aktualisiert werden:\n{fehler}")
            return

        # 3. Datei umbenennen
        try:
            os.rename(self.aktueller_dateipfad, neuer_dateipfad)
        except OSError as fehler:
            showerror("Fehler", f"Datei konnte nicht umbenannt werden:\n{fehler}")
            return

        # 4. Bildverzeichnis umbenennen (falls vorhanden)
        if altes_bildverzeichnis.is_dir():
            try:
                os.rename(altes_bildverzeichnis, neues_bildverzeichnis)
            except OSError as fehler:
                showerror(
                    "Fehler",
                    f"Bildverzeichnis konnte nicht umbenannt werden:\n{fehler}\n\n"
                    f"Die Artikeldatei wurde bereits umbenannt.",
                )
                return

        # 5. Zustand aktualisieren
        self.aktueller_dateiname = neuer_dateiname
        self.aktueller_dateipfad = neuer_dateipfad
        self.body = neuer_body
        self.metadaten["title"] = neuer_titel
        self.titel_var.set(neuer_titel)
        self.aenderungen_vorhanden = False

        self._status_setzen(
            f"Umbenannt: {neuer_dateiname} ({anzahl} Bildreferenzen aktualisiert)",
            "green",
        )
        showinfo(
            "Umbenannt",
            f"Artikel wurde umbenannt.\n\n"
            f"• Datei: {neuer_dateiname}\n"
            f"• Bildreferenzen: {anzahl} ersetzt\n"
            f"• Bildverzeichnis: {'umbenannt' if altes_bildverzeichnis.is_dir() else 'keins vorhanden'}",
        )

        self._artikel_liste_laden()

    def _status_setzen(self, text: str, farbe: str = "black") -> None:
        """Setzt den Text der Statuszeile."""
        if self.status_label:
            self.status_label.config(text=text, fg=farbe)


# ---------------------------------------------------------------------------
# Einstiegspunkt
# ---------------------------------------------------------------------------

def main() -> None:
    lade_referenzdaten()

    root = Tk()
    root.update_idletasks()
    breite = 720
    hoehe = 700
    x = (root.winfo_screenwidth() // 2) - (breite // 2)
    y = (root.winfo_screenheight() // 2) - (hoehe // 2)
    root.geometry(f"{breite}x{hoehe}+{x}+{y}")

    ArtikelBearbeitenGui(root)
    root.mainloop()


if __name__ == "__main__":
    main()
