# ---------------------------------------------------------------------------
# \src\core\discord\chameleon_mask.py
# ---------------------------------------------------------------------------

import random
import threading
import time
import asyncio
import datetime
 
from src.core.animation.debug_animation import logger as debug_logger
from src.core.animation.running_animation import print_banner, append_message

try:
    import settings
    DEBUG = getattr(settings, 'DEBUG', False)
except ImportError:
    settings = None
    DEBUG = False


def _get_sleep_segment():
    hour = datetime.datetime.now().hour
    if 8 <= hour < 20:
        return random.uniform(0.2, 0.6)
    else:
        return random.uniform(0.05, 0.3)


def _presence_loop(self):
    initial_delay = random.uniform(1, 10)
    debug_logger.debug('chameleon', f'Initiale Präsenz-Pause: {initial_delay:.2f}s')
    time.sleep(initial_delay)
    base_statuses = getattr(settings, 'PRESENCE_STATUSES', ['online', 'idle', 'dnd'])
    base_activities = getattr(settings, 'PRESENCE_ACTIVITIES', [
        [],
        [{'name': 'Chatten', 'type': 0}],
        [{'name': 'Lesen', 'type': 0}],
        [{'name': 'Musik hören', 'type': 2}]
    ])
    debug_logger.debug('chameleon', 'Presence-Loop gestartet')
    while not self._stop_event.is_set():
        statuses = list(base_statuses)
        activities = list(base_activities)
        hour = datetime.datetime.now().hour
        if hour >= 20 or hour < 6:
            statuses.extend(['idle', 'dnd'] * 2)
        inner = [
            ('since', 0),
            ('activities', random.choice(activities)),
            ('status', random.choice(statuses)),
            ('afk', False)
        ]
        random.shuffle(inner)
        d_payload = {k: v for k, v in inner}
        outer = [('op', 3), ('d', d_payload)]
        random.shuffle(outer)
        payload = {k: v for k, v in outer}
        debug_logger.debug('chameleon', f"Prepared Presence payload fields order: {list(payload.keys())}")
        try:
            self.bot.gateway.send(payload)
            debug_logger.debug('chameleon', f"Presence-Update gesendet: {payload['d']}")
        except Exception as e:
            debug_logger.error('chameleon', f"Presence-Update fehlgeschlagen: {e}")
            if 'closed' in str(e).lower():
                debug_logger.warn('chameleon', 'Gateway-Verbindung geschlossen, Presence-Loop endet')
                break
        min_m, max_m = getattr(settings, 'PRESENCE_MEAN_RANGE', (120, 300))
        mean = random.uniform(min_m, max_m)
        wait = random.expovariate(1 / mean)
        jitter = random.uniform(-mean * 0.1, mean * 0.1)
        total = max(1, wait + jitter)
        debug_logger.debug('chameleon', f"Nächste Presence-Update in {total:.2f}s")
        rem = total
        while rem > 0 and not self._stop_event.is_set():
            seg = _get_sleep_segment()
            t = min(seg, rem)
            time.sleep(t)
            rem -= t


def _activity_once(self):
    actions = []
    if settings and hasattr(settings, 'ACTIVITY_ACTIONS'):
        for name in settings.ACTIVITY_ACTIONS:
            fn = getattr(self.bot, name, None)
            if callable(fn):
                actions.append(fn)
    if not actions:
        actions = [self.bot.getGuilds, self.bot.info]
    fn = random.choice(actions)
    try:
        res = fn()
        debug_logger.debug('chameleon', f"Warm-up Aktion {fn.__name__} erfolgreich: {res}")
    except Exception as e:
        debug_logger.error('chameleon', f"Warm-up Aktion {fn.__name__} fehlgeschlagen: {e}")
    # Dummy-Interaktionen ergänzen
    for dummy in ['getChannel', 'getGuildRoles']:
        fn_dummy = getattr(self.bot, dummy, None)
        if callable(fn_dummy):
            try:
                guilds = self.bot.getGuilds()
                gid = None
                if isinstance(guilds, list) and guilds:
                    first = guilds[0]
                    gid = first.get('id') if isinstance(first, dict) else first
                if gid:
                    fn_dummy(gid)
                    debug_logger.debug('chameleon', f"Dummy-Interaktion {dummy} ausgeführt: {gid}")
            except Exception as e:
                debug_logger.error('chameleon', f"Dummy-Interaktion {dummy} fehlgeschlagen: {e}")
    # Simuliere Lesebestätigung für zufällige Nachrichten
    try:
        # Channels aus erster Guild
        guilds = self.bot.getGuilds()
        if isinstance(guilds, list) and guilds:
            first = guilds[0]
            gid = first.get('id') if isinstance(first, dict) else first
            # Nachrichten abrufen und acken
            msgs = self.bot.getMessages(gid, num=3)
            if hasattr(msgs, 'json'):
                data = msgs.json()
                for m in random.sample(data, min(2, len(data))):
                    mid = m.get('id')
                    self.bot.ackMessage(gid, mid)
                    debug_logger.debug('chameleon', f"AckMessage für Nachricht {mid} in Channel {gid}")
    except Exception as e:
        debug_logger.error('chameleon', f"Lesebestätigung fehlgeschlagen: {e}")


def _random_activity_loop(self):
    initial_delay = random.uniform(1, 10)
    debug_logger.debug('chameleon', f'Initiale Activity-Pause: {initial_delay:.2f}s')
    time.sleep(initial_delay)
    debug_logger.debug('chameleon', 'Random-Activity-Loop gestartet')
    while not self._stop_event.is_set():
        _activity_once(self)
        min_a, max_a = getattr(settings, 'ACTIVITY_MEAN_RANGE', (60, 180))
        mean_a = random.uniform(min_a, max_a)
        w = random.expovariate(1 / mean_a)
        jit = random.uniform(-mean_a * 0.1, mean_a * 0.1)
        tot = max(1, w + jit)
        debug_logger.debug('chameleon', f"Nächste Random-Activity in {tot:.2f}s")
        rem = tot
        while rem > 0 and not self._stop_event.is_set():
            seg = _get_sleep_segment()
            t = min(seg, rem)
            time.sleep(t)
            rem -= t


def mask(self):
    if not DEBUG:
        try:
            print_banner("Verschleierung wird gestartet")
            append_message("Warm-up Phase: Präsenz und Aktivität werden initialisiert.")
        except Exception as e:
            debug_logger.error('chameleon', f"Fehler bei Statusanzeige: {e}")
    phases = ['presence', 'activity']
    random.shuffle(phases)
    for phase in phases:
        if phase == 'presence':
            _presence_loop(self)
        else:
            _activity_once(self)
        p = random.uniform(1, 3)
        debug_logger.debug('chameleon', f"Warm-up Pause: {p:.2f}s")
        time.sleep(p)
    if not DEBUG:
        append_message("Alle Verschleierungen angewendet.")
    t1 = threading.Thread(target=_presence_loop, args=(self,), daemon=True)
    t1.start()
    debug_logger.debug('chameleon', 'Presence-Loop Thread gestartet')
    t2 = threading.Thread(target=_random_activity_loop, args=(self,), daemon=True)
    t2.start()
    debug_logger.debug('chameleon', 'Random-Activity-Loop Thread gestartet')
    debug_logger.debug('chameleon', 'Alle Masking-Routinen gestartet')
    # Threads laufen weiter im Hintergrund
