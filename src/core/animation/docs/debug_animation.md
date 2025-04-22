# Debug Animation Modul (`debug_animation.py`)

Dieses Modul stellt eine zentralisierte Logger-Klasse bereit, um Debug-, Warn- und Fehler-Nachrichten konsistent formatiert auszugeben und in Log-Dateien zu speichern. Durch die Nutzung dieser Klasse wird sichergestellt, dass alle Debug-Ausgaben einheitlich aussehen und die Log-Konsistenz gewahrt bleibt.

## Inhaltsverzeichnis

1. [Installation / Import](#installation--import)
2. [Klasse `DebugConsole`](#klasse-debugconsole)
   - [Initialisierung](#initialisierung)
   - [Methoden](#methoden)
3. [Konfiguration](#konfiguration)
4. [Beispielnutzung](#beispielnutzung)
5. [Hinweis zur Konsistenz](#hinweis-zur-konsistenz)

---

## Installation / Import

1. Stelle sicher, dass das Modul in deinem Python-Pfad liegt.
2. Importiere den globalen Logger:

```python
from src.core.animation.debug_animation import logger
```


## Klasse `DebugConsole`

Die `DebugConsole` ist eine Singleton-ähnliche Klasse, die alle Debug-, Warn- und Fehler-Meldungen entgegennimmt und:

- Auf der Konsole ausgibt (sofern `DEBUG=True`).
- ANSI-Farb-Codierung für verschiedene Ebenen (DEBUG, WARNUNG, FEHLER) nutzt.
- Nachrichten in eine Log-Datei schreibt (sofern `LOGGING=True`).

### Initialisierung

```python
logger = DebugConsole()
```

- Der Logger liest die Einstellungen `DEBUG` und `LOGGING` aus `settings.py`.
- Bei aktiviertem Logging wird im Verzeichnis `log/debug/` automatisch eine Datei mit Zeitstempel angelegt.

### Methoden

| Methode           | Beschreibung                                                                                             |
|-------------------|----------------------------------------------------------------------------------------------------------|
| `debug(fn, msg)`  | Protokolliert eine Debug-Nachricht. Wird nur ausgegeben, wenn `DEBUG=True`.                              |
| `warning(fn, msg)`| Protokolliert eine Warnung. Wird nur ausgegeben, wenn `DEBUG=True`.                                      |
| `error(fn, msg)`  | Protokolliert eine Fehler-Meldung. Wird nur ausgegeben, wenn `DEBUG=True`.                                |

#### Parameter

- `fn` (`str`): Name der Funktion oder Context-Identifikator, aus dem die Nachricht stammt.
- `msg` (`str`): Der eigentliche Log-Text. Kann mehrzeilig sein.


## Konfiguration

Die folgenden Einstellungen können in `settings.py` angepasst werden:

- `DEBUG` (`bool`): Steuert, ob Ausgaben auf der Konsole erscheinen.
- `LOGGING` (`bool`): Steuert, ob Ausgaben zusätzlich in Dateien geschrieben werden.
- ANSI-Farbcodes können über `RESETCOLOR` in `settings.py` angepasst werden.


## Beispielnutzung

```python
from src.core.animation.debug_animation import logger


def my_function(x):
    logger.debug('my_function', f'Starte Verarbeitung von {x}')
    try:
        result = x / 0  # Beispiel für einen Fehler
    except Exception as e:
        logger.error('my_function', f'Fehler aufgetreten: {e}')
    else:
        logger.debug('my_function', f'Ergebnis: {result}')

my_function(42)
```


## Hinweis zur Konsistenz

Um die Einheitlichkeit der Log-Ausgaben und die Optik zu wahren, **sollten alle Debug-, Warnungs- und Fehler-Messages ausschließlich an diese `DebugConsole`-Instanz (`logger`) gesendet werden**. Vermeide direkte `print`-Aufrufe oder alternative Logging-Mechanismen in deinem Code.

---

*Dokumentation generiert für `debug_animation.py`*

