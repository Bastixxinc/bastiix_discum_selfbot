# Dokumentation von `settings.py`

Diese Datei definiert zentrale Konfigurationsparameter für den SelfBot. Änderungen hier wirken sich direkt auf Verhalten, Logging und Darstellung aus.

---

## Inhaltsverzeichnis

1. [Allgemeine Hinweise](#allgemeine-hinweise)
2. [Konfigurationsvariablen](#konfigurationsvariablen)
   - [`DEBUG`](#debug)
   - [`LOGGING`](#logging)
   - [`PREFIX`](#prefix)
   - [`LOGIN_EMAIL`, `LOGIN_PASSWORD`](#login_email-login_password)
   - [`ALLLOWED_USERS`](#allowed_users)
   - [`MAINCOLOR`, `SECONDCOLOR`, `STAMPCOLOR`, `RESETCOLOR`](#farbdefinitionen)
   - [`MAX_CHUNK_SIZE`](#max_chunk_size)
   - [`SELFBOT_DUMP_CHANNEL`](#selfbot_dump_channel)
   - [`RESTART_DEBUG_MODE_PATH`](#restart_debug_mode_path)
3. [Anpassung und Beispiele](#anpassung-und-beispiele)

---

## Allgemeine Hinweise

- Diese Datei wird beim Start von `main.py` importiert und liest alle Einstellungen ein.
- Leere Werte (z. B. `LOGIN_EMAIL = ""`) signalisieren manuelle Eingabe bzw. Deaktivierung der betreffenden Funktion.
- Farbwerte werden als ANSI-Codes gespeichert und zur Gestaltung von Ausgaben im Terminal verwendet.

---

## Konfigurationsvariablen

### `DEBUG`
- **Typ**: `bool`
- **Standard**: `True`

Schaltet alle Debug-Ausgaben in der Konsole ein (True) oder aus (False).

---

### `LOGGING`
- **Typ**: `bool`
- **Standard**: `True`

Steuert, ob Debug- und Fehler-Logs in Dateien unter `/log/debug/` abgelegt werden.

---

### `PREFIX`
- **Typ**: `str`
- **Standard**: `"$"`

Präfix, mit dem alle Bot-Befehle in Discord identifiziert werden.

---

### `LOGIN_EMAIL` & `LOGIN_PASSWORD`
- **Typ**: `str`
- **Standard**: `<Beispielwerte>`

E-Mail und Passwort für automatisches Login via Selenium/Chrome. Leere Strings deaktivieren automatischen Login und erzwingen manuelle Eingabe.

---

### `ALLLOWED_USERS`
- **Typ**: `tuple` von `str`
- **Standard**: Vier IDs in Beispielkonfiguration

Liste der Discord-User-IDs, von denen Befehle akzeptiert werden. Andere Nachrichten werden ignoriert.

---

### Farbdefinitionen
- **`MAINCOLOR`**: ANSI-Code für Rahmen und Banner (z. B. `"\033[1;36m"`)
- **`SECONDCOLOR`**: Sekundärfarbe, z. B. für Zeitstempel
- **`STAMPCOLOR`**: Farbe für Timestamps
- **`RESETCOLOR`**: ANSI-Code zum Zurücksetzen der Farbe

Diese Werte definieren das Erscheinungsbild von Terminal-Ausgaben im Nicht-Debug-Modus.

---

### `MAX_CHUNK_SIZE`
- **Typ**: `int`
- **Standard**: `2000`

Maximale Länge einer Discord-Nachricht, bevor sie in mehrere Chunks aufgeteilt wird.

---

### `SELFBOT_DUMP_CHANNEL`
- **Typ**: `str`
- **Standard**: Beispiel-Channel-ID

Discord-Channel-ID, in den systemkritische Logs oder Dumps gesendet werden können.

---

### `RESTART_DEBUG_MODE_PATH`
- **Typ**: `str`
- **Standard**: Pfad zu Batch-Datei `src/core/system/restart_debug.bat`

Pfad zur Skriptdatei, die den SelfBot im Debug-Modus neustarten kann.

---

## Anpassung und Beispiele

- **Debug deaktivieren**:
  ```python
  DEBUG = False
  LOGGING = False
  ```
- **Befehlspräfix ändern**:
  ```python
  PREFIX = "!"
  ```
- **Nur bestimmte Nutzer zulassen**:
  ```python
  ALLLOWED_USERS = ("123456789012345678",)
  ```

*Ende der Dokumentation*

