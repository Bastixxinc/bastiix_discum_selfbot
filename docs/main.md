# Dokumentation von `main.py`

Diese Dokumentation beschreibt den Aufbau und die Hauptfunktionen der Datei `main.py`, die den SelfBot für Discord initialisiert, konfiguriert und ausführt.

---

## Inhaltsverzeichnis

1. [Übersicht](#übersicht)
2. [Voraussetzungen](#voraussetzungen)
3. [Konfiguration](#konfiguration)
4. [Retry-Decorator](#retry-decorator)
5. [Fehlerklassen](#fehlerklassen)
6. [Klasse `SelfBot`](#klasse-selfbot)
   - [Initialisierung (`__init__`)](#initialisierung-init)
   - [Login-Mechanismus](#login-mechanismus)
   - [Event Loop mit Backoff](#event-loop-mit-backoff)
   - [Token-Verifikation](#token-verifikation)
   - [Nachrichtenversand mit simuliertem Tippen](#nachrichtenversand-mit-simuliertem-tippen)
   - [Gateway-Events](#gateway-events)
   - [Aufräumarbeiten (`cleanup`)](#aufräumarbeiten-cleanup)
   - [Ausführung (`run`)](#ausführung-run)
7. [Beispielhafter Programmablauf](#beispielhafter-programmablauf)

---

## Übersicht

`main.py` implementiert einen Discord-SelfBot auf Basis von [Discum](https://github.com/Merubokkusu/Discord-S.C.U.M). Der Bot:

- Lädt Einstellungen aus `settings.py`.
- Führt eine Anmeldung via Chrome-Selenium durch.
- Initialisiert Discord-Client, Befehlsbaum und Event-Loop.
- Handhabt automatisches Wiederverbinden und Fehlertoleranz.
- Bietet eine simulierte Tipphandlung vor dem Versenden von Nachrichten.

---

## Voraussetzungen

- Python 3.x
- Chrome Browser + kompatibler Chromedriver auf PATH
- Pakete (siehe `requirements.txt`):
  - `selenium`
  - `discum`
  - Standardbibliotheken: `asyncio`, `threading`, `subprocess`, u. a.

---

## Konfiguration

Einstellungen werden in `settings.py` definiert:

```python
DEBUG = True                # Schaltet Debug-Ausgaben an/aus
PREFIX = "$"              # Präfix für Bot-Befehle
LOGIN_EMAIL = "..."        # Optional für automatisches Login
LOGIN_PASSWORD = "..."     # Optional für automatisches Login
ALLLOWED_USERS = (...)       # IDs erlaubter Nutzer
MAX_CHUNK_SIZE = 2000        # Maximale Nachrichtenlänge pro Chunk
...
```

Um manuelles Login zu erzwingen, lassen Sie `LOGIN_EMAIL` und `LOGIN_PASSWORD` leer.

---

## Retry-Decorator

```python
def retry(exceptions, tries=2, delay=5, backoff=2, logger=None):
    ...
```

- **Zweck**: Wiederholtes Ausführen einer Funktion bei bestimmten Ausnahmen.
- **Parameter**:
  - `exceptions`: Tuple von Exception-Klassen zum Abfangen.
  - `tries`: Maximalversuche (inkl. erster Ausführung).
  - `delay`: Wartezeit vor erneutem Versuch (Sekunden).
  - `backoff`: Multiplikator zur Verlängerung der Wartezeit.
  - `logger`: Optionaler Logger für Warnmeldungen.

---

## Fehlerklassen

### `LoginError`

Erweiterung von `Exception`, enthält zusätzliche Felder:

- `attempts`: Anzahl erfolgter Versuche.
- `last_exception`: Letzte gefangene Ausnahme.
- `timestamp`: UTC-Zeitpunkt des Fehlers.


---

## Klasse `SelfBot`

Kernklasse, die den SelfBot verwaltet.

### Initialisierung (`__init__`)

1. Liest Debug-Flag und Settings.
2. Registriert globalen Exception-Hook.
3. Bestimmt erlaubte Benutzer-IDs (`allowed_users`).
4. Zeigt optional Banner im Terminal.
5. Führt Login durch (`_perform_login`).
6. Initialisiert Discum-Client und Befehlssystem (`CommandTree`).
7. Setzt Chameleon-Maske und startet Event-Loop in eigenem Thread.
8. Registriert Cleanup-Funktion via `atexit`.

### Login-Mechanismus

- **Methode**: `_login_via_chrome`
- Öffnet Chrome mit Selenium, navigiert zu `https://discord.com/login`.
- Entscheidet zwischen automatischem und manuellem Login.
- Wartet bis URL `/channels/` enthält.
- Liest Discord-Token aus `window.localStorage` mittels iframe-Hack.
- Schließt Browser und liefert Token.
- Wird durch `_perform_login` mit maximal 2 Versuchen (`MAX_LOGIN_ATTEMPTS`) umgeben.

### Event Loop mit Backoff

- **Methode**: `_run_event_loop_with_backoff`
- Führt `self.loop.run_forever()` in Schleife mit bis zu 3 Wiederholungen aus.
- Bei Fehlern: Stackdump schreiben, optional Debug-Neustart, Wartezeiten mit exponentiellem Backoff.

### Token-Verifikation

- **Methode**: `verify_token`
- Ruft `bot.info()` über REST auf.
- Prüft, ob gültige Nutzerdaten (z. B. `id`) zurückkommen.
- Im Fehlerfall Terminierung des Programms.

### Nachrichtenversand mit simuliertem Tippen

- **Methode**: `simulate_typing_send(channel: str, message: str)`
- Prüft Kanal-ID-Format.
- Teilt lange Nachrichten in Chunks nach `MAX_CHUNK_SIZE` auf.
- Berechnet Tippdauer anhand der Nachrichtlänge.
- Führt vor jedem Sendevorgang `typingAction()` aus und wartet.

### Gateway-Events

- **Methode**: `setup_events`
- Registriert zwei Gateway-Handler:
  1. `on_connect`: Setzt Presence (`online`), lädt Nutzer-Infos, zeigt Banner und Logs.
  2. `on_message`: Filtert Bot- und Fremdnachrichten, prüft Präfix, führt Befehle via `CommandTree` aus, sendet Antwort.

### Aufräumarbeiten (`cleanup`)

- Schließt Gateway und setzt internes Stop-Event.
- Wird automatisiert bei Programmende (`atexit`) oder `KeyboardInterrupt` aufgerufen.

### Ausführung (`run`)

- Ruft `verify_token()` auf.
- Zeigt Start-Banner oder Debug-Log.
- Startet Gateway mit `auto_reconnect=True`.
- Handhabt KeyboardInterrupt und unerwartete Fehler mit sauberem Herunterfahren.

---

## Beispielhafter Programmablauf

1. Programmstart: `bot = SelfBot()` → `__init__()` → Login
2. Verifizierung des Tokens
3. Aufbau des Discord-Gateways
4. Empfang von Nachrichten → Ausführung von Befehlen
5. Bei Beendung: `cleanup()` → Programmende

---

*Ende der Dokumentation für main.py*

