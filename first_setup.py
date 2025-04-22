#!/usr/bin/env python3
# ---------------------------------------------------------------------------
# first_setup.py
# \author @bastiix
# ---------------------------------------------------------------------------
import subprocess
import sys
import os
import platform
import shutil
import time
from datetime import datetime
import settings

# Farbdefinitionen
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
    if not settings.DEBUG:
        width = len(text) + 2
        frame_top    = f"\n╔{'═' * width}╗"
        frame_middle = f"║ {text} ║"
        frame_bottom = f"╚{'═' * width}╝"

        print(f"{COLOR_MAIN}{frame_top}{RESET}")
        print(f"{COLOR_MAIN}{frame_middle}{RESET}")
        print(f"{COLOR_MAIN}{frame_bottom}{RESET}")


def append_message(message: str) -> None:
    if not settings.DEBUG:
        ts = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        info = f"   ↳ {TIME_COLOR}{ts}{RESET} | {SECOND_COLOR}{message}{RESET}"
        typewriter_print(info)


def main():
    venv_dir = 'venv'

    # Erstes Banner
    print_banner('Erstes setup gestartet')
    append_message('venv wird aufgesetzt..')
    subprocess.check_call([sys.executable, '-m', 'venv', venv_dir])
    append_message('venv erfolgreich aufgesetzt.')

    append_message('lese requirements.txt')
    # Filter out leere Zeilen und Kommentare
    with open('requirements.txt', 'r') as f:
        packages = [line.strip() for line in f if line.strip() and not line.strip().startswith('#')]

    pip_executable = os.path.join(
        venv_dir,
        'Scripts' if os.name == 'nt' else 'bin',
        'pip.exe' if os.name == 'nt' else 'pip'
    )

    for pkg in packages:
        append_message(f"installiere {pkg}")
        # Pip-Ausgabe unterdrücken
        subprocess.check_call(
            [pip_executable, 'install', pkg],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        append_message(f"{pkg} installiert")

    append_message('Alle Pakete installiert.')
    os_name = platform.system()
    append_message(f"Betriebssystem {os_name} erkannt.")

    print_banner('Das initiale setup ist abgeschlossen.')

    # Benutzerabfrage
    append_message('Willst du dass die vorgenommenen Änderungen übernommen werden? {Y/N}')
    choice = input().strip().lower()
    if choice == 'y':
        print_banner('Alle änderungen übernommen.')
        cmd = (
            f"{venv_dir}\\Scripts\\activate.bat" if os.name == 'nt'
            else f"source {venv_dir}/bin/activate"
        )
        append_message(f"Führe {cmd} aus um die Umgebung zu aktivieren.")
        append_message('Starte den Bot mit "python main.py"')
        append_message('Drücke Enter zum Beenden...')
        input()
    else:
        print_banner('Prozess wird abgebrochen')
        append_message('Lösche die installierten Pakete...')
        subprocess.check_call(
            [pip_executable, 'uninstall', '-r', 'requirements.txt', '-y'],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        append_message('Lösche den venv Ordner..')
        shutil.rmtree(venv_dir)
        append_message('Alle Vorgänge rückgängig gemacht')
        append_message('Drücke Enter zum Beenden...')
        input()


if __name__ == '__main__':
    main()
