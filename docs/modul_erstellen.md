# Modul-Erstellung für den Bastiix Selfbot
Diese Dokumentation erklärt, wie du selbst ein Modul für den Selfbot erstellst. Sie zeigt Schritt für Schritt:

- Wie Module aufgebaut und im `CommandTree` registriert werden
- Wie du **zwei Hilfebeschreibungen** bei Commands angibst
- Wie du verschiedene Nachrichtentypen aus `message.py` nutzt
- Wie du laufende Ausgaben und Debug-Logs korrekt verschickst
- Wie das Senden von Nachrichten funktioniert

---

## 1. Ordner- und Dateistruktur

Lege dein Modul in `src/modules/<dein_modul>/`. Die Mindeststruktur:

```
src/modules/
└── mein_modul/
    ├── __init__.py   # Damit Python den Ordner als Package erkennt
    └── setup.py      # Enthält die setup()-Funktion (kann auch anders beannt werden)
```

## 2. Die `setup()`-Funktion
Jedes Modul muss eine Funktion `setup(command_tree)` exportieren. Darin registrierst du deine Commands.

```python
# src/modules/mein_modul/setup.py
from src.core.discord.commandtree import Command
from src.core.discord.message import (
    success_message, info_message, error_message,
    boxed_message_with_title, inline_message_with_title,
    warning_message, debug_message, syntax_message,
    list_message, question_message, spoiler_message,
    embed_like_message
)
from src.core.animation.running_animation import append_message
from src.core.animation.debug_animation import logger as debug_logger


def setup(command_tree):
    """
    Registriert alle Commands für dieses Modul.
    """
    # Beispiel-Command registrieren
    def hallo_callback(ctx, args):
        # Laufende Ausgaben (kein Debug):
        append_message("`hallo`-Befehl aufgerufen von {user}".format(user=ctx['author_username']))

        # Debug-Level-Log:
        debug_logger.debug('hallo_callback', f"Args: {args}")

        if not args:
            return info_message("Bitte gib deinen Namen an: `$hallo <Name>`")
        name = args[0]
        return success_message(f"Hallo, {name}!")

    cmd = Command(
        name="hallo",
        callback=hallo_callback,
        help_description_short="Sagt Hallo",
        help_description_long=(
            "Verwendet `$hallo <Name>` um den Bot deinen Namen sagen zu lassen.\n"
            "Beispiel: `$hallo Alice`"
        )
    )
    command_tree.register(cmd)
```

### 2.1 Zwei Hilfebeschreibungen & Automatisierter Console Notify
- **help_description_short**: Kurze Zeile (max. 80 Zeichen), die in der Übersicht angezeigt wird.
- **help_description_long**: Ausführliche Beschreibung, die bei `$help <Command>` erscheint.
- Der **CommandTree** registriert wenn ein Befehl ausgeführt wird und printet im Debug und Pretty Mode eine Info.

## 3. Nachrichten-Typen aus `message.py`
Die Rückgabe eines Command-Callbacks ist immer ein `str`, der an Discord gesendet wird. Hier eine Übersicht aller Typen:

| Funktion                        | Zweck                                                 | Beispiel                                             |
|---------------------------------|-------------------------------------------------------|------------------------------------------------------|
| `boxed_message_with_title`      | Block mit Überschrift                                | ``` boxed_message_with_title("Titel", "Text")``` |
| `inline_message_with_title`     | Ungelockter Inline-Block                              | ``` inline_message_with_title("Ttl","Body")```   |
| `success_message`               | Grün mit + SUCCESS                                    | ``` success_message("Erfolg") ```                  |
| `success_message_boxed`         | Boxed grün                                            | ``` success_message_boxed("Ttl","Msg")```        |
| `info_message`                  | `[ INFO ]`                                            | ``` info_message("Info") ```                       |
| `info_message_boxed`            | Boxed `[ INFO ]`                                      | ``` info_message_boxed("Ttl","Msg")```           |
| `warning_message`               | Gelb mit - WARNING                                    | ``` warning_message("Warnung") ```                 |
| `warning_message_boxed`         | Boxed gelb                                            | ``` warning_message_boxed("Ttl","Msg")```        |
| `error_message`                 | Rot mit - ERROR                                       | ``` error_message("Fehler") ```                    |
| `error_message_with_title`      | Rot mit Überschrift                                   | ``` error_message_with_title("Ttl","Msg")```     |
| `error_message_with_title_and_correction` | Rot mit Korrektur                        | ``` error_message_with_title_and_correction("Ttl","Msg","Fix")``` |
| `debug_message`                 | Rot SCI-Format                                        | ``` debug_message("Text") ```                      |
| `debug_message_boxed`           | Boxing als DEBUG                                      | ``` debug_message_boxed("Ttl","Msg")```         |
| `question_message`              | Fix-Format für Fragen                                 | ``` question_message("?</?>") ```                  |
| `syntax_message`                | Code-Block mit Syntax                                  | ``` syntax_message("py","print()") ```           |
| `list_message`                  | Nummerierte Liste                                      | ``` list_message("Ttl", ["a","b"]) ```         |
| `spoiler_message`               | Spoiler-Tags                                           | ``` spoiler_message("geheim") ```                  |
| `embed_like_message`            | **falsches** Embed mit Titel und Text                  | ``` embed_like_message("Ttl","Desc","Ftr")```  |

### 3.1 Verwendung im Callback
```python
# return einer Tabelle
return boxed_message_with_title(
    "Überschrift",
    "- Punkt 1\n- Punkt 2"
)
```


## 4. Laufende Ausgaben vs. Debug-Logs
- **Laufende Ausgaben** (Pretty Mode) werden mit `append_message(text)` aus `running_animation.py` ausgegeben. Diese erscheinen als gelockerte Banner-Ausgaben während der Runtime.
- **Debug-Logs** (Detailinfos, Warnungen, Fehler) schickst du an `debug_logger` aus `debug_animation.py`:
  - `debug_logger.debug(fn_name, msg)`
  - `debug_logger.warning(fn_name, msg)` oder `debug_logger.warn(...)`
  - `debug_logger.error(fn_name, msg)`

> Der Logger entscheidet anhand der `settings.DEBUG` und `settings.LOGGING`, ob Log-Einträge nur in Datei landen oder auf der Konsole ausgegeben werden.


## 5. Senden von Nachrichten
Innerhalb eines Command-Callbacks gibst du einfach den String zurück. Der Selfbot kümmert sich um:

1. `typingAction`-Event schicken
2. Nachricht senden (reagiert auf Länge automatisch mit Chunks)

**Wichtig:** Du musst nicht selbst `bot.sendMessage()`, sondern nur den Rückgabewert setzen.


## 6. Beispiel-Komplettes Modul

```python
# src/modules/mein_modul/setup.py
from settings import PREFIX as prefix
from src.core.discord.commandtree import Command
from src.core.discord.message import (
    success_message, error_message, info_message, syntax_message
)
from src.core.animation.running_animation import append_message
from src.core.animation.debug_animation import logger as debug_logger

def setup(command_tree):
    def ping(ctx, args):
        append_message("`ping`-Check gestartet")
        debug_logger.debug('ping', 'Args: %s' % args)
        if args:
            return error_message("`ping` braucht keine Argumente.")
        return boxed_message("Pong!", "Ich habe Reagiert!")

    cmd_ping = Command(
        name="ping",
        callback=ping,
        help_description_short="Liefert Pong zurück",
        help_description_long=(
            "Einfacher Connectivity-Test.\n"
            f"Verwende `{prefix}ping`, um die Antwortzeit zu testen."
        )
    )
    command_tree.register(cmd_ping)
```

---

Mit dieser Vorlage kannst du **beliebig viele** Commands in deinem Modul definieren. Achte auf:

1. Korrektes Importieren der Utilities (`append_message`, `debug_logger`, Nachrichten-Funktionen)
2. Registrierung via `command_tree.register(...)`
3. Rückgabe eines formatierten Strings
4. Ausführliche Hilfetexte

Viel Erfolg beim Erstellen deiner eigenen Module! 🎉

*Dieses Readme ist teilweise KI Generiert.* ~@bastiix