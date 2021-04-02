from hashlib import md5
from datetime import datetime

MARVEL_PUBLIC_KEY = "0000000000000000000000000000000"
MARVEL_PRIVATE_KEY = "000000000000000000000000000000000000"


def get_hash_ts() -> tuple:
    ts = _get_ts()
    s = str(ts) + MARVEL_PRIVATE_KEY + MARVEL_PUBLIC_KEY
    my_hash = md5(s.encode())
    return my_hash.hexdigest(), ts


def _get_ts() -> int:
    h = datetime.now()
    return int(h.timestamp())
