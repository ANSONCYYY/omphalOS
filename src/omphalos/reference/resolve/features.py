from __future__ import annotations

import re
from typing import List, Set


_PUNCT_RE = re.compile(r"[^A-Z0-9\s-]")

_STOPWORDS: Set[str] = {
    "INC",
    "LLC",
    "LTD",
    "CO",
    "CORP",
    "CORPORATION",
    "COMPANY",
    "GROUP",
    "HOLDINGS",
    "HOLDING",
    "LIMITED",
}


def canonical_tokens(text: str) -> List[str]:
    """Stable token list used for both matching and display.

    Keeps original token order (after normalization) so a canonicalized name can
    be rendered deterministically.
    """

    s = text.upper()
    s = _PUNCT_RE.sub(" ", s)
    s = s.replace("-", " ")
    toks = [t for t in s.split() if t]
    return [t for t in toks if t not in _STOPWORDS]


def canonical_name(text: str) -> str:
    return " ".join(canonical_tokens(text))


def tokenize(text: str) -> Set[str]:
    """Tokenize text for deterministic matching.

    - uppercase
    - remove punctuation (keep letters, digits, spaces, hyphens)
    - split on whitespace and hyphens
    - drop generic corporate suffix tokens
    """

    return set(canonical_tokens(text))


def jaccard(a: Set[str], b: Set[str]) -> float:
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    inter = len(a & b)
    union = len(a | b)
    return inter / union
