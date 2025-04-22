# ---------------------------------------------------------------------------
# \src\core\animation\running_animation.py
# ---------------------------------------------------------------------------

import sys
import time
from datetime import datetime

try:
    import settings
except ImportError:
    settings = type("S", (), {"DEBUG": True})

COLOR_MAIN      = settings.MAINCOLOR or "\033[1;34m"
TIME_COLOR      = settings.STAMPCOLOR or "\033[1;32m"
SECOND_COLOR    = settings.SECONDCOLOR or "\033[1;33m"
RESET           = settings.RESETCOLOR or "\033[0m"

def typewriter_print(text: str, delay: float = 0.01) -> None:
    for ch in text:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write("\n")
    sys.stdout.flush()

def print_banner(text: str) -> None:
    if settings.DEBUG is False:
        width = len(text) + 2
        frame_top    = f"\n╔{'═' * width}╗"
        frame_middle = f"║ {text} ║"
        frame_bottom = f"╚{'═' * width}╝"

        print(f"{COLOR_MAIN}{frame_top}{RESET}")
        print(f"{COLOR_MAIN}{frame_middle}{RESET}")
        print(f"{COLOR_MAIN}{frame_bottom}{RESET}")
    else:
        return

def append_message(message: str) -> None:
    if settings.DEBUG is False:
        ts = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        info = f"   ↳ {TIME_COLOR}{ts}{RESET} | {SECOND_COLOR}{message}{RESET}"
        typewriter_print(info)
    else:
        return