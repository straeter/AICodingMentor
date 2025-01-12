import secrets
import string


def generate_unique_id(length=16):
    characters = string.ascii_letters  # Uppercase and lowercase letters
    return ''.join(secrets.choice(characters) for _ in range(length))
