# assets

Bitte hier das Profilbild ablegen:

- **Dateiname:** `peter-hess.jpg`
- **Format:** JPEG
- **Empfohlene Größe:** 500×500 Pixel oder größer (wird auf 180×180 skaliert)
- **Position:** Das Bild erscheint im kreisrunden Avatar im Hero-Bereich der Startseite.

Solange kein Bild hinterlegt ist, wird der Platzhalter ausgeblendet und die Seite funktioniert einwandfrei.

## Blog-Assets

Blog-spezifische Dateien liegen unter `assets/diy-magic/`:

- `css/site.css`: Dark-Theme und Blog-Layout; View Transitions sind für den Blog deaktiviert.
- `js/blog-navigation.js`: clientseitige Navigation für Blog-interne Links und Wechsel vom Blog zur Hauptseite.
- `js/search.js`: clientseitige Suche; wird im Blog-Basislayout geladen und initialisiert sich nur auf der Suchseite.
- `images/articles/<artikel-slug>/`: Bilder zu einzelnen Artikeln.

CSS, JavaScript und der Suchindex werden in den Layouts mit einer Build-Version als Query-Parameter eingebunden, damit Browser nach Deploys aktuelle Dateien laden.
