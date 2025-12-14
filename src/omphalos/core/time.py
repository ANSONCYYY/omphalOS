from __future__ import annotations

import datetime as dt

from .fingerprint import sha256_bytes

_EPOCH = dt.datetime(2000, 1, 1, 0, 0, 0, tzinfo=dt.timezone.utc)


def deterministic_now_iso(seed: str, salt: str = "") -> str:
    """Deterministic clock derived from (seed, salt)."""
    b = (seed + "|" + salt).encode("utf-8")
    h = sha256_bytes(b)
    seconds = int(h[:16], 16) % (20 * 365 * 24 * 3600)
    ts = _EPOCH + dt.timedelta(seconds=seconds)
    return ts.replace(microsecond=0).strftime("%Y-%m-%dT%H:%M:%SZ")
