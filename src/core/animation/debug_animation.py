# ---------------------------------------------------------------------------
# \src\core\animation\debug_animation.py
# \author @bastiix
# ---------------------------------------------------------------------------
import os
import re
import atexit
import shutil
import textwrap
from datetime import datetime

try:
    import settings
except ImportError:
    settings = type("S", (), {"DEBUG": True, "LOGGING": True})

# ANSI‐Farbcodes
_TS_COLOR    = "\033[94m"
_DEBUG_COLOR = "\033[1;36m"
_WARN_COLOR  = "\033[33m"
_ERROR_COLOR = "\033[1;31m"
_RESET       = settings.RESETCOLOR or "\033[0m"

_ANSI_ESCAPE_RE = re.compile(r'\x1b\[[0-9;]*m')

class DebugConsole:
    def __init__(self):
        self._debug_count = 0
        self._warn_count  = 0
        self._error_count = 0

        self.debug_enabled   = getattr(settings, "DEBUG", False)
        self.logging_enabled = getattr(settings, "LOGGING", False)
        self._log_fp         = None

        if self.logging_enabled:
            base_log_dir = os.path.join(os.getcwd(), "log", "debug")
            os.makedirs(base_log_dir, exist_ok=True)
            fname = datetime.now().strftime("%Y%m%d_%H%M%S") + ".txt"
            self._log_fp = open(os.path.join(base_log_dir, fname), "a", encoding="utf-8")
            atexit.register(self._close_log)

    def _close_log(self):
        if self._log_fp:
            self._log_fp.close()
            self._log_fp = None

    def _strip_ansi(self, text: str) -> str:
        return _ANSI_ESCAPE_RE.sub("", text)

    def _log_line(self, line: str):
        if self.logging_enabled and self._log_fp:
            self._log_fp.write(self._strip_ansi(line) + "\n")

    def _print_message(self, level_name: str, count: int, fn: str, msg: str, color: str):
        if not self.debug_enabled:
            return

        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        header = f"{_TS_COLOR}{ts}{_RESET}"
        tag    = f"{color}[{level_name}#{count}]{_RESET}"
        fncol  = f"{_DEBUG_COLOR}{fn}{_RESET}"
        raw    = f"{ts} [{level_name}#{count}] {fn}"

        width  = shutil.get_terminal_size((80, 20)).columns
        if len(raw) > width - 4:
            raw = raw[: width - 4]

        pad       = " " * (len(raw) - len(raw.rstrip()))
        arrow     = " → "
        prefix    = f"{header} {tag} {fncol}{pad}{arrow}"
        indent    = len(self._strip_ansi(prefix))

        wrapper = textwrap.TextWrapper(
            width=width,
            initial_indent=prefix,
            subsequent_indent=" " * indent,
            replace_whitespace=False,
            drop_whitespace=False
        )

        for paragraph in msg.split("\n"):
            for line in wrapper.wrap(paragraph):
                print(line)
                self._log_line(line)

    def debug(self, fn: str, msg: str):
        self._debug_count += 1
        self._print_message("DEBUG", self._debug_count, fn, msg, _DEBUG_COLOR)

    def warning(self, fn: str, msg: str):
        self._warn_count += 1
        self._print_message("WARNUNG", self._warn_count, fn, msg, _WARN_COLOR)

    warn = warning

    def error(self, fn: str, msg: str):
        self._error_count += 1
        self._print_message("FEHLER", self._error_count, fn, msg, _ERROR_COLOR)

logger = DebugConsole()
