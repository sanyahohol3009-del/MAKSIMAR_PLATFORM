from __future__ import annotations

from MAKSIMAR_CORE_LIB.update_recovery.offline_import_gate_contract import (
    OfflineImportCandidate,
    OfflineImportGateDecisionStatus,
    evaluate_offline_import_gate,
)

ONE = "1" * 64


def test_offline_import_gate_accepts_safe_import_for_verification_only() -> None:
    candidate = OfflineImportCandidate(
        import_id="offline-import-001",
        package_id="update-package-001",
        source_uri="offline-media://usb-001/update-package-001",
        package_sha256=ONE,
        created_at_utc="2026-01-01T00:00:00Z",
        signature_present=True,
        air_gap_transfer_confirmed=True,
        media_quarantined=True,
        operator_approval_present=True,
    )

    decision = evaluate_offline_import_gate(candidate)

    assert decision.status is OfflineImportGateDecisionStatus.ACCEPTED_FOR_VERIFICATION
    assert decision.offline_import_allowed_for_verification is True
    assert decision.update_apply_allowed is False
    assert decision.dashboard_execution_allowed is False


def test_offline_import_gate_rejects_unsafe_import() -> None:
    candidate = OfflineImportCandidate(
        import_id="offline-import-001",
        package_id="update-package-001",
        source_uri="offline-media://usb-001/update-package-001",
        package_sha256=ONE,
        created_at_utc="2026-01-01T00:00:00Z",
        signature_present=False,
        air_gap_transfer_confirmed=True,
        media_quarantined=False,
        operator_approval_present=False,
    )

    decision = evaluate_offline_import_gate(candidate)

    assert decision.status is OfflineImportGateDecisionStatus.REJECTED
    assert decision.offline_import_allowed_for_verification is False
    assert "missing_signature" in decision.reason_codes
    assert "media_quarantine_missing" in decision.reason_codes
    assert "operator_approval_missing" in decision.reason_codes
