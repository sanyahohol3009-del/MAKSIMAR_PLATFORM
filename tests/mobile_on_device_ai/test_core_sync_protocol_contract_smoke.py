from __future__ import annotations

from MAKSIMAR_CORE_LIB.mobile_bridge.core_sync_protocol_contract import (
    build_core_sync_protocol_contract,
)


def test_core_sync_protocol_contract_keeps_server_authority() -> None:
    read_model = build_core_sync_protocol_contract().to_read_model()

    assert read_model["sync_direction"] == "server_senior_to_mobile_junior"
    assert read_model["mobile_feedback_allowed"] is True
    assert read_model["mobile_feedback_is_proposal_only"] is True
    assert read_model["mobile_feedback_canonical_write"] is False
    assert read_model["junior_sync_authority"] is False
    assert read_model["server_remains_canonical_authority"] is True
    assert read_model["conflict_resolution_on_server_only"] is True
