from __future__ import annotations

import math
from typing import Any, Dict, List, Tuple


_CHOKEPOINT_HS = {"8504", "8542", "8471", "9013"}  # illustrative


def compute_chokepoint_scores(
    trade_rows: List[dict[str, Any]],
    matches: List[dict[str, Any]],
    registry_rows: List[dict[str, Any]],
) -> List[dict[str, Any]]:
    ship_to_entity = {m["shipment_id"]: m["entity_id"] for m in matches}
    entity_meta = {r["entity_id"]: (r["entity_name"], r["country"]) for r in registry_rows}

    agg: Dict[str, Dict[str, float]] = {}
    counts: Dict[str, int] = {}
    choke_value: Dict[str, float] = {}

    for t in trade_rows:
        eid = ship_to_entity.get(t["shipment_id"])
        if not eid:
            continue
        counts[eid] = counts.get(eid, 0) + 1
        agg.setdefault(eid, {"total_value": 0.0})
        agg[eid]["total_value"] += float(t["value_usd"])
        if str(t["hs_code"]) in _CHOKEPOINT_HS:
            choke_value[eid] = choke_value.get(eid, 0.0) + float(t["value_usd"])

    totals = [v["total_value"] for v in agg.values()] or [1.0]
    max_total = max(totals)

    rows: List[dict[str, Any]] = []
    for eid, v in sorted(agg.items(), key=lambda kv: kv[0]):
        total = v["total_value"]
        ratio = (choke_value.get(eid, 0.0) / total) if total > 0 else 0.0
        magnitude = math.log1p(total) / math.log1p(max_total) if max_total > 0 else 0.0
        score = round(ratio * magnitude, 6)

        name, country = entity_meta.get(eid, (eid, "ZZ"))
        rows.append({
            "entity_id": eid,
            "entity_name": name,
            "country": country,
            "shipment_count": int(counts.get(eid, 0)),
            "total_value_usd": round(total, 2),
            "chokepoint_score": float(score),
        })

    rows.sort(key=lambda r: (-r["chokepoint_score"], r["entity_id"]))
    return rows
