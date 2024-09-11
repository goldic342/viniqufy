import base64
import os
from string import digits, ascii_letters


def validate_spotify_id(spotify_id: str) -> bool:
    """
    Validates spotify id by length and contains only base-62 characters
    :param spotify_id: Base-62 spotify id
    :return: True if id is valid
    """
    if len(spotify_id) != 22:
        return False

    base62_chars = digits + ascii_letters

    for char in spotify_id:
        if char not in base62_chars:
            return False

    return True


def base64_id() -> str:
    random_bytes = os.urandom(16)
    return base64.urlsafe_b64encode(random_bytes).decode('utf-8').rstrip('=')
