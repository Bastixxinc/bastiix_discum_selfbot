# ---------------------------------------------------------------------------
# \src\core\discord\message.py
# \author @bastiix
# ---------------------------------------------------------------------------
 
def boxed_message(title: str, body: str) -> str:
    lines = [title, "=" * len(title)] + body.split("\n")
    return "```\n" + "\n".join(lines) + "\n```"

boxed_message_with_title = boxed_message  # Alias für Konsistenz

def inline_message_with_title(title: str, body: str) -> str:
    lines = [title, "=" * len(title)] + body.split("\n")
    return "\n" + "\n".join(lines) + "\n"


def success_message(text: str) -> str:
    return (
        "```diff\n"
        f"+ SUCCESS: {text}\n"
        "```"
    )

def success_message_boxed(title: str, text: str) -> str:
    return (
        "```diff\n"
        f"+ SUCCESS: {title}\n"
        f"{text}\n"
        "```"
    )


def info_message(text: str) -> str:
    return (
        "```ini\n"
        f"[ INFO ] {text}\n"
        "```"
    )

def info_message_boxed(title: str, text: str) -> str:
    return (
        "```ini\n"
        f"[ INFO ] {title}\n"
        f"{text}\n"
        "```"
    )


def warning_message(text: str) -> str:
    return (
        "```diff\n"
        f"- WARNING: {text}\n"
        "```"
    )

def warning_message_boxed(title: str, text: str) -> str:
    return (
        "```diff\n"
        f"- WARNING: {title}\n"
        f"{text}\n"
        "```"
    )


def error_message(text: str) -> str:
    return (
        "```diff\n"
        f"- ERROR: {text}\n"
        "```"
    )

def error_message_with_title(title: str, text: str) -> str:
    return (
        "```diff\n"
        f"- -> {title}\n"
        f"{text}\n"
        "```"
    )

def error_message_with_title_and_correction(title: str, text: str, correction: str) -> str:
    return (
        "```diff\n"
        f"- -> {title}\n"
        f"{text}\n"
        f"+ {correction}\n"
        "```"
    )


def debug_message(text: str) -> str:
    return (
        "```diff\n"
        f"- DEBUG: {text}\n"
        "```"
    )

def debug_message_boxed(title: str, text: str) -> str:
    return (
        "```diff\n"
        f"- DEBUG: {title}\n"
        f"{text}\n"
        "```"
    )

def question_message(question: str) -> str:
    return (
        "```fix\n"
        f"? {question}\n"
        "```"
    )

def syntax_message(language: str, code: str) -> str:
    return (
        f"```{language}\n"
        f"{code}\n"
        "```"
    )

def list_message(title: str, items: list[str]) -> str:
    body = "\n".join(f"{i+1}. {item}" for i, item in enumerate(items))
    return boxed_message(title, body)

def spoiler_message(text: str) -> str:
    return f"||{text}||"

def embed_like_message(title: str, description: str, footer: str | None = None) -> str:
    lines = [f"**{title}**", description]
    if footer:
        lines.append(f"*{footer}*")
    return "\n".join(lines)
