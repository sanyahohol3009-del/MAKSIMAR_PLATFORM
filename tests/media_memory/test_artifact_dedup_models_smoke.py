from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.media_memory import build_artifact_dedup_contract


def test_artifact_dedup_models_smoke() -> None:
    contract = build_artifact_dedup_contract()

    assert contract.total_decisions == len(contract.decisions)
    assert contract.existing_artifacts >= 1
    assert contract.new_artifact_candidates >= 1
