from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

from omphalos.core.time import deterministic_now_iso


def write_narrative_deltas(
    run_dir: Path,
    entity_scores: List[dict[str, Any]],
    sensitivity: Dict[str, Any],
    run_id: str,
    clock_seed: str,
) -> List[str]:
    rel = "exports/narratives/deltas.md"
    path = run_dir / rel
    path.parent.mkdir(parents=True, exist_ok=True)

    top = entity_scores[:5]
    lines = []
    lines.append(f"# Narrative deltas\n")
    lines.append(f"- run_id: `{run_id}`\n")
    lines.append(f"- created_at: `{deterministic_now_iso(clock_seed, salt='narrative')}`\n")
    lines.append("\n## Sensitivity\n")
    lines.append(f"- count: {sensitivity.get('count')}\n")
    lines.append(f"- p50: {sensitivity.get('p50')}\n")
    lines.append(f"- p90: {sensitivity.get('p90')}\n")
    lines.append(f"- max: {sensitivity.get('max')}\n")
    lines.append("\n## Top entities\n")
    for r in top:
        lines.append(f"- {r['entity_id']} — score {r['chokepoint_score']}, value {r['total_value_usd']}\n")

    path.write_text("".join(lines), encoding="utf-8")
    return [rel]
