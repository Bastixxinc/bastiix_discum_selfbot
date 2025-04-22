# ---------------------------------------------------------------------------
# \src\core\animation\pretty_animation.py
# \author @bastiix
# ---------------------------------------------------------------------------
 
import sys
import time
from datetime import datetime

try:
    import settings
except ImportError:
    settings = type("S", (), {"DEBUG": True})


CYAN   = "\033[1;36m"
YELLOW = "\033[1;33m"
BLUE   = "\033[94m"
RESET  = settings.RESETCOLOR or "\033[0m"

def typewriter_print(text: str, delay: float = 0.05):
    """
    Gibt Text im Typewriter-Stil aus, wenn DEBUG aktiv.
    """
    if not settings.DEBUG:
        return
    for ch in text:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write("\n")
    sys.stdout.flush()

def pretty_banner(
    banner_text: str,
    completion_title: str,
    completion_message: str,
    pulse_cycles: int = 4,
    pulse_delay: float = 0.35,
    type_delay: float = 0.015
):
    if settings.DEBUG is True:
        return

    ts = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    text = banner_text
    width = len(text) + 2

    frame_top    = f"╔{'═'*width}╗"
    frame_mid    = f"║ {text} ║"
    frame_bottom = f"╚{'═'*width}╝"
    frames = [frame_top, frame_mid, frame_bottom]

    sys.stdout.write("\033[?25l")
    sys.stdout.flush()
    try:
        for _ in range(pulse_cycles):
            for color in (CYAN, BLUE):
                for line in frames:
                    print(f"{color}{line}{RESET}")
                time.sleep(pulse_delay)
                sys.stdout.write("\033[F" * len(frames))

        for line in frames:
            print(f"{CYAN}{line}{RESET}")
        print() 

        border = "═" * (len(completion_title) + 4)
        print(f"\n╔{border}╗")
        print(f"║  {CYAN}{completion_title}{RESET}  ║")
        print(f"╚{border}╝")

        info = f"   ↳ {YELLOW}{ts}{RESET} | {BLUE}{completion_message}{RESET}"
        typewriter_print(info, delay=type_delay)

    finally:
        sys.stdout.write("\033[?25h")
        sys.stdout.flush()
