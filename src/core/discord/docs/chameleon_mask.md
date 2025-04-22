# Chameleon Mask (chameleon_mask.py)

Dieses Modul sorgt dafür, dass ein Selfbot oder Discord-Client seine Präsenz und Aktivität zufällig variiert, um wie ein „Chamäleon“ im Netzwerk aufzutreten. Es startet Hintergrund-Threads, die in definierten Intervallen Status- und Aktivitäts-Updates senden.

## Inhaltsverzeichnis

1. [Voraussetzungen](#voraussetzungen)
2. [Import](#import)
3. [Konfiguration](#konfiguration)
4. [Internale Hilfsfunktionen](#internale-hilfsfunktionen)
   - [_get_sleep_segment](#_get_sleep_segment)
5. [Kern-Funktionen](#kern-funktionen)
   - [_presence_loop](#_presence_loop)
   - [_activity_once](#_activity_once)
   - [_random_activity_loop](#_random_activity_loop)
   - [mask](#mask)
6. [Empfohlene Nutzung](#empfohlene-nutzung)
7. [Beispiel](#beispiel)

---

## Voraussetzungen

- Python 3.6+
- Abhängigkeiten:
  - `src.core.animation.debug_animation` (Logger)
  - `src.core.animation.running_animation` (`print_banner`, `append_message`)
- Optionale `settings.py` mit Konfigurations-Variablen (siehe unten).

## Import

```python
from src.core.discord.chameleon_mask import mask
```

## Konfiguration

In einer `settings.py` können folgende Variablen definiert werden:

- `DEBUG: bool` – wenn True, werden optische Banner und Meldungen unterdrückt.
- `PRESENCE_STATUSES: list[str]` – Liste der möglichen Statuswerte (Standard: `['online','idle','dnd']`).
- `PRESENCE_ACTIVITIES: list[list[dict]]` – Liste von Activity-Payloads (Standard-Beispiele enthalten `Chatten`, `Lesen`, `Musik hören`).
- `PRESENCE_MEAN_RANGE: tuple[int,int]` – mittleres Intervall (in Sekunden) für Status-Updates (Standard: `(120,300)`).
- `ACTIVITY_ACTIONS: list[str]` – Namen von Bot-Methoden für Warm-up-Aktionen (z. B. `['getGuilds','info']`).
- `ACTIVITY_MEAN_RANGE: tuple[int,int]` – mittleres Intervall (in Sekunden) für zufällige Aktionen (Standard: `(60,180)`).

## Internale Hilfsfunktionen

### `_get_sleep_segment() -> float`

Berechnet einen kurzen zufälligen Sleep-Abschnitt, der in Schleifen verwendet wird, um „jittered“ Wartezeiten zu realisieren.

- Tagsüber (8–20 Uhr): Zufallswert zwischen 0,2 – 0,6 s
- Nachts (< 6 Uhr oder ≥ 20 Uhr): Zufallswert zwischen 0,05 – 0,3 s

## Kern-Funktionen

### `_presence_loop(self)`

Endlosschleife, die in zufälligen Abständen Presence-Update-Payloads an die Discord-Gateway-Verbindung sendet.

1. Initiale zufällige Verzögerung (1–10 s).
2. Endlosschleife bis `self._stop_event` gesetzt:
   - Status- und Activity-Listen anhand der Uhrzeit gewichten.
   - Payload-Felder zufällig mischen und senden (`op:3`, `d:{...}`).
   - Nächste Wartezeit nach Exponentialverteilung mit Jitter aus `PRESENCE_MEAN_RANGE`.
   - In kleinen Segmenten (aus `_get_sleep_segment()`) schlafen, bis Gesamtdauer erreicht.

### `_activity_once(self)`

Führt eine Warm-up-Aktion aus:

1. Wählt aus `settings.ACTIVITY_ACTIONS` oder Standard-Methoden (`getGuilds`, `info`).
2. Führt eine Dummy-Interaktion mit `getChannel` und `getGuildRoles` durch.
3. Simuliert Lesebestätigungen (`ackMessage`) für zufällige Nachrichten in der ersten Guild.

### `_random_activity_loop(self)`

Wie `_presence_loop`, aber führt in Intervallen immer wieder `_activity_once` aus.

1. Initiale Verzögerung (1–10 s).
2. In Schleife bis `self._stop_event`:
   - `_activity_once(self)`
   - Wartezeit nach `ACTIVITY_MEAN_RANGE` mit Jitter.
   - Schlaf in Segmenten.

### `mask(self)`

Öffentliche Funktion zum Starten aller Masking-Routinen:

1. Optional: Anzeige via `print_banner` und `append_message` (wenn `DEBUG is False`).
2. Warm-up-Phase:
   - Führt einmalig `_presence_loop` oder `_activity_once` (randomisiert) aus.
3. Startet zwei Daemon-Threads:
   - Thread 1 für `_presence_loop`
   - Thread 2 für `_random_activity_loop`
4. Threads laufen unbegrenzt im Hintergrund.

## Empfohlene Nutzung

- Rufen Sie `mask(self)` **einmal** im Initialisierungsprozess Ihres Bots auf.
- **Runtime-Ausgaben** sollten mit `append_message(...)` erfolgen, Banner (`print_banner`) nur, wenn Sie eine auffällige visuelle Einleitung oder Trennung wünschen.

## Beispiel

```python
# in Ihrem Bot-Setup:
from src.core.discord.chameleon_mask import mask

class SelfBot:
    def __init__(...):
        # Setup, Login, etc.
        mask(self)
```

*Ende der Dokumentation.*

