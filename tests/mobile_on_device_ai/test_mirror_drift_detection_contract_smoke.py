from __future__ import annotations

from MAKSIMAR_CORE_LIB.mobile_bridge.mirror_drift_detection_contract import (
    build_mirror_drift_detection_contract,
)


def test_mirror_drift_detection_contract_is_evidence_only() -> None:
    read_model = build_mirror_drift_detection_contract().to_read_model()

    assert read_model["mirror_drift_detection_enabled"] is True
    assert read_model["drift_detection_read_only"] is True
    assert read_model["drift_report_is_evidence_only"] is True
    assert read_model["auto_resolution_allowed"] is False
    assert read_model["junior_model_can_resolve_drift"] is False
    assert read_model["server_review_required"] is True
    assert read_model["server_remains_canonical_authority"] is True
    assert read_model["proposal_only"] is True
