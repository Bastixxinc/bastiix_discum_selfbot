# ---------------------------------------------------------------------------
# \main.py
# ---------------------------------------------------------------------------

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import sys
import re
import time
import traceback
import subprocess
import threading
import asyncio
import atexit
from datetime import datetime

# Selenium imports
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException, TimeoutException as SeleniumTimeout
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

# Discord client
import discum
try:
    from discum import DiscordError
except ImportError:
    DiscordError = Exception

# Project imports
from src.core.discord.commandtree import CommandTree
from src.core.discord.message import error_message
from src.core.discord.chameleon_mask import mask as apply_chameleon_mask

# Animation & logging utilities
from src.core.animation.debug_animation import logger as debug_logger
from src.core.animation.running_animation import print_banner, append_message
from src.core.animation.pretty_animation import pretty_banner, CYAN, YELLOW, BLUE, RESET

# Settings override
DEBUG_OVERRIDE = len(sys.argv) > 1 and sys.argv[1] == "DEBUG"
try:
    import settings
    from settings import spawn_restart
    if DEBUG_OVERRIDE:
        settings.DEBUG = True
    DEBUG = getattr(settings, 'DEBUG', False)
    MAX_CHUNK_SIZE = getattr(settings, 'MAX_CHUNK_SIZE', 2000)
    prefix = getattr(settings, 'PREFIX', '$') or '$'
except ImportError:
    settings = None
    DEBUG = True
    MAX_CHUNK_SIZE = 2000
    prefix = '&'
debug_logger.warning('main', f"Prefix gesetzt auf '{prefix}' und DEBUG={DEBUG}")

if prefix is None:
    prefix = '&'
    debug_logger.warning('main', "Settings nicht gefunden, Prefix auf '&' gesetzt")


def retry(exceptions, tries=2, delay=5, backoff=2, logger=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            mtries, mdelay = tries, delay
            while mtries > 1:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if logger:
                        logger.warning(func.__name__, f"Fehler: {e}. Versuche {mtries-1} mal weiter, Warte {mdelay}s")
                    time.sleep(mdelay)
                    mtries -= 1
                    mdelay *= backoff
            return func(*args, **kwargs)
        return wrapper
    return decorator

class LoginError(Exception):
    def __init__(self, message, attempts: int, last_exception: Exception = None):
        super().__init__(message)
        self.attempts = attempts
        self.last_exception = last_exception
        self.timestamp = datetime.utcnow()
    def __str__(self):
        base = super().__str__()
        return f"{base} after {self.attempts} attempts at {self.timestamp.isoformat()}"

class SelfBot:
    MAX_LOGIN_ATTEMPTS = 2
    LOGIN_DELAY = 1
    BACKOFF = 2
    EVENT_LOOP_RETRIES = 3
    EVENT_LOOP_DELAY = 2

    def __init__(self, DEBUG=False):
        self.DEBUG = getattr(settings, 'DEBUG', False)
        debug_logger.debug('init', f"DEBUG={self.DEBUG}")

        def _global_exception_hook(exc_type, exc_value, exc_traceback):
            non_critical = (WebDriverException, SeleniumTimeout)
            if issubclass(exc_type, non_critical):
                debug_logger.error('_global_exception_hook', f"Nicht-kritische Exception: {exc_value}")
            else:
                self._handle_unhandled_exception(exc_type, exc_value, exc_traceback)
        sys.excepthook = _global_exception_hook

        raw = getattr(settings, 'ALLLOWED_USERS', None) or getattr(settings, 'ALLOWED_USERS', [])
        if isinstance(raw, str):
            self.allowed_users = [u.strip() for u in raw.split(',') if u.strip()]
        elif isinstance(raw, (list, tuple)):
            self.allowed_users = [str(u) for u in raw]
        else:
            self.allowed_users = []
        debug_logger.debug('init', f"Allowed users: {self.allowed_users}")

        if not self.DEBUG:
            pretty_banner(
                banner_text="Bastiix Selfbot startet",
                completion_title="Login-Fenster geöffnet",
                completion_message="Bitte im Chrome-Fenster einloggen oder warten bis der Automatischer Login abgeschlossen ist.",
            )

        # Login
        try:
            token = self._perform_login()
            self.TOKEN = token.strip('"')
            debug_logger.debug('init', 'Token erfolgreich abgerufen und geparst')
        except LoginError as le:
            debug_logger.error('init', f"LoginError: {le}")
            if self.DEBUG:
                self._write_stackdump(le, crash=True)
                sys.exit(1)
            else:
                self._write_stackdump(le, crash=False)
                spawn_restart()
                sys.exit(1)

        # Bot-Setup
        self.bot = discum.Client(token=self.TOKEN, log={'console': False, 'file': False})
        self.selfbot_user = None
        self._stop_event = threading.Event()
        self.logger = debug_logger
        self.commands = CommandTree(self.bot, prefix, logger=self.logger)
        self.commands.token = self.TOKEN

        self.setup_events()
        apply_chameleon_mask(self)
        debug_logger.debug('init', 'Chameleon Mask angewendet')

        self.loop = asyncio.new_event_loop()
        threading.Thread(target=self._run_event_loop_with_backoff, daemon=True).start()
        debug_logger.debug('init', 'Eigenen asyncio Event-Loop gestartet')

        atexit.register(self.cleanup)
        debug_logger.debug('init', 'SelfBot initialisiert')
        self._startup_done = False

    @retry((WebDriverException, SeleniumTimeout), tries=MAX_LOGIN_ATTEMPTS, delay=LOGIN_DELAY, backoff=BACKOFF, logger=debug_logger)
    def _login_via_chrome(self):
        try:
            service = Service(log_path=os.devnull)
            opts = Options()
            opts.add_argument('--disable-gpu')
            opts.add_argument('--no-sandbox')
            opts.add_experimental_option('excludeSwitches', ['enable-logging'])
            driver = webdriver.Chrome(service=service, options=opts)
        except WebDriverException:
            debug_logger.error('_login_via_chrome', 'Chrome-Treiber nicht gefunden oder inkompatibel. Bitte Chromedriver installieren oder Version an Browser anpassen.')
            raise

        driver.get('https://discord.com/login')
        debug_logger.debug('_login_via_chrome', 'Discord Login-Seite geladen')

        pretty_manual = not (
            hasattr(settings, 'LOGIN_EMAIL') and hasattr(settings, 'LOGIN_PASSWORD')
            and settings.LOGIN_EMAIL and settings.LOGIN_PASSWORD
        )
        if not pretty_manual:
            try:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'email')))
                email_in = driver.find_element(By.NAME, 'email')
                pass_in = driver.find_element(By.NAME, 'password')
                submit_btn = driver.find_element(By.CSS_SELECTOR, 'button[type=submit]')
                email_in.clear(); email_in.send_keys(settings.LOGIN_EMAIL)
                pass_in.clear(); pass_in.send_keys(settings.LOGIN_PASSWORD)
                submit_btn.click()
                debug_logger.debug('_login_via_chrome', 'Anmeldedaten abgeschickt')
            except Exception as e:
                debug_logger.error('_login_via_chrome', f"Automatisches Login fehlgeschlagen: {e}")
                pretty_manual = True
                if not self.DEBUG:
                    append_message('Automatisches Login fehlgeschlagen. Bitte manuell einloggen.')

        WebDriverWait(driver, 300, poll_frequency=1).until(lambda d: '/channels/' in d.current_url)
        debug_logger.debug('_login_via_chrome', f"Redirect erkannt: {driver.current_url}")

        driver.execute_script("""
            const iframe = document.createElement('iframe');
            document.head.appendChild(iframe);
            const pd = Object.getOwnPropertyDescriptor(iframe.contentWindow, 'localStorage');
            iframe.remove();
            Object.defineProperty(window, 'localStorage', pd);
        """)
        debug_logger.debug('_login_via_chrome', 'localStorage via iframe-Hack wiederhergestellt')

        try:
            token = WebDriverWait(driver, 300, poll_frequency=1).until(lambda d: d.execute_script("return window.localStorage.getItem('token');"))
            append_message('Login Erfolgreich. Selfbot wird iniziiert.')
        except SeleniumTimeout:
            debug_logger.error('_login_via_chrome', 'Timeout beim Warten auf Token')
            if not self.DEBUG:
                append_message('Token nicht gefunden. Beende den Selfbot.')
            driver.quit()
            sys.exit(1)
        finally:
            driver.quit()
        debug_logger.debug('_login_via_chrome', f"Token gefunden: {token[:8]}…")
        return token

    def _perform_login(self):
        try:
            return self._login_via_chrome()
        except Exception as e:
            debug_logger.error('_perform_login', f'Login-Versuche erschöpft nach {self.MAX_LOGIN_ATTEMPTS} Versuchen: {e}')
            raise LoginError(f'Login nach {self.MAX_LOGIN_ATTEMPTS} Versuchen fehlgeschlagen', attempts=self.MAX_LOGIN_ATTEMPTS, last_exception=e) from e

    def _run_event_loop_with_backoff(self):
        retries = self.EVENT_LOOP_RETRIES
        delay = self.EVENT_LOOP_DELAY
        while retries > 0:
            try:
                self.loop.run_forever()
                return
            except Exception as e:
                debug_logger.error('_run_event_loop', f"Event-Loop Fehler: {e}")
                self._write_stackdump(e, crash=True)
                if not self.DEBUG:
                    spawn_restart()
                time.sleep(delay)
                retries -= 1
                delay *= 2
        sys.exit(1)

    def _handle_unhandled_exception(self, exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        debug_logger.error('_unhandled_exception', f"{exc_value}")
        self._write_stackdump(exc_value, crash=True)
        if not self.DEBUG:
            spawn_restart()
        sys.exit(1)

    def _write_stackdump(self, exception, crash=False):
        prefix = 'CRASH' if crash else 'EXCEPTION'
        timestamp = datetime.utcnow().strftime('%H.%M_%d.%m.%Y')
        filename = f"{prefix}_{timestamp}.log"
        path = os.path.join('.', 'log', 'system', filename)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(f"{prefix} {datetime.utcnow().isoformat()}\n")
            traceback.print_exception(type(exception), exception, exception.__traceback__, file=f)

    def request_with_backoff(self, func, *args, **kwargs):
        delay = 1
        for attempt in range(1, 6):
            try:
                debug_logger.debug('backoff', f"Versuch {attempt} für {func.__name__}")
                return func(*args, **kwargs)
            except Exception as e:
                debug_logger.warning('backoff', f"{func.__name__} fehlgeschlagen: {e}, warte {delay}s")
                time.sleep(delay)
                delay *= 2
        debug_logger.error('backoff', f"Maximale Versuche für {func.__name__} erreicht")
        if not self.DEBUG:
            append_message(f"Fehler bei {func.__name__}. Maximale Versuche erreicht.")
        sys.exit(1)

    def verify_token(self):
        debug_logger.debug('verify_token', 'Überprüfe Token via REST info()')
        try:
            resp = self.request_with_backoff(self.bot.info)
            data = resp.json() if hasattr(resp, 'json') else resp
            if not isinstance(data, dict) or not data.get('id'):
                raise ValueError('Ungültige Antwort von info()')
            debug_logger.debug('verify_token', f"Token gültig für User ID {data['id']}")
        except Exception as e:
            debug_logger.error('verify_token', f'Verifikation fehlgeschlagen: {e}')
            if not self.DEBUG:
                append_message(f"Fehler beim Verifizieren des Tokens: {e}")
            sys.exit(1)

    async def simulate_typing_send(self, channel: str, message: str) -> None:
        try:
            debug_logger.debug('simulate_typing_send', f"Aufruf mit channel={channel}, message length={len(message)}")
        except Exception as e:
            debug_logger.error('simulate_typing_send', f"Logger konnte Eingangsparameter nicht protokollieren: {e}")

        if not re.fullmatch(r"\d+", channel):
            err_msg = f"Ungültige channel-ID: {channel}"; debug_logger.error('simulate_typing_send', err_msg); raise ValueError(err_msg)

        async def _type_and_wait(chan: str, wait: float):
            try:
                self.bot.typingAction(chan)
                debug_logger.debug('simulate_typing_send', f"Typing event ausgelöst für {wait:.2f}s")
            except DiscordError as e:
                debug_logger.error('simulate_typing_send', f"Discord-Fehler beim Typing-Event: {e}")
            except Exception as e:
                debug_logger.error('simulate_typing_send', f"Unbekannter Fehler beim Typing-Event: {e}")
            await asyncio.sleep(wait)

        if len(message) > MAX_CHUNK_SIZE:
            total_chunks = (len(message) + MAX_CHUNK_SIZE - 1) // MAX_CHUNK_SIZE
            debug_logger.debug('simulate_typing_send', f"Nachricht in {total_chunks} Chunks aufgeteilt")
            for idx, i in enumerate(range(0, len(message), MAX_CHUNK_SIZE), start=1):
                chunk = message[i:i + MAX_CHUNK_SIZE]
                debug_logger.debug('simulate_typing_send', f"Bereite Chunk {idx}/{total_chunks} vor (Zeichen {i}-{i+len(chunk)})")
                try:
                    await _type_and_wait(channel, 1.0)
                    self.bot.sendMessage(channel, chunk)
                    debug_logger.debug('simulate_typing_send', f"Chunk {idx}/{total_chunks} gesendet an {channel}")
                except DiscordError as e:
                    debug_logger.error('simulate_typing_send', f"Discord-Fehler beim Chunk {idx}: {e}")
                except Exception as e:
                    debug_logger.error('simulate_typing_send', f"Unbekannter Fehler beim Chunk {idx}: {e}")
            return

        length = len(message)
        delay = 1.0 if length <= 100 else 1.0 + (min(length, MAX_CHUNK_SIZE) - 100) * 3.0 / (MAX_CHUNK_SIZE - 100)
        debug_logger.debug('simulate_typing_send', f"Simuliere Tippen für {length} Zeichen: Warte {delay:.2f}s")
        try:
            await _type_and_wait(channel, delay)
            self.bot.sendMessage(channel, message)
            debug_logger.debug('simulate_typing_send', f"Nachricht gesendet an {channel}")
        except DiscordError as e:
            debug_logger.error('simulate_typing_send', f"Discord-Fehler beim Senden: {e}")
        except Exception as e:
            debug_logger.error('simulate_typing_send', f"Unbekannter Fehler beim Senden: {e}")

    def setup_events(self):
        @self.bot.gateway.command
        def on_connect(resp):
            if not resp.event.ready_supplemental:
                return
            debug_logger.debug('on_connect', f"Connected: ready={resp.event.ready_supplemental}")
            time.sleep(1)
            try:
                u = self.bot.gateway.session.user
                if not u or not u.get('id'):
                    raise KeyError()
                self.selfbot_user = u
                debug_logger.debug('on_connect', 'User aus Gateway-Cache geladen')
            except Exception:
                resp = self.request_with_backoff(self.bot.info)
                self.selfbot_user = resp.json() if hasattr(resp, 'json') else resp
                debug_logger.debug('on_connect', 'User über REST info() geladen')
            payload = {'op': 3, 'd': {'since': 0, 'activities': [], 'status': 'online', 'afk': False}}
            self.bot.gateway.send(payload)

            if not self.DEBUG and not self._startup_done:
                self._startup_done = True
                print_banner('Startup Aufgaben abgeschlossen')
                append_message(f"Angemeldet als {self.selfbot_user['username']}#{self.selfbot_user.get('discriminator','')}")
                append_message(f"Geladene Befehle: {len(self.commands.commands)}")
                print_banner('Laufzeit')

        @self.bot.gateway.command
        def on_message(resp):
            if not resp.event.message:
                return
            try:
                msg = resp.parsed.auto()
            except Exception:
                debug_logger.error('on_message', 'Parsing fehlgeschlagen')
                return
            author = msg.get('author') or {}
            author_id = str(author.get('id'))
            if author.get('bot', False) or (self.allowed_users and author_id not in self.allowed_users):
                return
            content = msg.get('content', '').strip()
            channel = msg.get('channel_id')
            message_id = msg.get('id')
            if not content.startswith(self.commands.prefix):
                return
            debug_logger.debug('on_message', f"Inhalt empfangen: {content}")
            handled, reply = self.commands.handle(channel, author, content)
            if not handled:
                return
            if not self.DEBUG:
                cmd_label = content.split()[0]
                append_message(f"{author.get('username','?')} hat den Befehl {cmd_label} ausgeführt.")
            try:
                self.bot.typingAction(channel)
                self.bot.reply(channel, message_id, reply)
                debug_logger.debug('on_message', f"Replied to message {message_id} in channel {channel}")
            except Exception as e:
                debug_logger.error('on_message', f"Fehler beim Reply: {e}")

    def cleanup(self):
        debug_logger.debug('cleanup', 'Starte Cleanup')
        self._stop_event.set()
        try:
            self.bot.gateway.close()
            debug_logger.debug('cleanup', 'Gateway geschlossen')
        except Exception as e:
            debug_logger.error('cleanup', f"Fehler beim Schließen: {e}")

    def run(self):
        self.verify_token()
        if self.DEBUG:
            debug_logger.debug('startup', 'Starte im Debug-Modus')
        else:
            print_banner('Initialisierung abgeschlossen')
            append_message('Starte Selfbot login...')
        try:
            self.bot.gateway.run(auto_reconnect=True)
        except KeyboardInterrupt:
            debug_logger.debug('run', 'KeyboardInterrupt empfangen, führe Cleanup aus')
            self.cleanup()
            if not self.DEBUG:
                pretty_banner(
                    banner_text='Bastiix Selbstbot wird beendet',
                    completion_title='Alle Systeme offline',
                    completion_message='Bis zum nächsten Mal!'
                )
            sys.exit(0)
        except Exception as e:
            debug_logger.error('run', f"Gateway-Fehler: {e}")
        else:
            if not self.DEBUG:
                pretty_banner(
                    banner_text='Discum Selfbot wird beendet',
                    completion_title='Alle Systeme offline',
                    completion_message='Bis zum nächsten Mal!'
                )

if __name__ == '__main__':
    bot = SelfBot(DEBUG=DEBUG)
    bot.run()
