from __future__ import annotations

from typing import Literal

Tier = Literal["T0", "T1", "T2", "T3"]


def tier_for_score(score: float) -> Tier:
    if score >= 0.75:
        return "T3"
    if score >= 0.50:
        return "T2"
    if score >= 0.25:
        return "T1"
    return "T0"
