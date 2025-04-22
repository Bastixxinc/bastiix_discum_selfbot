# Laufzeit-Animation (running_animation.py)

Dieses Modul stellt Hilfsfunktionen bereit, um während der Laufzeit ansprechende Konsolenausgaben zu erzeugen. Es eignet sich insbesondere für Bots oder CLI-Programme, die Statusmeldungen und Fortschrittsanzeigen visuell hervorheben möchten.

## Inhaltsverzeichnis

1. [Voraussetzungen](#voraussetzungen)
2. [Import](#import)
3. [Konfiguration](#konfiguration)
4. [Funktionen](#funktionen)
   - [typewriter_print](#typewriter_print)
   - [print_banner](#print_banner)
   - [append_message](#append_message)
5. [Empfohlene Nutzung](#empfohlene-nutzung)
6. [Beispiele](#beispiele)

---

## Voraussetzungen

- Python 3.6+
- Optional: eigene `settings`-Datei mit folgenden Einstellungen:
  ```python
  DEBUG = False               # Wenn True: Ausgabe über Banner/Append unterdrücken
  MAINCOLOR = "\033[1;34m"   # Farbe für Banner-Rahmen
  STAMPCOLOR = "\033[1;32m" # Farbe für Zeitstempel
  SECONDCOLOR = "\033[1;33m"# Farbe für Nachrichtentext
  RESETCOLOR = "\033[0m"    # Reset-Farbe
  ```
- Falls `settings` nicht vorhanden ist, wird standardmäßig `DEBUG = True` angenommen und alle Ausgaben unterdrückt.

## Import

```python
from src.core.animation.running_animation import (
    typewriter_print,
    print_banner,
    append_message
)
```

## Konfiguration

Alle Funktionen respektieren den `settings.DEBUG`-Wert:

- `settings.DEBUG = True` ⇒ `print_banner` und `append_message` führen **keine** Ausgabe durch.
- `settings.DEBUG = False` ⇒ Ausgaben werden angezeigt.

Farbcodes und Zeitformat können über die `settings`-Variablen angepasst werden.

## Funktionen

### `typewriter_print(text: str, delay: float = 0.01) -> None`

Gibt den übergebenen Text zeichenweise im "Typewriter-Stil" aus.

**Parameter**:
- `text` – Der auszugebende String.
- `delay` – Verzögerung in Sekunden zwischen den Zeichen.

**Verhalten**:
- Schreibt jeden Buchstaben einzeln mit `sys.stdout.write`, gefolgt von `time.sleep(delay)`.
- Am Ende wird ein Zeilenumbruch ausgegeben.

### `print_banner(text: str) -> None`

Erzeugt eine dekorative Rahmenanzeige um einen kurzen Text.

**Parameter**:
- `text` – Der Text, der mittig im Rahmen stehen soll.

**Verhalten**:
- Nur aktiv, wenn `settings.DEBUG is False`.
- Berechnet Rahmengröße basierend auf Textlänge.
- Druckt Rahmen und Text in der Hauptfarbe (`MAINCOLOR`) und setzt anschließend zurück (`RESETCOLOR`).

### `append_message(message: str) -> None`

Gibt eine formatierte Laufzeit-Meldung mit Zeitstempel aus.

**Parameter**:
- `message` – Der frei wählbare Meldungstext.

**Verhalten**:
- Nur aktiv, wenn `settings.DEBUG is False`.
- Ermittelt aktuellen Zeitstempel im Format `HH:MM:SS.mmm`.
- Erzeugt eine Zeile:
  ```
  "   ↳ [STAMPCOLOR]HH:MM:SS.fff[RESET] | [SECONDCOLOR]message[RESET]"
  ```
- Gibt die Zeile mithilfe von `typewriter_print` aus.

## Empfohlene Nutzung

- **Primärer Einsatz**: Verwenden Sie `append_message` für alle laufzeitbezogenen Status- oder Debug-Ausgaben in der Konsole.
- **Banner**: `print_banner` nur dann einsetzen, wenn Sie eine optisch hervorgehobene, vollflächige Nachricht wünschen (z. B. zum Start oder Ende eines Prozesses).
- **Typewriter**: `typewriter_print` ist eine Low-Level-Hilfe; rufen Sie es direkt nur auf, wenn das Typing-Feeling gewünscht ist.

## Beispiele

```python
from src.core.animation.running_animation import print_banner, append_message

def main():
    print_banner("Start der Verarbeitung")
    
    # ... Ihre Logik ...
    append_message("Schritt 1 abgeschlossen")
    # ... mehr Logik ...
    append_message("Schritt 2 abgeschlossen")
    
    print_banner("Verarbeitung beendet")

if __name__ == "__main__":
    main()
```

---

*Ende der Dokumentation.*

