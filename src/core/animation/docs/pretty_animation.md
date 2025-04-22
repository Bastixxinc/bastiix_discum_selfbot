# Modul: pretty_animation.py

Dieses Modul stellt Funktionen zur Verfügung, um ansprechende Start‑ und Endanimationen im Terminal anzuzeigen. Es ist Teil der Kommandozeilenanimationen und wird typischerweise beim Starten oder Beenden von Anwendungen verwendet.

## Übersicht

- **Ziel**: Visuelle Banner und Statusanzeigen im Terminal mit Puls‑Effekt und Typewriter‑Style.
- **Anwendungsfall**: Startup‑Banner, Abschluss‑Nachrichten, typisierte Laufzeit‑Informationen.
- **Abhängigkeiten**: Standard‑Bibliothek (`sys`, `time`, `datetime`), optionale `settings` zum Aktivieren/Deaktivieren.

## Funktionen

### `typewriter_print(text: str, delay: float = 0.05)`

Schreibt den übergebenen Text Zeichen für Zeichen im Typewriter‑Effekt. Wenn `settings.DEBUG` gesetzt ist, erfolgt die Ausgabe; andernfalls bleibt die Funktion stumm.

- **Parameter**:
  - `text` – Der auszugebende String.
  - `delay` – Pause (in Sekunden) zwischen den Zeichen (Standard: 0.05).

### `pretty_banner(
    banner_text: str,
    completion_title: str,
    completion_message: str,
    pulse_cycles: int = 4,
    pulse_delay: float = 0.35,
    type_delay: float = 0.015
)`

Erzeugt ein mehrzeiliges Banner mit Rahmen und Puls‑Animation, gefolgt von einem Abschlussrahmen mit Zeitstempel und Message im Typewriter‑Stil.

- **Parameter**:
  - `banner_text` – Text, der im Hauptbanner angezeigt wird.
  - `completion_title` – Titel im Abschlussbanner.
  - `completion_message` – Nachricht, die zusammen mit einem Zeitstempel angezeigt wird.
  - `pulse_cycles` – Anzahl der Puls‑Durchläufe (Standard: 4).
  - `pulse_delay` – Verzögerung zwischen den Farbwechseln in Sekunden (Standard: 0.35).
  - `type_delay` – Verzögerung für die abschließende Typmaschinen‑Nachricht (Standard: 0.015).

- **Funktionsweise**:
  1. Erzeugt obere, mittlere und untere Rahmenlinien um `banner_text`.
  2. Wechselt für `pulse_cycles` zwischen zwei Farben und zeigt das Banner pulsierend.
  3. Zeigt den Abschlussrahmen mit `completion_title`.
  4. Druckt `completion_message` zusammen mit dem aktuellen Timestamp im Typewriter‑Stil.

- **Hinweis**: Wenn `settings.DEBUG` auf `True` gesetzt ist, erfolgt keine Animation.

## Verwendung

```python
from src.core.animation.pretty_animation import pretty_banner

# Beispiel beim Programmstart:
pretty_banner(
    banner_text="Mein Programm startet",
    completion_title="Initialisierung abgeschlossen",
    completion_message="Alle Systeme bereit",
)

# Beispiel beim Programmende:
pretty_banner(
    banner_text="Mein Programm wird beendet",
    completion_title="Beendet",
    completion_message="Bis zum nächsten Mal!",
)
```

## Konfiguration

Das Modul beachtet die Variable `settings.DEBUG`:

- `DEBUG = False` (Produktivmodus): Animationen werden angezeigt.
- `DEBUG = True` (Entwicklungsmodus): Animationsfunktionen sind stumm, um Log‑Ausgaben nicht zu stören.

## Integration

- Importiere das Modul in deiner Startup‑Routine, bevor kritische Initialisierungen erfolgen.
- Verwende am Ende deiner Anwendung ein weiteres Banner, um das Beenden optisch hervorzuheben.

Beispiel in der `__main__`‑Datei:

```python
from src.core.animation.pretty_animation import pretty_banner

def main():
    pretty_banner("Starte Anwendung", "Bereit", "Anwendung läuft...")
    # ... Hauptlogik ...
    pretty_banner("Beende Anwendung", "Fertig", "Auf Wiedersehen!")

if __name__ == '__main__':
    main()
```

---
*Dieses Modul ist speziell für Startup‑ und Endanimationen im Terminal konzipiert.*

