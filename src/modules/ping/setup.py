# ---------------------------------------------------------------------------
# src/modules/ping/setup.py
# \author @bastiix
# ---------------------------------------------------------------------------

"""
Dieses Modul zeigt, wie ein einfacher Command für den Selfbot registriert wird.
Es dient gleichzeitig als Tutorial für:
1. Die Struktur eines Modules unter src/modules
2. Die Verwendung von Command, error_message, boxed_message
3. Wie append_message und debug_logger eingebunden werden
4. Best Practices: Docstrings, Logging und Benutzer-Feedback
"""

# Importiere Command-Klasse zum Erstellen neuer Befehle
from src.core.discord.commandtree import Command

# Hilfsfunktionen für Formatierung von Fehlermeldungen und Response-Boxen für Discord Nachrichten
# error_message() erzeugt eine rote Box mit Fehlerhinweis
# boxed_message() erzeugt eine Box mit Titel und Inhalt
# Diese Funktionen sind in der src/core/discord/message.py definiert
from src.core.discord.message import error_message, boxed_message

# Schreiben von Informationen in das Runtime-Log der Console
from src.core.animation.running_animation import append_message

# Debug-Logger für detaillierte Protokollierung im Terminal/Logdatei 
# src/core/animation/debug_animation.py
# debug_logger.debug() schreibt Debug-Informationen in die Logdatei
# debug_logger.{error/warning/debug}() gibt Debug-Informationen in der Console aus wenn DEBUG = True
from src.core.animation.debug_animation import logger as debug_logger

# Standard-Python-Library für Zeitmessung
import time


def setup(command_tree):
    """
    Registriert den `ping`-Command im übergebenen CommandTree.

    Parameter:
        command_tree (CommandTree): Das Core System, in dem alle Commands verwaltet werden.
    """

    def ping_callback(ctx, args):
        """
        Callback-Funktion, die ausgeführt wird, wenn ein Benutzer `$ping` eingibt.

        ctx: Kontext-Dictionary mit Schlüsseln
            - channel_id: ID des Discord-Channels
            - author_id: ID des Benutzers, der den Befehl ausgelöst hat
            - author_username: Der Username (für personalisierte Meldungen)

        args: Liste aller Argumente nach dem Command-Namen (bei `$ping` sollte args leer sein)
        """

        # 1) Informiere im Running-Log über den Start
        #    Dies erscheint in der Console als laufender Status unter "Laufzeit"
        append_message(f"`ping`-Check gestartet von {ctx['author_username']}")

        # 2) Debug-Log: Zeige alle übergebenen Argumente
        #    Nützlich, um später zu prüfen, was genau der Nutzer eingegeben hat
        debug_logger.debug('ping_callback', f"Args: {args}")

        # 3) Validierung: `$ping` darf keine Argumente bekommen
        if args:
            # error_message() liefert eine Box mit rotem Titel
            return error_message("`ping` braucht keine Argumente.")

        # 4) Messen der reinen Antwortzeit
        start_time = time.monotonic()
        # (Hier könnte man echten Netzwerk- oder API-Call testen)
        end_time = time.monotonic()

        # 5) Millisekunden-Berechnung
        latency_ms = int((end_time - start_time) * 1000)

        # 6) Rückgabe als eingerahmte Nachricht (boxed_message)
        #    boxed_message(titel, inhalt) erzeugt eine Discord-Message mit Titel und Inhalt
        return boxed_message(
            "Pong!",
            f"Die Antwortzeit beträgt: {latency_ms} ms"
        )

    # Instanziere den Command mit Name, Callback und Hilfetexten
    cmd_ping = Command(
        name="ping",
        callback=ping_callback,
        help_description_short="Liefert Pong zurück",
        help_description_long=(
            "Einfacher Connectivity-Test.\n"
            "Verwende `$ping`, um die Antwortzeit zu testen.\n"
            "\n"
            "• **Beispiel:** `$ping`\n"
            "• **Ergebnis:** `Pong! Die Antwortzeit beträgt: 5 ms`"
        )
    )

    # Registriere den neuen Command im CommandTree
    command_tree.register(cmd_ping)

    # Hinweis im Debug-Log/Print, dass setup() durchgelaufen ist
    debug_logger.debug('ping.setup', "Der `ping`-Command wurde registriert")
