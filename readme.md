```bash
# Vor dem ersten Start: Setup-Skript ausführen
python first_setup.py
```

# Bastiix Selfbot

Eine umfassende Anleitung zum Einrichten, Konfigurieren und Verwenden des Bastiix Selfbot.
Jeder Ordner enthält einen Unterordner `docs/` mit einer Dokumentation zu jeder Datei (außer den vorinstallierten Modulen).

Im `docs/` Ordner, welcher im gleichen Ordner wie die `main.py` liegt, ist eine detaillierte Erklärung zum Schreiben eigener Module.

---

## Inhaltsverzeichnis

1. [Einführung](#einführung)
2. [Voraussetzungen](#voraussetzungen)
3. [Installation](#installation)
4. [Konfiguration (`settings.py`)](#konfiguration-settingspy)
5. [Verzeichnisstruktur](#verzeichnisstruktur)
6. [Skript-Funktionen im Überblick](#skript-funktionen-im-überblick)
   - [main.py](#mainpy)
   - [src/core/discord/commandtree.py](#srccorediscordcommandtreepy)
   - [src/core/discord/message.py](#srccorediscordmessagepy)
   - [src/core/animation/running_animation.py](#srccoreanimationrunning_animationpy)
   - [src/core/animation/debug_animation.py](#srccoreanimationdebug_animationpy)
7. [Module und `docs/`-Ordner](#module-und-docs-ordner)
8. [Benutzung](#benutzung)
9. [Fehlerbehebung](#fehlerbehebung)

---

## Einführung
Der Bastiix Selfbot ermöglicht automatisierte Interaktionen mit Discord über einen personalisierten Bot-Account. Er lädt über Selenium die Token-Daten und verwendet die `discum`-Bibliothek, um Befehle entgegenzunehmen und auszuführen.

## Voraussetzungen

- Python 3.10 oder höher
- Chromedriver passend zur installierten Chrome-Version
- Discord-Account
- Virtuelle Umgebung via `first_setup.py` aufsetzen und Abhängigkeiten installieren

## Installation

1. Repository klonen:
   ```bash
   git clone <repo-url>
   cd <repo-directory>
   ```
2. Setup-Skript ausführen (erstellt und aktiviert venv, installiert Abhängigkeiten):
   ```bash
   python first_setup.py
   ```

## Konfiguration (`settings.py`)
In der Datei `settings.py` definierst du:

| Variable               | Beschreibung                                                                 |
|------------------------|-------------------------------------------------------------------------------|
| `DEBUG`                | `True` für ausführliche Debug-Ausgaben, `False` für Prettymode                 |
| `LOGGING`              | `True` um Logdateien unter `log/debug/` zu schreiben                          |
| `PREFIX`               | Kommando-Präfix, z. B. `$` oder `&`                                           |
| `LOGIN_EMAIL`          | E-Mail für automatisches Login (leer lassen für manuelles Login)              |
| `LOGIN_PASSWORD`       | Passwort für automatisches Login (leer lassen für manuelles Login)            |
| `ALLLOWED_USERS`       | Tupel von Discord-User-IDs, die Befehle ausführen dürfen                       |
| Farbcodes (`MAINCOLOR`,`SECONDCOLOR`, `STAMPCOLOR`,`RESETCOLOR`)
| `MAX_CHUNK_SIZE`       | Maximale Zeichenlänge pro Nachricht, bevor Chunks gesendet werden             |
| `SELFBOT_DUMP_CHANNEL` | Channel-ID für Dumps im Fehlerfall                                            |
| `RESTART_DEBUG_MODE_PATH` | Pfad zur Batch-Datei für Neustart im Debug-Mode                           |

Passe diese Werte vor dem ersten Start an.

## Verzeichnisstruktur

```
├── main.py
├── settings.py
├── requirements.txt
├── first_setup.py        # Setup-Skript für venv & Pakete
├── log/                  # Logdateien (Debug + Crash)
├── src/
│   ├── core/
│   │   ├── discord/
│   │   │   ├── commandtree.py
│   │   │   └── message.py
│   │   └── animation/
│   │       ├── running_animation.py
│   │       └── debug_animation.py
│   ├── modules/         # Benutzer-Module
│   │   └── <module_name>/
│   │       ├── setup.py
│   │       └── docs/
│   └── core/system/
│       └── restart_debug.bat
├── docs/                # Globale Dokumentation zu main.py, settings.py und Modul-Erstellung
└── src/modules/
    ├── <module1>/
    │   ├── setup.py
    │   └── docs/         # Detaillierte docs für jede Datei im Modul
    └── <module2>/
        ├── setup.py
        └── docs/
```

## Skript-Funktionen im Überblick

### `main.py`
- **SelfBot Klasse**: Initialisiert Selenium-Login, `discum.Client`, Event-Loop.
- **_perform_login()**: Versucht automatisches Login oder öffnet manuelles Fenster.
- **retry Decorator**: Wiederholungen mit Backoff für WebDriver-/Timeout-Fehler.
- **simulate_typing_send()**: Splitten langer Nachrichten, Senden mit simulated Typing.
- **setup_events()**: Websocket-Handler für `on_connect` und `on_message`.
- **cleanup()**: Schließt Gateway sauber bei Beendigung.

### `src/core/discord/commandtree.py`
- **CommandTree**: Verwaltet Registrierung und Ausführung von Commands.
- **register(cmd)**: Fügt einen `Command` hinzu.
- **handle(channel_id, author, content)**: Parst Präfix, ruft `Command.execute()` auf.
- **Autodiscover**: Lädt alle Module unter `src/modules` automatisch.
- **Help-Command**: Eingebauter `help` mit Übersicht und Detailansicht.

### `src/core/discord/message.py`
Stellt verschiedene Formatierungsfunktionen für Rückgabewerte bereit:
- `success_message`, `info_message`, `error_message`, `boxed_message_with_title`, u.v.m.

### `src/core/animation/running_animation.py`
- **append_message(text)**: Schicke Pretty-Output mit Zeitstempel und Farbgebung.
- **print_banner(text)**: Große Rahmen-Banner, wenn `DEBUG=False`.

### `src/core/animation/debug_animation.py`
- **DebugConsole** (`debug_logger`): Loggt Debug/Warn/Error intern und in Dateien.
- **debug()/warning()/error()**: Methoden zur differenzierten Protokollierung.

## Module und `docs/`-Ordner

Jeder Modul-Ordner enthält einen `docs/`-Unterordner mit Dokumentation für jede Datei:
```
src/modules/<modul>/docs/
├── setup.md         # Erklärt Aufbau der setup()-Funktion
└── weitere_datei.md # Detaillierte Beschreibung
```
Verweise aus dem Haupt-`README` via relative Pfade.

## Benutzung

1. `python main.py` starten
2. Folge dem Chrome-Login (manuell oder automatisch durch `LOGIN_EMAIL`/`LOGIN_PASSWORD`)
3. Nutze Befehle in Discord mit dem Präfix aus `settings.py` (`$` standardmäßig)
4. Hilfestellung mit `$help` und `$help <befehl>`

## Fehlerbehebung

- **Chromedriver-Inkompatibilität**: Stelle sicher, dass Versionen übereinstimmen.
- **Timeout beim Token**: Warte max. 5 Minuten manuell im Fenster, prüfe Cookies.
- **Keine Module gefunden**: Prüfe `src/modules` und `__init__.py`
- **Logs einsehen**: Debug-Logs in `log/debug/`, Crash-Dumps in `log/system/`

---

*Dieses Readme ist KI Generiert.*

