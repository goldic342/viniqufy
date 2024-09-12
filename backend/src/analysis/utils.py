import base64
import re
from string import digits, ascii_letters
from uuid import UUID


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


def is_valid_base64(base64_str):
    base64_str = base64_str.strip()

    if len(base64_str) % 4 != 0:
        return False

    base64_pattern = re.compile(r'^[A-Za-z0-9+/]*={0,2}$')
    if not base64_pattern.match(base64_str):
        return False

    try:
        return base64.b64encode(base64.b64decode(s)) == s
    except Exception:
        return False


# Made only for a more beautiful look of uuid

def encode_uuid(uuid_str: str | UUID) -> str:
    """
    Encodes UUID bytes to base-64

    :param uuid_str: UUID string
    :return: base-64 encoded UUID
    """
    uuid_obj = UUID(uuid_str)
    uuid_bytes = uuid_obj.bytes

    return base64.urlsafe_b64encode(uuid_bytes).rstrip(b'=').decode('utf-8')


def decode_uuid(base64_str: str) -> str:
    """
    Decodes base-64 encoded UUID to UUID string
    :param base64_str: Base-64 encoded UUID
    :return: decoded UUID string
    """
    padding = '=' * (4 - len(base64_str) % 4)
    base64_str_padded = base64_str + padding

    uuid_bytes = base64.urlsafe_b64decode(base64_str_padded)

    uuid_obj = UUID(bytes=uuid_bytes)

    return str(uuid_obj)
