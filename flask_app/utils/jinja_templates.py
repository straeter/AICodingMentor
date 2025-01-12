import urllib.parse
from datetime import datetime
import base64

def encode_path(path):
    """
    Encodes a file path to a string using Base64.
    """
    if not path:
        return ""
    return base64.urlsafe_b64encode(path.encode('utf-8')).decode('utf-8')

def decode_path(encoded_string):
    """
    Decodes the Base64 string back to the original file path.
    """
    if not encoded_string:
        return ""
    return base64.urlsafe_b64decode(encoded_string.encode('utf-8')).decode('utf-8')


def format_query_string(value: str):
    encoded_variable = urllib.parse.quote(value)
    return encoded_variable


def format_datetime(value: str):
    if not value:
        return "NaN"

    if isinstance(value, datetime):
        value = value.strftime('%Y-%m-%d-%H:%M')
    return value[:10].replace("T", "-")


def get_level_color(level) -> str:
    level = int(level)

    if level == 1:
        return "darkgreen"
    elif level == 2:
        return "green"
    elif level == 3:
        return "yellow"
    elif level == 4:
        return "orange"
    elif level == 5:
        return "red"
