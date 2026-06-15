from __future__ import annotations

from MAKSIMAR_SERVER.MEMORY_SYNC.junior_feedback_ingest_contract import (
    build_junior_feedback_ingest_contract,
)


def test_junior_feedback_ingest_contract_is_proposal_and_evidence_only() -> None:
    read_model = build_junior_feedback_ingest_contract().to_read_model()

    assert read_model["junior_feedback_allowed"] is True
    assert read_model["feedback_ingest_is_proposal_only"] is True
    assert read_model["feedback_ingest_is_evidence_only"] is True
    assert read_model["feedback_may_create_server_intent_candidate"] is True
    assert read_model["feedback_may_execute_actions"] is False
    assert read_model["feedback_may_write_canonical_memory"] is False
    assert read_model["feedback_may_mutate_core"] is False
    assert read_model["feedback_may_deploy"] is False
    assert read_model["feedback_requires_server_review"] is True
    assert read_model["owner_approval_required_for_mutation"] is True
    assert read_model["server_remains_canonical_authority"] is True
