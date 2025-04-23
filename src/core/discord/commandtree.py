# ---------------------------------------------------------------------------
# \src\core\discord\commandtree.py
# \author @bastiix
# ---------------------------------------------------------------------------
import pkgutil
import importlib
import inspect
from typing import Callable, Dict, List, Tuple

from src.core.discord.message import boxed_message_with_title
from src.core.animation.debug_animation import logger as debug_logger

try:
    import settings
except ImportError:
    settings = None

prefix = getattr(settings, 'PREFIX', '$')

_raw_allowed = None
if settings:
    _raw_allowed = getattr(settings, 'ALLOWED_USERS', None) or getattr(settings, 'ALLLOWED_USERS', None)

if _raw_allowed:
    if isinstance(_raw_allowed, str):
        ALLOWED_USERS = [u.strip() for u in _raw_allowed.split(',') if u.strip()]
    elif isinstance(_raw_allowed, (list, tuple)):
        ALLOWED_USERS = [str(u) for u in _raw_allowed]
    else:
        ALLOWED_USERS = None
else:
    ALLOWED_USERS = None


class Command:
    def __init__(
        self,
        name: str,
        callback: Callable[[Dict, List[str]], str],
        help_description_short: str,
        help_description_long: str
    ):
        debug_logger.debug(
            'Command.__init__',
            f"Initialisiere Command: name={name}, callback={callback}, help_short={help_description_short}"
        )
        self.name = name
        self.callback = callback
        self.help_short = help_description_short
        self.help_long = help_description_long

    def execute(self, ctx: Dict, args: List[str]) -> str:
        debug_logger.debug(
            'Command.execute',
            f"Führe Command '{self.name}' aus mit ctx={ctx} und args={args}"
        )
        try:
            result = self.callback(ctx, args) or ""
            debug_logger.debug(
                'Command.execute',
                f"Command '{self.name}' erfolgreich ausgeführt, Ergebnis={result!r}"
            )
            return result
        except Exception as e:
            debug_logger.error(
                'Command.execute',
                f"Fehler im Command '{self.name}': {e}",
                exc_info=True
            )
            raise RuntimeError(f"Fehler im Command '{self.name}': {e}") from e


class CommandTree:
    def __init__(self, bot, prefix, logger=None):
        debug_logger.debug(
            'CommandTree.__init__',
            f"Initialisiere CommandTree mit prefix={prefix}, bot={bot}"
        )
        self.bot = bot
        self.prefix = prefix
        self.logger = logger or debug_logger
        self.commands: Dict[str, Command] = {}
        self.allowed_users = ALLOWED_USERS

        self.logger.debug('CommandTree.__init__', "Registriere Help-Command")
        self._register_help()
        self.logger.debug('CommandTree.__init__', "Suche automatisch nach Commands")
        self._autodiscover_commands()
        self.logger.debug('CommandTree.__init__', "CommandTree-Initialisierung abgeschlossen")

    def _register_help(self):
        debug_logger.debug('_register_help', "Help-Command wird eingerichtet")

        def help_callback(ctx, args):
            debug_logger.debug('help_callback', f"Help aufgerufen mit args={args}")
            if not args:
                debug_logger.debug('help_callback', "Keine Argumente, generiere Übersicht aller Befehle")
                return self.format_all_help()
            debug_logger.debug('help_callback', f"Argument vorhanden, generiere Hilfe für Command {args[0]}")
            return self.format_command_help(args[0])

        help_cmd = Command(
            name="help",
            callback=help_callback,
            help_description_short="Zeigt Übersicht aller Befehle",
            help_description_long=(
                "Ohne Argument zeigt `!help` alle Befehle mit kurzer Beschreibung.\n"
                "Mit `!help <Befehl>` Details zu genau diesem Befehl."
            )
        )
        try:
            self.register(help_cmd)
            debug_logger.debug('_register_help', "Help-Command erfolgreich registriert")
        except Exception as e:
            debug_logger.error('_register_help', f"Help-Registration fehlgeschlagen: {e}", exc_info=True)

    def register(self, cmd: Command) -> None:
        key = cmd.name.lower()
        debug_logger.debug('CommandTree.register', f"Versuche, Command '{key}' zu registrieren")
        if key in self.commands:
            debug_logger.error('CommandTree.register', f"Command '{key}' ist bereits registriert")
            raise ValueError(f"Command '{key}' bereits registriert")
        self.commands[key] = cmd
        debug_logger.debug('CommandTree.register', f"'{key}' registriert (Kurzbeschreibung: {cmd.help_short})")

    def handle(
        self,
        channel_id: str,
        author: Dict,
        content: str
    ) -> Tuple[bool, str]:
        debug_logger.debug(
            'CommandTree.handle',
            f"Verarbeite Nachricht in channel={channel_id} von author={author} -> content={content!r}"
        )
        name = None
        try:
            if not content.startswith(self.prefix):
                debug_logger.debug('CommandTree.handle', "Nachricht beginnt nicht mit Prefix, ignoriere")
                return False, ""

            author_id = str(author.get("id"))
            if self.allowed_users is not None and author_id not in self.allowed_users:
                debug_logger.debug(
                    'CommandTree.handle',
                    f"Author {author_id} nicht in erlaubten Benutzern, ignoriere"
                )
                return False, ""

            parts = content[len(self.prefix):].split()
            debug_logger.debug('CommandTree.handle', f"Geparste Teile: {parts}")
            if not parts:
                debug_logger.debug('CommandTree.handle', "Kein Command nach Prefix, ignoriere")
                return False, ""

            name = parts[0].lower()
            args = parts[1:]
            debug_logger.debug('CommandTree.handle', f"Command-Name='{name}', args={args}")

            cmd = self.commands.get(name)
            if not cmd:
                debug_logger.warning('CommandTree.handle', f"Unbekannter Befehl: {name}")
                return True, f"Unbekannter Befehl: `{self.prefix}{name}`. Probiere `{self.prefix}help`"

            ctx = {
                "channel_id": channel_id,
                "author_id": author_id,
                "author_username": author.get("username", "unknown")
            }
            debug_logger.debug('CommandTree.handle', f"Ausführungskontext: {ctx}")

            result = cmd.execute(ctx, args)
            debug_logger.debug('CommandTree.handle', f"Command '{name}' lieferte Ergebnis: {result!r}")
            return True, result

        except Exception as e:
            debug_logger.error('CommandTree.handle', f"Ausnahme bei `{self.prefix}{name}`: {e}", exc_info=True)
            return True, f"Fehler beim Ausführen von `{self.prefix}{name}`: {e}"

    def format_all_help(self) -> str:
        debug_logger.debug('format_all_help', "Generiere komplette Hilfeübersicht")
        try:
            lines = ["Verfügbare Befehle:"]
            for name, cmd in sorted(self.commands.items()):
                debug_logger.debug('format_all_help', f"Füge Hilfeeintrag für '{name}' hinzu")
                lines.append(f"- `{self.prefix}{name}`: {cmd.help_short}")
            body = "\n".join(lines)
            debug_logger.debug('format_all_help', "Hilfeübersicht erstellt")
            return boxed_message_with_title("Hilfe Übersicht", body)
        except Exception as e:
            debug_logger.error('format_all_help', str(e), exc_info=True)
            return boxed_message_with_title("Fehler", "Hilfe konnte nicht generiert werden.")

    def format_command_help(self, name: str) -> str:
        debug_logger.debug('format_command_help', f"Generiere Hilfe für Command '{name}'")
        try:
            cmd = self.commands.get(name.lower())
            if not cmd:
                debug_logger.warning('format_command_help', f"Kein Hilfetext für '{name}' gefunden")
                return boxed_message_with_title("Fehler", f"Kein Hilfetext für `{self.prefix}{name}` gefunden.")
            debug_logger.debug('format_command_help', f"Command '{name}' gefunden, liefere detaillierte Hilfe")
            return boxed_message_with_title(f"Hilfe: {self.prefix}{cmd.name}", cmd.help_long)
        except Exception as e:
            debug_logger.error('format_command_help', str(e), exc_info=True)
            return boxed_message_with_title("Fehler", "Befehls-Hilfe konnte nicht generiert werden.")

    def _autodiscover_commands(self):
        debug_logger.debug('_autodiscover_commands', "Starte automatische Entdeckung der Module")
        try:
            import src.modules as pkg
        except ModuleNotFoundError:
            debug_logger.warning('_autodiscover_commands', "Paket src.modules nicht gefunden")
            return

        for _, mod_name, _ in pkgutil.walk_packages(pkg.__path__, pkg.__name__ + "."):
            debug_logger.debug('_autodiscover_commands', f"Untersuche Modul: {mod_name}")
            if ".inaktiv." in mod_name or mod_name.endswith(".inaktiv"):
                debug_logger.debug('_autodiscover_commands', f"Überspringe inaktives Modul: {mod_name}")
                continue
            try:
                debug_logger.debug('_autodiscover_commands', f"Lade Modul: {mod_name}")
                module = importlib.import_module(mod_name)
                setup_fn = getattr(module, "setup", None)
                if callable(setup_fn) and inspect.isfunction(setup_fn):
                    debug_logger.debug('_autodiscover_commands', f"setup() in {mod_name} gefunden, rufe auf")
                    setup_fn(self)
                    debug_logger.debug('_autodiscover_commands', f"setup() für {mod_name} abgeschlossen")
                else:
                    debug_logger.debug('_autodiscover_commands', f"Kein setup() in {mod_name}, überspringe")
            except Exception as e:
                debug_logger.error(
                    '_autodiscover_commands',
                    f"Fehler beim Import/Setup {mod_name}: {e}",
                    exc_info=True
                )

        debug_logger.debug('_autodiscover_commands', "Automatische Command-Entdeckung abgeschlossen")
