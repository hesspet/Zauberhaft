# BlePrompter — Debug

**Version:** 1.0.0-debug
**Datum:** 05.06.2026
**Chip:** ESP32-C3

## Beschreibung

Debug-Version mit erweiterter serieller Log-Ausgabe. Nur f&uuml;r Entwickler
und zur Fehlersuche gedacht.

## Unterschiede zur Release-Version

- Ausf&uuml;hrliche Log-Ausgaben auf dem seriellen Monitor (115200 Baud)
- Zus&auml;tzliche Diagnose-Befehle &uuml;ber serielle Konsole
- Kein Deep-Sleep-Modus (verhindert Verbindungsabbr&uuml;che beim Debuggen)

## Warnung

Diese Version verbraucht mehr Strom und sollte nicht im Batteriebetrieb
verwendet werden. Der serielle Monitor muss w&auml;hrend des Betriebs nicht
verbunden sein, die Log-Ausgaben werden trotzdem erzeugt.
