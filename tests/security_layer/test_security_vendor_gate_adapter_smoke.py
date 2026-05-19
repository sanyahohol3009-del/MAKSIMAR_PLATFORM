from __future__ import annotations

from MAKSIMAR_SERVER.SECURITY_LAYER.adapters.security_vendor_gate_adapter import (
    VendorGateSecuritySignal,
    evaluate_vendor_gate_signal,
)


def test_vendor_gate_adapter_allows_clean_signal() -> None:
    decision = evaluate_vendor_gate_signal(
        VendorGateSecuritySignal(
            backend_id="clean_backend",
            official_remote_verified=True,
            commit_seen_in_remote_refs=True,
            canonical_memory_access=False,
            runtime_mutation_allowed=False,
            risky_static_findings_count=0,
            dependency_vulnerabilities_count=0,
            verified_secret_found=False,
            manual_security_review_required=False,
        )
    )

    assert decision.allowed_for_runtime is True
    assert decision.allowed_for_read_only_reference is True
    assert decision.reason_codes == ("vendor_gate_clean",)


def test_vendor_gate_adapter_blocks_risky_signal_but_keeps_read_only_reference() -> None:
    decision = evaluate_vendor_gate_signal(
        VendorGateSecuritySignal(
            backend_id="risky_backend",
            official_remote_verified=True,
            commit_seen_in_remote_refs=True,
            canonical_memory_access=False,
            runtime_mutation_allowed=False,
            risky_static_findings_count=7,
            dependency_vulnerabilities_count=0,
            verified_secret_found=False,
            manual_security_review_required=True,
        )
    )

    assert decision.allowed_for_runtime is False
    assert decision.allowed_for_read_only_reference is True
    assert "risky_static_findings_present" in decision.reason_codes
    assert "manual_security_review_required" in decision.reason_codes
    assert decision.to_read_model().dashboard_safe is True
