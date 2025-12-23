from __future__ import annotations

from typing import Any, Dict, List


def compute_sensitivity(entity_scores: List[dict[str, Any]]) -> Dict[str, Any]:
    scores = [float(r["chokepoint_score"]) for r in entity_scores]
    if not scores:
        return {"count": 0, "p50": 0.0, "p90": 0.0, "max": 0.0}

    scores_sorted = sorted(scores)
    def pct(p: float) -> float:
        idx = int(round((len(scores_sorted) - 1) * p))
        return float(scores_sorted[idx])

    return {
        "count": len(scores_sorted),
        "p50": pct(0.50),
        "p90": pct(0.90),
        "max": float(scores_sorted[-1]),
    }
