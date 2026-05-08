from __future__ import annotations

from pathlib import Path

from MAKSIMAR_SERVER.OBSERVABILITY.memory_skill_metrics import (
    build_memory_skill_metrics_contract,
)


def test_memory_skill_metrics_no_single_entry_limit_smoke() -> None:
    source = Path(
        "MAKSIMAR_SERVER/OBSERVABILITY/memory_skill_metrics/memory_skill_metrics_contract.py"
    ).read_text(encoding="utf-8")

    assert "Expected exactly one canonical memory registry entry" not in source
    assert "Expected exactly one canonical skill registry entry" not in source

    contract = build_memory_skill_metrics_contract()
    assert contract.total_entries == len(contract.entries)
