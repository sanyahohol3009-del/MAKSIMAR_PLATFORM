from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.media_memory import build_artifact_dedup_contract


def test_existing_artifact_not_rewritten_smoke() -> None:
    contract = build_artifact_dedup_contract()

    existing = tuple(decision for decision in contract.decisions if decision.status == "existing_artifact")

    assert existing
    for decision in existing:
        assert decision.write_allowed is False
        assert decision.rewrite_forbidden is True
        assert decision.existing_record_ref
