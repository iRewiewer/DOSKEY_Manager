import os
import random
import re
import string


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
        pool = string.digits
    elif kind == 'sc':  # Small letters
        pool = string.ascii_lowercase
    elif kind == 'bc':  # Big letters
        pool = string.ascii_uppercase
    elif kind == 'mc':  # Mixed letters (small + big)
        pool = string.ascii_letters
    elif kind == 'dsc':  # Digits + small letters
        pool = string.digits + string.ascii_lowercase
    elif kind == 'dbc':  # Digits + big letters
        pool = string.digits + string.ascii_uppercase
    elif kind == 'dmc':  # Digits + big + small letters
        pool = string.digits + string.ascii_letters
    else:  # Fallback case
        return 'unsupported_syntax_for_generating_random_content'

    return ''.join(random.choices(pool, k=length))


def process_placeholders(content):
    def replacer(match):
        kind = match.group(1)
        length = int(match.group(2))
        return generate_random_content(kind, length)

    placeholder_pattern = r"%_random_([a-z]+)_(\d+)_%"
    return re.sub(placeholder_pattern, replacer, content)


script_dir = os.path.dirname(os.path.abspath(__file__))
welcome_screens_path = os.path.join(script_dir, "welcome_screens")
active_folder_path = os.path.join(welcome_screens_path, "active")

os.makedirs(active_folder_path, exist_ok=True)

txt_files = [f for f in os.listdir(active_folder_path) if f.endswith(".txt")]

if not txt_files:
    print("")
else:
    selected_file = random.choice(txt_files)
    selected_file_path = os.path.join(active_folder_path, selected_file)

    with open(selected_file_path, "r", encoding="utf-8") as file:
        content = file.read()
        processed_content = process_placeholders(content)
        print(processed_content + ("\n" * 1))
