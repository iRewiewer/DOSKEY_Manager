from random import choice, choices
from re import sub
from string import ascii_letters, ascii_lowercase, ascii_uppercase, digits

from .paths import ASSETS_DIR


def generate_random_content(kind, length):
    pools = {
        "d": digits,
        "sc": ascii_lowercase,
        "bc": ascii_uppercase,
        "mc": ascii_letters,
        "dsc": digits + ascii_lowercase,
        "dbc": digits + ascii_uppercase,
        "dmc": digits + ascii_letters,
    }
    pool = pools.get(kind)
    if not pool:
        return "unsupported_syntax_for_generating_random_content"
    return "".join(choices(pool, k=length))


def process_placeholders(content):
    def replacer(match):
        kind = match.group(1)
        length = int(match.group(2))
        return generate_random_content(kind, length)

    return sub(r"%_random_([a-z]+)_(\d+)_%", replacer, content)


def display_title():
    active_folder = ASSETS_DIR / "welcome_screens" / "active"
    active_folder.mkdir(parents=True, exist_ok=True)
    screens = [item for item in active_folder.iterdir() if item.suffix.lower() == ".txt"]
    if not screens:
        return

    selected = choice(screens)
    with open(selected, "r", encoding="utf-8") as file:
        print(process_placeholders(file.read()) + "\n")
