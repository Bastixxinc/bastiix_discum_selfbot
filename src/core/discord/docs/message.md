# Detaillierte Dokumentation: `message.py`

Das Modul `message.py` bietet eine Reihe von Funktionen zur einheitlichen Formatierung von Discord-Nachrichten im Textkanal. Es abstrahiert wiederkehrende Anzeigetypen wie eingerahmte Blöcke, Statusmeldungen und Inline-Layouts, um den Code einfacher und konsistenter zu halten.

---

## Inhaltsverzeichnis

1. [Modul-Import](#modul-import)
2. [Funktionale Übersicht](#funktionale-übersicht)
3. [Detaillierte Funktionsreferenz](#detaillierte-funktionsreferenz)
   1. [`boxed_message`](#boxed_message)
   2. [`inline_message_with_title`](#inline_message_with_title)
   3. [`success_message`](#success_message)
   4. [`success_message_boxed`](#success_message_boxed)
   5. [`info_message`](#info_message)
   6. [`info_message_boxed`](#info_message_boxed)
   7. [`warning_message`](#warning_message)
   8. [`warning_message_boxed`](#warning_message_boxed)
   9. [`error_message`](#error_message)
   10. [`error_message_with_title`](#error_message_with_title)
   11. [`error_message_with_title_and_correction`](#error_message_with_title_and_correction)
   12. [`debug_message`](#debug_message)
   13. [`debug_message_boxed`](#debug_message_boxed)
   14. [`question_message`](#question_message)
   15. [`syntax_message`](#syntax_message)
   16. [`list_message`](#list_message)
   17. [`spoiler_message`](#spoiler_message)
   18. [`embed_like_message`](#embed_like_message)

---

## Modul-Import

```python
from src.core.discord.message import (
    boxed_message,
    inline_message_with_title,
    success_message,
    success_message_boxed,
    info_message,
    info_message_boxed,
    warning_message,
    warning_message_boxed,
    error_message,
    error_message_with_title,
    error_message_with_title_and_correction,
    debug_message,
    debug_message_boxed,
    question_message,
    syntax_message,
    list_message,
    spoiler_message,
    embed_like_message,
)
```

> **Hinweis:** `boxed_message_with_title` ist ein Alias für `boxed_message`.

---

## Funktionale Übersicht

| Funktion                                | Kurzbeschreibung                               | Rückgabetyp |
|-----------------------------------------|------------------------------------------------|-------------|
| `boxed_message`                        | Eingerahmter Codeblock mit Titel und Inhalt     | `str`       |
| `inline_message_with_title`            | Inline-Text mit hervorgehobenem Titel           | `str`       |
| `success_message`                      | Erfolgsmeldung (+ SUCCESS) im Diff-Stil         | `str`       |
| `success_message_boxed`                | Erfolgsmeldung im eingerahmten Block            | `str`       |
| `info_message`                         | Info-Meldung ([ INFO ]) im INI-Stil             | `str`       |
| `info_message_boxed`                   | Eingerahmte Info-Meldung                        | `str`       |
| `warning_message`                      | Warnung (- WARNING) im Diff-Stil                | `str`       |
| `warning_message_boxed`                | Eingerahmte Warnmeldung                         | `str`       |
| `error_message`                        | Fehlermeldung (- ERROR) im Diff-Stil            | `str`       |
| `error_message_with_title`             | Fehlermeldung mit Titelzeile                    | `str`       |
| `error_message_with_title_and_correction` | Fehler + Korrekturhinweis                    | `str`       |
| `debug_message`                        | Debug-Ausgabe (- DEBUG) im Diff-Stil            | `str`       |
| `debug_message_boxed`                  | Eingerahmte Debug-Ausgabe                       | `str`       |
| `question_message`                     | Frage (? ...) im Fix-Stil                       | `str`       |
| `syntax_message`                       | Code-Block mit Sprach-Markup                    | `str`       |
| `list_message`                         | Nummerierte Liste im eingerahmten Block         | `str`       |
| `spoiler_message`                      | Discord-Spoiler (`||...||`)                     | `str`       |
| `embed_like_message`                   | Embed-ähnliche Nachricht mit Titel & Footer      | `str`       |

---

## Detaillierte Funktionsreferenz

### `boxed_message(title: str, body: str) -> str`
Erzeugt einen eingerahmten Codeblock, der den Titel über einer Trennlinie und den mehrzeiligen Textkörper enthält.

- **Parameter**:
  - `title` (_str_): Überschrift des Blocks.
  - `body` (_str_): Mehrzeiliger Nachrichtentext.
- **Rückgabe**: Ein String im Format:
  ```
  ```
  Titel
  ========
  Zeile 1
  Zeile 2
  ...
  ```
  ```
- **Beispiel**:
  ```python
  print(boxed_message("Status", "Alles OK"))
  ```
  **Ergibt**:
  ```
  Status
  ======
  Alles OK
  ```

---

### `inline_message_with_title(title: str, body: str) -> str`
Erzeugt eine kompakte Nachricht mit Fettdruck-Titel und folgendem Fließtext, ohne Code-Block.

- **Parameter**:
  - `title` (_str_): Fettdargestellter Titel.
  - `body` (_str_): Beschreibungstext.
- **Rückgabe**: String im Markdown-Format:
  ```markdown
  **Titel**
  Beschreibung
  ```
- **Beispiel**:
  ```python
  print(inline_message_with_title("Info", "Dieser Vorgang ist abgeschlossen."))
  ```

---

### `success_message(text: str) -> str`
Formatiert eine Erfolgsmeldung im `diff`-Stil mit grünem Plus (`+`) und `SUCCESS`-Prefix.

- **Parameter**:
  - `text` (_str_): Erfolgsnachricht.
- **Rückgabe**:
  ```diff
  + SUCCESS: Dein Text hier.
  ```

---

### `success_message_boxed(title: str, text: str) -> str`
Kombiniert `success_message` mit einem eingerahmten Codeblock um Titel und Detailtext.

- **Parameter**:
  - `title` (_str_): Titel der Meldung.
  - `text` (_str_): Detailtext.
- **Rückgabe**: Mehrzeiliger diff-Block im eingerahmten Layout.

---

### `info_message(text: str) -> str`
Generiert eine Info-Meldung im `ini`-Stil.

- **Parameter**:
  - `text` (_str_): Informationstext.
- **Rückgabe**:
  ```ini
  [ INFO ] Information hier.
  ```

---

### `info_message_boxed(title: str, text: str) -> str`
Verpackt eine `info_message` in einen eingerahmten Codeblock.

---

### `warning_message(text: str) -> str`
Formatiert Warnungen im `diff`-Stil mit rotem Minus (`-`).

- **Parameter**:
  - `text` (_str_): Warntext.
- **Rückgabe**:
  ```diff
  - WARNING: Vorsicht hier!
  ```

---

### `warning_message_boxed(title: str, text: str) -> str`
Eingerahmte Version von `warning_message`.

---

### `error_message(text: str) -> str`
Formatiert Fehler im `diff`-Stil.

- **Parameter**:
  - `text` (_str_): Fehlermeldung.
- **Rückgabe**:
  ```diff
  - ERROR: Etwas ist schiefgelaufen.
  ```

---

### `error_message_with_title(title: str, text: str) -> str`
Ergänzt die Fehlermeldung um eine separate Titelzeile.

- **Rückgabe**:
  ```diff
  - -> Titel des Fehlers
    Detailbeschreibung hier.
  ```

---

### `error_message_with_title_and_correction(title: str, text: str, correction: str) -> str`
Fügt zusätzlich einen positiven Correction-Hinweis hinzu.

- **Rückgabe**:
  ```diff
  - -> Titel
    Fehlerbeschreibung
  + Verbesserungsvorschlag
  ```

---

### `debug_message(text: str) -> str`
Markiert Debug-Ausgaben im `diff`-Stil.

- **Rückgabe**:
  ```diff
  - DEBUG: Debug-Info hier.
  ```

---

### `debug_message_boxed(title: str, text: str) -> str`
Eingerahmte Debug-Informationen.

---

### `question_message(question: str) -> str`
Formatiert eine Frage im `fix`-Stil mit vorangestelltem Fragezeichen.

- **Rückgabe**:
  ```fix
  ? Deine Frage hier?
  ```

---

### `syntax_message(language: str, code: str) -> str`
Erzeugt einen Codeblock, ausgezeichnet mit einer Sprachkennung.

- **Parameter**:
  - `language` (_str_): Bezeichner der Programmiersprache (z.B. `python`).
  - `code` (_str_): Zu markierender Quellcode.
- **Rückgabe**:
  ```<language>
  <code>
  ```

---

### `list_message(title: str, items: list[str]) -> str`
Nummerierte Liste im eingerahmten Codeblock.

- **Parameter**:
  - `title` (_str_): Überschrift der Liste.
  - `items` (_list[str]_): Elemente der Liste.
- **Rückgabe**:
  ```
  <title>
  ======
  1. Erster Punkt
  2. Zweiter Punkt
  ...
  ```

---

### `spoiler_message(text: str) -> str`
Verwandelt beliebigen Text in einen Discord-Spoiler.

- **Rückgabe**: `||text||`

---

### `embed_like_message(title: str, description: str, footer: str | None = None) -> str`
Erzeugt eine embed-ähnliche Nachricht mit fettem Titel, Beschreibung und optionaler Fußzeile.

- **Parameter**:
  - `footer` (_Optional[str]_) – wird als kursiver Text unterhalb der Beschreibung angezeigt.
- **Rückgabe**:
  ```markdown
  **Titel**
  Beschreibungstext
  *Fußzeile (falls gesetzt)*
  ```

---

*Ende der detaillierten Dokumentation*

