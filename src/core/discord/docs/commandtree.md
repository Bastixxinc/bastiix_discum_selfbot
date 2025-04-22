# Dokumentation von `commandtree.py`

Diese Datei implementiert die Klasse `CommandTree`, die alle Bot-Befehle verwaltet, registriert und ausführt sowie die Klasse `Command`, die einzelne Befehle kapselt.

---

## Inhaltsverzeichnis

1. [Übersicht](#übersicht)
2. [Imports und Abhängigkeiten](#imports-und-abhängigkeiten)
3. [Klasse `Command`](#klasse-command)
   - [Attribute](#command-attribute)
   - [Methoden](#command-methoden)
4. [Klasse `CommandTree`](#klasse-commandtree)
   - [Initialisierung (`__init__`)](#initialisierung-init)
   - [Help-Command registrieren (`_register_help`)](#help-command-registrieren-_register_help)
   - [Befehl registrieren (`register`)](#befehl-registrieren-register)
   - [Nachrichten-Handling (`handle`)](#nachrichten-handling-handle)
   - [Help-Ausgabe formatieren](#help-ausgabe-formatieren)
     - [`format_all_help`](#format_all_help)
     - [`format_command_help`](#format_command_help)
   - [Automatische Befehlsentdeckung (`_autodiscover_commands`)](#automatische-befehlsentdeckung-_autodiscover_commands)
5. [Beispielhafte Nutzung](#beispielhafte-nutzung)

---

## Übersicht

`commandtree.py` definiert zwei Kernkomponenten:

- **`Command`**: Repräsentiert einen einzelnen Befehl mit Namen, Callback-Funktion und Hilfetext.
- **`CommandTree`**: Verwaltet alle Befehle, führt sie basierend auf eingehenden Discord-Nachrichten aus und generiert Hilfeausgaben.

---

## Imports und Abhängigkeiten

```python
import pkgutil
import importlib
import inspect
import os
import threading
import time
from typing import Callable, Dict, List, Tuple

from src.core.discord.message import boxed_message_with_title
from src.core.animation.debug_animation import logger as debug_logger
from src.core.animation.running_animation import append_message

try:
    import settings
except ImportError:
    settings = None

prefix = getattr(settings, 'PREFIX', '$') or "$"
```

- `pkgutil`, `importlib`, `inspect`: Für das automatische Laden von Kommandomodulen.
- `boxed_message_with_title`: Erzeugt formatierten Hilfe-Text.
- `debug_logger`, `append_message`: Logging und Statusmeldungen.
- `settings.PREFIX`: Globales Präfix, Standard: `$`.

---

## Klasse `Command`

### Attribute

- `name` (`str`): Befehlsschlüssel, z. B. `"help"`.
- `callback` (`Callable[[Dict, List[str]], str]`): Funktion, die bei Ausführung aufgerufen wird.
- `help_short` (`str`): Kurze Beschreibung für Listenübersicht.
- `help_long` (`str`): Ausführliche Hilfetexte für einzelne Befehle.

### Methoden

#### `execute(self, ctx: Dict, args: List[str]) -> str`

- **Parameter**:
  - `ctx`: Kontextinfo mit `channel_id`, `author_id`, `author_username`.
  - `args`: Liste der Argumente nach dem Befehlsnamen.
- **Verhalten**:
  1. Führt `self.callback(ctx, args)` aus.
  2. Loggt Erfolg oder Fehler.
  3. Bei Ausnahme: Loggt Stacktrace und wirft `RuntimeError`.

---

## Klasse `CommandTree`

Verwaltet Registrierung, Aufruf und Hilfe von Befehlen.

### Initialisierung (`__init__`)

```python
def __init__(self, bot, prefix, logger=None):
    self.bot = bot
    self.prefix = prefix
    self.logger = logger or debug_logger
    self.commands: Dict[str, Command] = {}
    self._register_help()
    self._autodiscover_commands()
```

- `bot`: Discum-Client-Instanz für späteren Zugriff.
- `prefix`: Befehlspräfix.
- `commands`: Dict mapping Befehlsschlüssel → `Command`.
- Ruft Help-Registrierung und automatische Modul-Discovery auf.

### Help-Command registrieren (`_register_help`)

- Legt Standardbefehl `help` an.
- Callback bestimmt anhand übergebener Argumente, ob alle Befehle oder Details zu einem Befehl angezeigt werden.
- Registriert den `Command` via `register`.

### Befehl registrieren (`register`)

```python
def register(self, cmd: Command) -> None:
    key = cmd.name.lower()
    if key in self.commands:
        raise ValueError(f"Command '{key}' bereits registriert")
    self.commands[key] = cmd
```

- Prüft auf Duplikate.
- Fügt neuen Eintrag in `self.commands` ein.

### Nachrichten-Handling (`handle`)

```python
def handle(self, channel_id: str, author: Dict, content: str) -> Tuple[bool, str]:
```

1. Prüft, ob `content` mit `self.prefix` beginnt.
2. Extrahiert `name` und `args` durch Split.
3. Sucht `Command` in `self.commands`.
4. Bei unbekanntem Befehl: Gibt Fehlertext zurück.
5. Baut `ctx`-Dictionary auf.
6. Führt `cmd.execute(ctx, args)` aus und liefert Ergebnis.
7. Bei interner Exception: Loggt und liefert Fehlertext.

### Help-Ausgabe formatieren

#### `format_all_help(self) -> str`

- Generiert Liste aller Befehle mit Kurzbeschreibung.
- Gibt formatiertes Boxed-Message-String zurück.

#### `format_command_help(self, name: str) -> str`

- Sucht `Command` nach Name.
- Bei Nichtvorhandensein: Fehlermeldung.
- Bei Erfolg: Ausführliche Hilfe in Boxed-Format.

### Automatische Befehlsentdeckung (`_autodiscover_commands`)

```python
def _autodiscover_commands(self):
    import src.modules as pkg
    for _, mod_name, _ in pkgutil.walk_packages(pkg.__path__, pkg.__name__ + "."):
        if ".inaktiv." in mod_name: continue
        module = importlib.import_module(mod_name)
        setup_fn = getattr(module, "setup", None)
        if callable(setup_fn):
            setup_fn(self)
```

- Durchsucht Paket `src.modules` rekursiv.
- Überspringt Module mit `.inaktiv.` im Namen.
- Lädt jedes Modul und ruft `setup(self)` auf, wenn vorhanden.
- Erlaubt modulare Erweiterung von Befehlen ohne Änderung von `commandtree.py`.

---

## Beispielhafte Nutzung

1. **Initialisierung**:
   ```python
   tree = CommandTree(bot, prefix="$")
   ```
2. **Eigenen Befehl definieren**:
   ```python
   def ping_callback(ctx, args):
       return "Pong!"
   cmd = Command(
       name="ping",
       callback=ping_callback,
       help_description_short="Antwortet mit Pong",
       help_description_long="Verifiziert die Erreichbarkeit des Bots."
   )
   tree.register(cmd)
   ```
3. **Nachrichten-Event**:
   ```python
   handled, reply = tree.handle(channel_id, author, message_content)
   if handled:
       bot.reply(channel_id, message_id, reply)
   ```

*Ende der Dokumentation*

