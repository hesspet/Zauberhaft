"""
BlogArtikelAnlegen – GUI zum Anlegen eines neuen Blog-Artikels via New-Article.ps1
Verwendung: pythonw BlogArtikelAnlegen.py  (kein Konsolenfenster)
"""
from __future__ import annotations

import subprocess
import yaml
from pathlib import Path
from tkinter import Tk, Frame, Label, Entry, Button, Text, StringVar
from tkinter import ttk
from tkinter.messagebox import showinfo, showerror

PROJECT_ROOT = Path(__file__).resolve().parent
PS1_PATH = PROJECT_ROOT / "tools" / "New-Article.ps1"

ARTIKELTYPEN: list[str] = []
THEMEN: list[str] = []


def load_reference_data() -> None:
    """Liest erlaubte Artikeltypen und Themen aus den YAML-Dateien."""
    global ARTIKELTYPEN, THEMEN

    types_path = PROJECT_ROOT / "_data" / "blog_article_types.yml"
    if types_path.is_file():
        with open(types_path, encoding="utf-8") as fh:
            ARTIKELTYPEN = yaml.safe_load(fh) or []

    topics_path = PROJECT_ROOT / "_data" / "blog_topics.yml"
    if topics_path.is_file():
        with open(topics_path, encoding="utf-8") as fh:
            THEMEN = yaml.safe_load(fh) or []


def build_gui(root: Tk) -> None:
    title_var = StringVar()
    type_var = StringVar()
    topics_var = StringVar()

    # --- Titel ---
    Label(root, text="Titel des Artikels:", anchor="w").pack(fill="x", padx=12, pady=(12, 0))
    Entry(root, textvariable=title_var, width=70).pack(fill="x", padx=12, pady=(2, 0))

    # --- Typ ---
    Label(root, text="Artikeltyp:", anchor="w").pack(fill="x", padx=12, pady=(10, 0))
    type_combo = ttk.Combobox(root, textvariable=type_var, values=ARTIKELTYPEN, state="readonly", width=30)
    type_combo.pack(anchor="w", padx=12, pady=(2, 0))
    if ARTIKELTYPEN:
        type_combo.current(0)

    # --- Themen ---
    Label(root, text="Themen (kommagetrennt):", anchor="w").pack(fill="x", padx=12, pady=(10, 0))
    Entry(root, textvariable=topics_var, width=70).pack(fill="x", padx=12, pady=(2, 0))

    # Themen-Referenz
    if THEMEN:
        ref_frame = Frame(root)
        ref_frame.pack(fill="x", padx=12, pady=(4, 0))
        Label(ref_frame, text="Verfügbar:", anchor="w", fg="gray").pack(side="left")
        Label(ref_frame, text=", ".join(THEMEN), anchor="w", fg="gray", wraplength=580, justify="left").pack(
            side="left", padx=(6, 0)
        )

    # --- Zusammenfassung ---
    Label(root, text="Kurze Zusammenfassung:", anchor="w").pack(fill="x", padx=12, pady=(10, 0))
    summary_text = Text(root, height=3, width=70, wrap="word")
    summary_text.pack(fill="x", padx=12, pady=(2, 0))

    # --- Statuszeile ---
    status_label = Label(root, text="", anchor="w", fg="gray")
    status_label.pack(fill="x", padx=12, pady=(12, 0))

    # --- Buttons ---
    button_frame = Frame(root)
    button_frame.pack(fill="x", padx=12, pady=(8, 12))

    def _anlegen() -> None:
        titel = title_var.get().strip()
        typ = type_var.get().strip()
        topics = topics_var.get().strip()
        summary = summary_text.get("1.0", "end-1c").strip()

        # Validierung
        fehler: list[str] = []
        if not titel:
            fehler.append("- Titel ist erforderlich.")
        if not typ:
            fehler.append("- Artikeltyp ist erforderlich.")
        if not topics:
            fehler.append("- Mindestens ein Thema ist erforderlich.")
        if not summary:
            fehler.append("- Zusammenfassung ist erforderlich.")
        if fehler:
            showerror("Eingabefehler", "Bitte korrigieren:\n\n" + "\n".join(fehler))
            return

        if not PS1_PATH.is_file():
            showerror("Fehler", f"PowerShell-Skript nicht gefunden:\n{PS1_PATH}")
            return

        # PowerShell aufrufen
        status_label.config(text="Lege Artikel an …", fg="black")
        root.update_idletasks()

        try:
            result = subprocess.run(
                [
                    "powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass",
                    "-File", str(PS1_PATH),
                    "-Title", titel,
                    "-Type", typ,
                    "-Topics", topics,
                    "-Summary", summary,
                ],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=30,
            )
        except subprocess.TimeoutExpired:
            showerror("Fehler", "Das PowerShell-Skript hat zu lange gedauert.")
            status_label.config(text="", fg="gray")
            return

        if result.returncode == 0:
            showinfo("Fertig", "Artikel und Bildordner wurden angelegt.\n\nAusgabe:\n" + result.stdout)
            status_label.config(text="Artikel erfolgreich angelegt.", fg="green")
        else:
            fehlertext = (result.stderr or result.stdout or "Unbekannter Fehler")
            showerror("Fehler", f"PowerShell meldete einen Fehler (Code {result.returncode}):\n\n{fehlertext}")
            status_label.config(text="Fehler beim Anlegen.", fg="red")

    Button(button_frame, text="Artikel anlegen", command=_anlegen, width=20, height=2).pack(side="left")
    Button(button_frame, text="Abbrechen", command=root.destroy, width=10, height=2).pack(side="left", padx=(8, 0))


def main() -> None:
    load_reference_data()

    root = Tk()
    root.title("Neuen Blog-Artikel anlegen")
    root.resizable(width=True, height=False)
    # Zentriere das Fenster grob
    root.update_idletasks()
    w = 680
    h = 480
    x = (root.winfo_screenwidth() // 2) - (w // 2)
    y = (root.winfo_screenheight() // 2) - (h // 2)
    root.geometry(f"{w}x{h}+{x}+{y}")

    build_gui(root)

    root.mainloop()


if __name__ == "__main__":
    main()
