from __future__ import annotations

import re
from typing import Iterable

_PATTERNS: list[re.Pattern[str]] = [
    re.compile(r"-----BEGIN (RSA|DSA|EC|OPENSSH|PRIVATE) KEY-----"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"(?i)(api[_-]?key|secret|token)\s*[:=]\s*['\"][A-Za-z0-9_\-]{16,}['\"]"),
]


def redact_text(text: str, replacement: str = "[REDACTED]") -> str:
    out = text
    for p in _PATTERNS:
        out = p.sub(replacement, out)
    return out


def redact_fields(d: dict[str, object], keys: Iterable[str]) -> dict[str, object]:
    out = dict(d)
    for k in keys:
        v = out.get(k)
        if isinstance(v, str):
            out[k] = redact_text(v)
    return out
