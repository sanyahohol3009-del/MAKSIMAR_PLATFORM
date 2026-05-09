from __future__ import annotations

from MAKSIMAR_CORE_LIB.evidence_memory import build_evidence_memory_contract
from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing import (
    build_evidence_memory_core_binding_contract,
)


def test_evidence_memory_core_id_match_smoke() -> None:
    core = build_evidence_memory_contract()
    binding = build_evidence_memory_core_binding_contract()

    core_ids = tuple(record.evidence_id for record in core.records)
    binding_ids = tuple(entry.evidence_id for entry in binding.entries)

    assert binding_ids == core_ids
    assert binding.matched_evidence_items == binding.total_bindings
