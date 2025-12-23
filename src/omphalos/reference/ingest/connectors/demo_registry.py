from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Any, List


@dataclass
class DemoRegistryConnector:
    """Deterministic synthetic "registry".

    Design goals for the reference pipeline:
      - include a stable core of entities that the trade feed can resolve against
      - include a small, controlled slice of ambiguity (suffix variants) to exercise review queues
      - remain entirely synthetic and reproducible
    """

    entities: int
    name: str = "registry"

    def read(self, *, seed: int) -> List[dict[str, Any]]:
        rng = random.Random(seed + 1000)

        countries = [
            "US",
            "CA",
            "MX",
            "BR",
            "GB",
            "DE",
            "FR",
            "NL",
            "PL",
            "TR",
            "IN",
            "JP",
            "KR",
            "VN",
            "SG",
        ]

        words = [
            "Aster",
            "Boreal",
            "Cobalt",
            "Dorian",
            "Echelon",
            "Fathom",
            "Gossamer",
            "Halcyon",
            "Iris",
            "Juniper",
            "Kestrel",
            "Lattice",
            "Mosaic",
            "Nimbus",
            "Orchid",
            "Pioneer",
        ]

        def make_base_names(target: int) -> List[str]:
            seen_key: set[str] = set()
            out: List[str] = []
            while len(out) < target:
                nm = f"{rng.choice(words)} {rng.choice(words)}"
                key = " ".join(sorted(nm.split()))
                if key not in seen_key:
                    seen_key.add(key)
                    out.append(nm)
            out.sort()
            return out

        core_base = make_base_names(max(12, min(32, self.entities)))
        ambiguous_base = core_base[:3]  # bounded ambiguity (exercised by trade feed)

        rows: List[dict[str, Any]] = []

        def add_entity(eid_num: int, entity_name: str) -> None:
            eid = f"E{eid_num:04d}"
            rows.append({"entity_id": eid, "entity_name": entity_name, "country": rng.choice(countries)})

        eid_num = 1
        for base in core_base:
            if base in ambiguous_base:
                add_entity(eid_num, f"{base} LLC")
                eid_num += 1
                add_entity(eid_num, f"{base} INC")
                eid_num += 1
            else:
                add_entity(eid_num, f"{base} CO")
                eid_num += 1

            if len(rows) >= self.entities:
                break

        used_keys = {" ".join(sorted(b.split())) for b in core_base}
        while len(rows) < self.entities:
            base = f"{rng.choice(words)} {rng.choice(words)}"
            key = " ".join(sorted(base.split()))
            if key in used_keys:
                continue
            used_keys.add(key)
            add_entity(eid_num, f"{base} HOLDINGS")
            eid_num += 1

        rows.sort(key=lambda r: r["entity_id"])
        return rows
