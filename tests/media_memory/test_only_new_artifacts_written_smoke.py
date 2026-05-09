from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.media_memory import build_artifact_dedup_contract


def test_only_new_artifacts_written_smoke() -> None:
    contract = build_artifact_dedup_contract()

    new_candidates = tuple(
        decision for decision in contract.decisions if decision.status == "new_artifact_candidate"
    )

    assert new_candidates
    for decision in new_candidates:
        assert decision.write_allowed is True
        assert decision.rewrite_forbidden is False
        assert decision.existing_record_ref == ""
