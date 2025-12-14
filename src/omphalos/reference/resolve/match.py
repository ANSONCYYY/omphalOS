from __future__ import annotations

import json
from typing import Any, Dict, List, Tuple

from .features import jaccard, tokenize
from .explain import explain_match
from .review_queue import make_review_item


def resolve_entities(
    trade_rows: List[dict[str, Any]],
    registry_rows: List[dict[str, Any]],
) -> Tuple[List[dict[str, Any]], List[dict[str, Any]], Dict[str, int]]:
    registry = [(r["entity_id"], r["entity_name"]) for r in registry_rows]

    matches: List[dict[str, Any]] = []
    review: List[dict[str, Any]] = []
    matched = 0

    for t in trade_rows:
        exp = t["exporter_name"]
        exp_tokens = tokenize(exp)
        scored: List[Tuple[float, str, str, Any]] = []
        for eid, ename in registry:
            et = tokenize(ename)
            s = jaccard(exp_tokens, et)
            scored.append((s, eid, ename, et))
        scored.sort(key=lambda x: (-x[0], x[1]))  # deterministic tie-break

        best_s, best_eid, best_name, best_tokens = scored[0]
        second_s = scored[1][0] if len(scored) > 1 else 0.0
        explanation = explain_match(exp, best_name, best_s, exp_tokens, best_tokens)

        # Deterministic decision policy:
        # - accept confident matches
        # - route low confidence or low margin (ambiguous) cases to review
        status = "REVIEW"
        if best_s >= 0.80 and (best_s - second_s) >= 0.10:
            status = "MATCH"
            matched += 1

        matches.append({
            "shipment_id": t["shipment_id"],
            "entity_id": best_eid,
            "score": float(best_s),
            "status": status,
            "explanation": json.dumps(explanation, sort_keys=True),
        })

        if status == "REVIEW":
            candidates = [{"entity_id": eid, "entity_name": en, "score": float(s)} for s, eid, en, _ in scored[:3]]
            review.append(make_review_item(t["shipment_id"], exp, candidates, reason="ambiguous_or_low_score"))

    stats = {"total": len(trade_rows), "matched": matched, "review": len(review)}
    return matches, review, stats
