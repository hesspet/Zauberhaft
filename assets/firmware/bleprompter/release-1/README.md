# BlePrompter — Release 1

**Version:** 1.0.0
**Datum:** 05.06.2026
**Chip:** ESP32-C3

## Beschreibung

Stabile Release-Version des BLE Prompters. Geeignet f&uuml;r den produktiven Einsatz
in Shows und Vorf&uuml;hrungen.

## Enthaltene Features

- BLE Advertising mit konfigurierbaren Intervallen
- Empfang von Textnachrichten &uuml;ber BLE
- Darstellung auf angeschlossenem OLED-Display
- Over-the-Air (OTA) Update-F&auml;higkeit

## Installation

1. ESP32-C3 &uuml;ber USB mit dem Computer verbinden
2. Auf dieser Seite den &bdquo;Installieren&ldquo;-Button klicken
3. Im Browser-Dialog den seriellen Port ausw&auml;hlen
4. Warten bis der Flash-Vorgang abgeschlossen ist

## Bekannte Einschr&auml;nkungen

- Bei sehr langen Textnachrichten (> 500 Zeichen) kann es zu Verz&ouml;gerungen kommen
- OTA-Updates erfordern WLAN-Verbindung
