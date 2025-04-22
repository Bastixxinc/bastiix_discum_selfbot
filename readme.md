```bash
# Vor dem ersten Start: Setup-Skript ausführen
python first_setup.py
```

# Bastiix Selfbot

Eine umfassende Anleitung zum Einrichten, Konfigurieren und Verwenden des Bastiix Selfbot.
Jeder Ordner enthält einen Unterordner `docs/` mit einer Dokumentation zu jeder Datei.

**Es werden keine Module mitgeliefert. `help` ist der einzige integriere Befehl!** 

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
   git clone https://github.com/Bastixxinc/bastiix_discum_selfbot

   cd <repo-directory>
   ```
2. Setup-Skript ausführen (erstellt und aktiviert venv, installiert Abhängigkeiten):
   ```bash
   python first_setup.py
   ```

## Konfiguration (`settings.py`)
In der Datei `settings.py` definierst du:

| Variable               | Beschreibung                                                                  |
|------------------------|-------------------------------------------------------------------------------|
| `DEBUG`                | `True` für ausführliche Debug-Ausgaben, `False` für Prettymode                |
| `LOGGING`              | `True` um Logdateien unter `log/debug/` zu schreiben                          |
| `PREFIX`               | Kommando-Präfix, z. B. `$` oder `&`                                           |
| `LOGIN_EMAIL`          | E-Mail für automatisches Login (leer lassen für manuelles Login)              |
| `LOGIN_PASSWORD`       | Passwort für automatisches Login (leer lassen für manuelles Login)            |
| `ALLLOWED_USERS`       | Tupel von Discord-User-IDs, die Befehle ausführen dürfen                      |
| `MAINCOLOR`            | Hauptfarbe des Console Outputs in ANSI-Escape-Sequenz                         |
| `SECONDCOLOR`          | Accentfarbe des Console Outputs in ANSI-Escape-Sequenz                        |
| `STAMPCOLOR`           | Zeitstempelfarbe des Console Outputs in ANSI-Escape-Sequenz                   |
| `RESETCOLOR`           | Resetfarbe des Console Outputs in ANSI-Escape-Sequenz                         |
| `MAX_CHUNK_SIZE`       | Maximale Zeichenlänge pro Nachricht, bevor Chunks gesendet werden             |
| `SELFBOT_DUMP_CHANNEL` | Channel-ID für Dumps (ungenutzt)                                              |

Passe diese Werte vor dem ersten Start an.

## Verzeichnisstruktur

```plaintext
╔══════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
├─── first_setup.py    # Dieses Skript führt den initialen Setup-Prozess automatisiert aus.
├─── main.py           # Hauptskript zum Start des Selfbots.
├─── readme.md         # Übersicht und Anleitung.
├─── settings.py       # Konfigurationsdatei.
├─── docs/             # Dokumentationen für main.py, settings.py und Module.
│   ├─ main.md              # Anleitung zum Aufsetzen eines eigenen Moduls.
│   ├─ modul_erstellen.md   # Anleitung zur Modulerstellung.
│   └─ settings.md         # Dokumentation der Einstellungen.
├─── log/              # Ordner für Debug- und Systemlogs.
│   ├─ debug/              # Debug-Logs.
│   │   └─ ...
│   └─ system/             # System-Logs.
│       └─ ...
└─── src/              # Quellcode-Verzeichnis.
    ├─ __init__.py
    ├─ core/                # Systemabhängigkeiten.
    │   ├─ animation/           # Startup-Animationen.
    │   │   ├─ debug_animation.py    # Debugging und Logging.
    │   │   ├─ pretty_animation.py   # Start-up-Animation.
    │   │   ├─ running_animation.py  # Ausgabe im „Pretty Mode“.
    │   │   └─ docs/                 # Dokumentation der Animationen.
    │   │       ├─ debug_animation.md
    │   │       ├─ pretty_animation.md
    │   │       └─ running_animation.md
    │   ├─ discord/             # Discord-Core-Skripte.
    │   │   ├─ chameleon_mask.py    # Tarn-Mechanismus für den Selfbot-Status.
    │   │   ├─ commandtree.py       # Befehlsregistrierung für modularen Import.
    │   │   ├─ message.py           # Formatierung von Discord-Nachrichten.
    │   │   └─ docs/                # Dokumentation der Skripte.
    │   │       ├─ chameleon_mask.md
    │   │       ├─ commandtree.md
    │   │       └─ message.md
    │   └─ system/              # Systemskripte (.bat/.sh).
    │       ├─ restart_debug.bat   # Fallback-Neustart im Debug-Modus (Windows).
    │       ├─ restart_debug.sh    # Fallback-Neustart im Debug-Modus (Linux).
    │       └─ docs/               # Dokumentation (aktuell keine).
    └─ modules/             
        ├─ __init__.py           # Initialisierung für modularen Import.
        └─ inaktiv/              # Vom Import ignorierte, inaktive Module.
            └─ ...
╚══════════════════════════════════════════════════════════════════════════════════════════════════════════════╝
```



## Skript-Funktionen im Überblick

### `main.py`
- **SelfBot Klasse**: Initialisiert Selenium-Login, `discum.Client`, Event-Loop.
- **_perform_login()**: Versucht automatisches oder manuelles Login in einem Chrome Fenster.
- **retry Decorator**: Wiederholungen mit Backoff für WebDriver-/Timeout-Fehler.
- **simulate_typing_send()**: Splitten langer Nachrichten, Senden mit simulated Typing.
- **setup_events()**: Websocket-Handler für `on_connect` und `on_message`.
- **cleanup()**: Schließt Gateway sauber bei Beendigung.

### `src/core/discord/commandtree.py`
- **CommandTree**: Verwaltet Registrierung und Ausführung von Commands.
- **register(cmd)**: Fügt einen `Command` hinzu.
- **handle(channel_id, author, content)**: Parst Präfix, ruft `Command.execute()` auf.
- **Autodiscover**: Lädt alle Module unter `src/modules/ . . .` automatisch.
- **Help-Command**: Eingebauter `help` mit Übersicht und Detailansicht sowie automatischer Integration der Befehler in den Modulen.

### `src/core/discord/message.py`
Stellt verschiedene Formatierungsfunktionen für Discord Nachrichten bereit:
- `success_message`, `info_message`, `error_message`, `boxed_message_with_title`, u.v.m.

### `src/core/animation/running_animation.py`
- **append_message(text)**: Pretty-Output (Debug = False) Runntime Console Outputs mit Zeitstempel und Farbgebung.
- **print_banner(text)**: Rahmen-Banner (Debug = False) Runntime Console Outputs.

### `src/core/animation/debug_animation.py`
- **DebugConsole** (`debug_logger`): Loggt Debug/Warn/Error intern und in Dateien. Nimmt Console Debug Output entgegen. Printet nur wenn (Debug = True)
- **debug()/warning()/error()**: Methoden zur differenzierten Protokollierung und Output

## Module und `docs/`-Ordner

Jeder Ordner enthält einen `docs/`-Unterordner mit Dokumentation für jede Datei:

---

## Benutzung

1. `python first_setup.py` starten (venv und requirements.tx setup automatisiert)
2. Folge den Anweisungen des Outputs der first_setup.py
3. Konfiguriere ggf die settings.py 
4. `python main.py` starten
5. Folge dem Chrome-Login (manuell oder automatisch durch `settings.LOGIN_EMAIL`/`settings.LOGIN_PASSWORD`)
6. Nutze Befehle in Discord mit dem Präfix aus `settings.py` (`$` standardmäßig)
7. Hilfestellung mit `$help` und `$help <befehl>`

## Fehlerbehebung

- **Chromedriver-Inkompatibilität**: Stelle sicher, dass Versionen übereinstimmen.
- **Timeout beim Token**: Warte max. 5 Minuten manuell im Fenster, prüfe Cookies.
- **Keine Module gefunden**: Prüfe `src/modules` und `__init__.py`
- **Logs einsehen**: Debug-Logs in `log/debug/`, Crash-Dumps in `log/system/`
- **Selfbot ist online aber reagiert nicht auf Befehle**: Überprüfe ob deie Discord-IP in der settings.py unter `ALLLOWED_USERS`registriert ist. Mehrere IDs werden mit Komma getrennt. `ALLLOWED_USERS = ("1234567890", "0987654321")

---

*Dieses Readme ist Teilweise AI Generiert.*
~ Bastiix
