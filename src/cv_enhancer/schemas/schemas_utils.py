import re

EQUIV_CHARS = {
    "á": "a",
    "ä": "a",
    "â": "a",
    "à": "a",
    "ã": "a",
    "å": "a",
    "é": "e",
    "ë": "e",
    "ê": "e",
    "è": "e",
    "í": "i",
    "ï": "i",
    "î": "i",
    "ì": "i",
    "ó": "o",
    "ö": "o",
    "ô": "o",
    "ò": "o",
    "õ": "o",
    "ø": "o",
    "ú": "u",
    "ü": "u",
    "û": "u",
    "ù": "u",
    "ñ": "n",
    "ç": "c",
}


def sanitize_text(text: str, max_len: int | None = 31) -> str:
    """
    Sanitize a string by converting it to lowercase, replacing special
    characters, and removing non-alphanumeric characters except dots.
    """
    # Convert to lowercase
    text = text.lower()

    # Replace special characters
    for char, equiv in EQUIV_CHARS.items():
        text = text.replace(char, equiv)

    # Replace spaces with underscores
    text = re.sub(r"[\s]+", "_", text)

    # Keep only alphanumeric characters and dots
    text = re.sub(r"[^a-z0-9.]", "", text)

    if max_len is not None:
        text = text[:max_len]

    return text


def consolidate_id(*args: str) -> str:
    """
    Create a consolidated ID from a string by sanitizing it and removing
    consecutive dots.
    """
    text = ".".join(args)

    # Convert to lowercase
    text = text.lower()

    # Replace special characters
    for char, equiv in EQUIV_CHARS.items():
        text = text.replace(char, equiv)

    # Replace separators with dots
    text = re.sub(r"[\s_:-]+", "_", text)

    # Keep only alphanumeric characters and dots
    text = re.sub(r"[^a-z0-9.]", "", text)

    # Clean up dots
    text = re.sub(r"\.+", ".", text)

    # Remove leading/trailing dots
    text = text.strip(".")

    return text
