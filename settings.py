# ---------------------------------------------------------------------------
# \settings.py
# \author @bastiix
# ---------------------------------------------------------------------------

DEBUG = False                                       # Debug-Mode (True/False) Prettymode = DEBUGMODE FALSE
LOGGING = True                                      # Logging-Mode (True/False) 
PREFIX = "$"
LOGIN_EMAIL = ""                                    # leer lassen wenn login manuell eingegeben werden soll
LOGIN_PASSWORD = ""                                 # leer lassen wenn login manuell eingegeben werden soll

ALLLOWED_USERS = ("514907234644393996",             # Bastixx
                  "488449454094155777",             # Dani Main
                  "908467731840532521",             # Dani second
                  "470936841345040384"              # Fabii
                  )
MAINCOLOR   = "\033[1;36m"                          # Hauptfarbe
SECONDCOLOR = "\033[94m"                            # Sekundärfarbe       
STAMPCOLOR  = "\033[1;33m"                          # Zeitstempel-Farbe
RESETCOLOR  = "\033[0m"                             # Reset-Farbe 

MAX_CHUNK_SIZE = 2000                               # Maximaler Chunk-Size für Discord-Nachrichten

SELFBOT_DUMP_CHANNEL = "1363982514993238037"        # Discord Dump Channel ID



# SYSTEM-Variablen

import os
import platform
import subprocess

_PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
_SYSTEM_DIR   = os.path.join(_PROJECT_ROOT, 'src', 'core', 'system')

RESTART_DEBUG_MODE_PATH_WINDOWS = os.path.join(_SYSTEM_DIR, 'restart_debug.bat')
RESTART_DEBUG_MODE_PATH_LINUX   = os.path.join(_SYSTEM_DIR, 'restart_debug.sh')

def spawn_restart():
    system = platform.system().lower()
    if system.startswith('win'):
        script = RESTART_DEBUG_MODE_PATH_WINDOWS
        return subprocess.call([script])
    elif system.startswith('linux') or system.startswith('darwin'):
        script = RESTART_DEBUG_MODE_PATH_LINUX
        return subprocess.call(['sh', script])
    else:
        raise RuntimeError(f"Unbekanntes Betriebssystem: {platform.system()}")