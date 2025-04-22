# ---------------------------------------------------------------------------
# \src\core\discord\commandtree.py
# ---------------------------------------------------------------------------
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


class Command:
    def __init__(
        self,
        name: str,
        callback: Callable[[Dict, List[str]], str],
        help_description_short: str,
        help_description_long: str
    ):
        debug_logger.debug('Command.__init__', f"Initializing Command: name={name}, callback={callback}, "
                                                f"help_short={help_description_short}")
        self.name = name
        self.callback = callback
        self.help_short = help_description_short
        self.help_long = help_description_long

    def execute(self, ctx: Dict, args: List[str]) -> str:
        debug_logger.debug('Command.execute', f"About to execute command '{self.name}' with ctx={ctx} and args={args}")
        try:
            result = self.callback(ctx, args) or ""
            debug_logger.debug('Command.execute', f"Command '{self.name}' executed successfully, result={result!r}")
            return result
        except Exception as e:
            debug_logger.error('Command.execute', f"Error in command '{self.name}': {e}", exc_info=True)
            raise RuntimeError(f"Fehler im Command '{self.name}': {e}") from e


class CommandTree:
    def __init__(self, bot, prefix, logger=None):
        debug_logger.debug('CommandTree.__init__', f"Initializing CommandTree with prefix={prefix}, bot={bot}")
        self.bot = bot
        self.prefix = prefix
        self.logger = logger or debug_logger
        self.commands: Dict[str, Command] = {}
        self.logger.debug('CommandTree.__init__', "Registering help command")
        self._register_help()
        self.logger.debug('CommandTree.__init__', "Autodiscovering commands")
        self._autodiscover_commands()
        self.logger.debug('CommandTree.__init__', "CommandTree initialization complete")

    def _register_help(self):
        debug_logger.debug('_register_help', "Setting up help command")
        def help_callback(ctx, args):
            debug_logger.debug('help_callback', f"help called with args={args}")
            if not args:
                debug_logger.debug('help_callback', "No args provided, formatting all help")
                return self.format_all_help()
            debug_logger.debug('help_callback', f"Arg provided, formatting help for command {args[0]}")
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
            debug_logger.debug('_register_help', "Help command registered successfully")
        except Exception as e:
            debug_logger.error('_register_help', f"Help-Registration fehlgeschlagen: {e}", exc_info=True)

    def register(self, cmd: Command) -> None:
        key = cmd.name.lower()
        debug_logger.debug('CommandTree.register', f"Attempting to register command '{key}'")
        if key in self.commands:
            debug_logger.error('CommandTree.register', f"Command '{key}' bereits registriert")
            raise ValueError(f"Command '{key}' bereits registriert")
        self.commands[key] = cmd
        debug_logger.debug('CommandTree.register', f"'{key}' registriert (kurz: {cmd.help_short})")

    def handle(
        self,
        channel_id: str,
        author: Dict,
        content: str
    ) -> Tuple[bool, str]:
        debug_logger.debug('CommandTree.handle', f"Handling message in channel={channel_id} from author={author} -> content={content!r}")
        name = None
        try:
            if not content.startswith(self.prefix):
                debug_logger.debug('CommandTree.handle', "Message does not start with prefix, ignoring")
                return False, ""
            parts = content[len(self.prefix):].split()
            debug_logger.debug('CommandTree.handle', f"Parsed parts: {parts}")
            if not parts:
                debug_logger.debug('CommandTree.handle', "No command after prefix, ignoring")
                return False, ""
            name = parts[0].lower()
            args = parts[1:]
            debug_logger.debug('CommandTree.handle', f"Command name='{name}', args={args}")
            cmd = self.commands.get(name)
            if not cmd:
                debug_logger.warn('CommandTree.handle', f"Unbekannter Befehl: {name}")
                return True, f"Unbekannter Befehl: `{self.prefix}{name}`. Probiere `{self.prefix}help`"

            ctx = {
                "channel_id": channel_id,
                "author_id": author.get("id"),
                "author_username": author.get("username", "unknown")
            }
            debug_logger.debug('CommandTree.handle', f"Context for execution: {ctx}")

            # Befehl ausführen
            result = cmd.execute(ctx, args)
            debug_logger.debug('CommandTree.handle', f"Command '{name}' returned result: {result!r}")
            return True, result

        except Exception as e:
            debug_logger.error('CommandTree.handle', f"Exception beim `{self.prefix}{name}`: {e}", exc_info=True)
            return True, f"Fehler beim Ausführen von `{self.prefix}{name}`: {e}"

    def format_all_help(self) -> str:
        debug_logger.debug('format_all_help', "Generating full help overview")
        try:
            lines = ["Verfügbare Befehle:"]
            for name, cmd in sorted(self.commands.items()):
                debug_logger.debug('format_all_help', f"Adding help entry for '{name}'")
                lines.append(f"- `{self.prefix}{name}`: {cmd.help_short}")
            body = "\n".join(lines)
            debug_logger.debug('format_all_help', "Full help body generated")
            return boxed_message_with_title("Hilfe Übersicht", body)
        except Exception as e:
            debug_logger.error('format_all_help', str(e), exc_info=True)
            return boxed_message_with_title("Fehler", "Hilfe konnte nicht generiert werden.")

    def format_command_help(self, name: str) -> str:
        debug_logger.debug('format_command_help', f"Generating help for command '{name}'")
        try:
            cmd = self.commands.get(name.lower())
            if not cmd:
                debug_logger.warning('format_command_help', f"No help found for '{name}'")
                return boxed_message_with_title("Fehler", f"Kein Hilfetext für `{self.prefix}{name}` gefunden.")
            debug_logger.debug('format_command_help', f"Found command '{name}', returning detailed help")
            return boxed_message_with_title(f"Hilfe: {self.prefix}{cmd.name}", cmd.help_long)
        except Exception as e:
            debug_logger.error('format_command_help', str(e), exc_info=True)
            return boxed_message_with_title("Fehler", "Befehls-Hilfe konnte nicht generiert werden.")

    def _autodiscover_commands(self):
        debug_logger.debug('_autodiscover_commands', "Starting automatic discovery of command modules")
        try:
            import src.modules as pkg
        except ModuleNotFoundError:
            debug_logger.warning('_autodiscover_commands', "Package src.modules nicht gefunden")
            return

        for _, mod_name, _ in pkgutil.walk_packages(pkg.__path__, pkg.__name__ + "."):
            debug_logger.debug('_autodiscover_commands', f"Inspecting module: {mod_name}")
            if ".inaktiv." in mod_name or mod_name.endswith(".inaktiv"):
                debug_logger.debug('_autodiscover_commands', f"Skipping inactive module: {mod_name}")
                continue
            try:
                debug_logger.debug('_autodiscover_commands', f"Loading module: {mod_name}")
                module = importlib.import_module(mod_name)
                setup_fn = getattr(module, "setup", None)
                if callable(setup_fn) and inspect.isfunction(setup_fn):
                    debug_logger.debug('_autodiscover_commands', f"Found setup() in {mod_name}, calling it")
                    setup_fn(self)
                    debug_logger.debug('_autodiscover_commands', f"setup() completed for {mod_name}")
                else:
                    debug_logger.debug('_autodiscover_commands', f"No setup() in {mod_name}, skipping")
            except Exception as e:
                debug_logger.error(
                    '_autodiscover_commands',
                    f"Fehler beim Import/Setup {mod_name}: {e}",
                    exc_info=True
                )

        debug_logger.debug('_autodiscover_commands', "Command autodiscovery complete")
