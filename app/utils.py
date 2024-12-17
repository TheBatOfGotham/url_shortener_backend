import string
from datetime import date

BASE62_ALPHABET = string.digits + string.ascii_letters

def encode_base62(number: int) -> str:
    if number == 0:
        return BASE62_ALPHABET[0]
    base62 = []
    while number:
        number, remainder = divmod(number, 62)
        base62.append(BASE62_ALPHABET[remainder])
    return ''.join(reversed(base62))

def is_rate_limited(url_entry, max_requests_per_day=20):
    today = date.today()
    if url_entry.last_hit_date != today:
        url_entry.hit_count = 0
        url_entry.last_hit_date = today
    return url_entry.hit_count >= max_requests_per_day
