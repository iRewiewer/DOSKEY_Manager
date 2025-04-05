from os import path, makedirs, listdir
from random import choice, choices
from re import sub
from string import digits, ascii_lowercase, ascii_uppercase, ascii_letters


def generate_random_content(kind, length):
    """
    Generate random content based on the kind and length.
    - Supported kinds:
      - d: digits
      - sc: small letters
      - bc: big letters
      - mc: mixed letters (both big and small)
      - dsc: digits and small letters
      - dbc: digits and big letters
      - dmc: digits, big and small letters
    """
    if kind == 'd':  # Digits only
        pool = digits
    elif kind == 'sc':  # Small letters
        pool = ascii_lowercase
    elif kind == 'bc':  # Big letters
        pool = ascii_uppercase
    elif kind == 'mc':  # Mixed letters (small + big)
        pool = ascii_letters
    elif kind == 'dsc':  # Digits + small letters
        pool = digits + ascii_lowercase
    elif kind == 'dbc':  # Digits + big letters
        pool = digits + ascii_uppercase
    elif kind == 'dmc':  # Digits + big + small letters
        pool = digits + ascii_letters
    else:  # Fallback case
        return 'unsupported_syntax_for_generating_random_content'

    return ''.join(choices(pool, k=length))


def process_placeholders(content):
    """Process the content and replace placeholders with random content."""
    def replacer(match):
        kind = match.group(1)
        length = int(match.group(2))
        return generate_random_content(kind, length)

    placeholder_pattern = r"%_random_([a-z]+)_(\d+)_%"
    return sub(placeholder_pattern, replacer, content)


if __name__ == "__main__":
    script_dir = path.dirname(path.abspath(__file__))
    welcome_screens_path = path.join(script_dir, "welcome_screens")
    active_folder_path = path.join(welcome_screens_path, "active")

    makedirs(active_folder_path, exist_ok=True)

    txt_files = [f for f in listdir(active_folder_path) if f.endswith(".txt")]

    if not txt_files:
        print("")
    else:
        selected_file = choice(txt_files)
        selected_file_path = path.join(active_folder_path, selected_file)

        with open(selected_file_path, "r", encoding="utf-8") as file:
            file_content = file.read()
            processed_content = process_placeholders(file_content)
            print(processed_content + ("\n" * 1))
